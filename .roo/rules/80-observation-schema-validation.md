# 80-observation-schema-validation.md
> Observation Schema Validation: Typed field validation, schema definitions for all observation types, and validation hooks to prevent corrupted observations from poisoning the knowledge graph.

## Overview

This document defines strict schema validation for all observation types to prevent corrupted or malformed observations from poisoning the knowledge graph. All modes must validate observations before writing them to the Memory MCP.

Corrupted observations can:
- Break graph traversals and queries
- Introduce inconsistent data types
- Cause downstream processing failures
- Pollute pattern recognition algorithms
- Lead to incorrect fix recommendations

## Schema Definitions

### Base Observation Envelope Schema

All observations must conform to this base schema:

```typescript
interface BaseObservation {
  type: ObservationType;
  ts: string; // ISO8601 timestamp
  mode: string; // <slug>@<ver?>
  repo: string; // <owner/repo or path>
  branch: string; // <git-branch>
  fingerprint: string; // sha256 hash
  data: Record<string, any>; // Type-specific data
}

type ObservationType =
  | 'command.exec'
  | 'error.capture'
  | 'warning.capture'
  | 'fix.apply'
  | 'fix.outcome'
  | 'doc.note'
  | 'run.summary';
```

### Type-Specific Data Schemas

#### command.exec

```typescript
interface CommandExecData {
  cmd: string; // The command that was executed (required)
  cwd?: string; // Working directory (optional)
  exitCode: number; // Exit code (required)
  durationMs?: number; // Execution duration in milliseconds (optional)
  stdoutHead?: string; // First ~8k of stdout (optional)
  stderrHead?: string; // First ~8k of stderr (optional)
}
```

#### error.capture

```typescript
interface ErrorCaptureData {
  normalizedKey: string; // Lowercase, stripped key (required)
  kind: string; // Error category (required)
  message: string; // Original error message (required)
  detector: string; // Which mode/component detected it (required)
  context?: Record<string, any>; // Additional context (optional)
}
```

#### warning.capture

```typescript
interface WarningCaptureData {
  normalizedKey: string; // Lowercase, stripped key (required)
  kind: string; // Warning category (required)
  message: string; // Original warning message (required)
  detector: string; // Which mode/component detected it (required)
  context?: Record<string, any>; // Additional context (optional)
}
```

#### fix.apply

```typescript
interface FixApplyData {
  strategy: string; // Description of the fix strategy (required)
  changes: string[]; // List of changes made (required, array of strings)
  result: 'proposed' | 'applied'; // Whether fix was applied (required)
}
```

#### fix.outcome

```typescript
interface FixOutcomeData {
  fixId: string; // Reference to the fix entity (required)
  status: 'verified_successful' | 'failed' | 'partially_effective'; // Outcome status (required)
  verificationMethod: string; // How success was verified (required)
  durationToVerify: number; // Time to verify in milliseconds (required)
  sideEffects: string[]; // Any side effects observed (required, array of strings)
  testCoverage?: string; // Test coverage impact (optional)
}
```

#### doc.note

```typescript
interface DocNoteData {
  url: string; // Canonical URL or DOI (required)
  title?: string; // Page title (optional)
  site?: string; // Publisher site (optional)
  author?: string; // Author or organization (optional)
  published_at?: string; // ISO8601 publish date (optional)
  accessed_at: string; // ISO8601 access date (required)
  archive_url?: string; // Wayback/Perma.cc URL (optional)
  excerpt?: string; // <=500 chars verbatim excerpt (optional)
}
```

#### run.summary

```typescript
interface RunSummaryData {
  summary: string; // High-level summary of outcomes (required)
  keyEvents: string[]; // Important events during the run (required, array of strings)
  success: boolean; // Overall success status (required)
  durationMs: number; // Total run duration (required)
}
```

## Validation Hooks

### Pre-Write Validation Function

```typescript
function validateObservation(observation: any): ValidationResult {
  const baseValidation = validateBaseSchema(observation);
  if (!baseValidation.valid) {
    return baseValidation;
  }

  const typeValidation = validateTypeSpecificData(observation.type, observation.data);
  if (!typeValidation.valid) {
    return typeValidation;
  }

  return { valid: true };
}

interface ValidationResult {
  valid: boolean;
  errors?: string[];
}
```

### Base Schema Validation

```typescript
function validateBaseSchema(obs: any): ValidationResult {
  const errors: string[] = [];

  // Required fields with type checking
  if (!obs.type || typeof obs.type !== 'string') {
    errors.push('Missing or invalid type field (must be string)');
  } else if (!isValidObservationType(obs.type)) {
    errors.push(`Invalid observation type: ${obs.type}`);
  }

  if (!obs.ts || typeof obs.ts !== 'string' || !isValidISO8601(obs.ts)) {
    errors.push('Missing or invalid ts field (must be valid ISO8601 string)');
  }

  if (!obs.mode || typeof obs.mode !== 'string') {
    errors.push('Missing or invalid mode field (must be string)');
  }

  if (!obs.repo || typeof obs.repo !== 'string') {
    errors.push('Missing or invalid repo field (must be string)');
  }

  if (!obs.branch || typeof obs.branch !== 'string') {
    errors.push('Missing or invalid branch field (must be string)');
  }

  if (!obs.fingerprint || typeof obs.fingerprint !== 'string' || !isValidSha256(obs.fingerprint)) {
    errors.push('Missing or invalid fingerprint field (must be valid sha256 string)');
  }

  if (!obs.data || typeof obs.data !== 'object' || Array.isArray(obs.data)) {
    errors.push('Missing or invalid data field (must be object)');
  }

  return { valid: errors.length === 0, errors };
}

function isValidObservationType(type: string): boolean {
  const validTypes = [
    'command.exec', 'error.capture', 'warning.capture',
    'fix.apply', 'fix.outcome', 'doc.note', 'run.summary'
  ];
  return validTypes.includes(type);
}

function isValidISO8601(ts: string): boolean {
  const iso8601Regex = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{3})?Z$/;
  return iso8601Regex.test(ts) && !isNaN(Date.parse(ts));
}

function isValidSha256(hash: string): boolean {
  const sha256Regex = /^[a-f0-9]{64}$/;
  return sha256Regex.test(hash);
}
```

### Type-Specific Validation

```typescript
function validateTypeSpecificData(type: string, data: any): ValidationResult {
  switch (type) {
    case 'command.exec':
      return validateCommandExecData(data);
    case 'error.capture':
      return validateErrorCaptureData(data);
    case 'warning.capture':
      return validateWarningCaptureData(data);
    case 'fix.apply':
      return validateFixApplyData(data);
    case 'fix.outcome':
      return validateFixOutcomeData(data);
    case 'doc.note':
      return validateDocNoteData(data);
    case 'run.summary':
      return validateRunSummaryData(data);
    default:
      return { valid: false, errors: [`Unknown observation type: ${type}`] };
  }
}
```

### Individual Type Validators

```typescript
function validateCommandExecData(data: any): ValidationResult {
  const errors: string[] = [];

  if (!data.cmd || typeof data.cmd !== 'string' || data.cmd.trim().length === 0) {
    errors.push('Missing or invalid cmd field (must be non-empty string)');
  }

  if (data.cwd !== undefined && (typeof data.cwd !== 'string' || data.cwd.trim().length === 0)) {
    errors.push('Invalid cwd field (must be non-empty string if present)');
  }

  if (typeof data.exitCode !== 'number' || !Number.isInteger(data.exitCode)) {
    errors.push('Missing or invalid exitCode field (must be integer)');
  }

  if (data.durationMs !== undefined && (typeof data.durationMs !== 'number' || data.durationMs < 0 || !Number.isInteger(data.durationMs))) {
    errors.push('Invalid durationMs field (must be non-negative integer if present)');
  }

  if (data.stdoutHead !== undefined && typeof data.stdoutHead !== 'string') {
    errors.push('Invalid stdoutHead field (must be string if present)');
  }

  if (data.stderrHead !== undefined && typeof data.stderrHead !== 'string') {
    errors.push('Invalid stderrHead field (must be string if present)');
  }

  return { valid: errors.length === 0, errors };
}

function validateErrorCaptureData(data: any): ValidationResult {
  const errors: string[] = [];

  if (!data.normalizedKey || typeof data.normalizedKey !== 'string' || data.normalizedKey.trim().length === 0) {
    errors.push('Missing or invalid normalizedKey field (must be non-empty string)');
  }

  if (!data.kind || typeof data.kind !== 'string' || data.kind.trim().length === 0) {
    errors.push('Missing or invalid kind field (must be non-empty string)');
  }

  if (!data.message || typeof data.message !== 'string' || data.message.trim().length === 0) {
    errors.push('Missing or invalid message field (must be non-empty string)');
  }

  if (!data.detector || typeof data.detector !== 'string' || data.detector.trim().length === 0) {
    errors.push('Missing or invalid detector field (must be non-empty string)');
  }

  if (data.context !== undefined && (typeof data.context !== 'object' || Array.isArray(data.context))) {
    errors.push('Invalid context field (must be object if present)');
  }

  return { valid: errors.length === 0, errors };
}

function validateWarningCaptureData(data: any): ValidationResult {
  // Same validation as error.capture
  return validateErrorCaptureData(data);
}

function validateFixApplyData(data: any): ValidationResult {
  const errors: string[] = [];

  if (!data.strategy || typeof data.strategy !== 'string' || data.strategy.trim().length === 0) {
    errors.push('Missing or invalid strategy field (must be non-empty string)');
  }

  if (!Array.isArray(data.changes) || data.changes.length === 0) {
    errors.push('Missing or invalid changes field (must be non-empty array)');
  } else if (!data.changes.every((c: any) => typeof c === 'string' && c.trim().length > 0)) {
    errors.push('Invalid changes field (all elements must be non-empty strings)');
  }

  if (!data.result || !['proposed', 'applied'].includes(data.result)) {
    errors.push('Missing or invalid result field (must be "proposed" or "applied")');
  }

  return { valid: errors.length === 0, errors };
}

function validateFixOutcomeData(data: any): ValidationResult {
  const errors: string[] = [];

  if (!data.fixId || typeof data.fixId !== 'string' || data.fixId.trim().length === 0) {
    errors.push('Missing or invalid fixId field (must be non-empty string)');
  }

  if (!data.status || !['verified_successful', 'failed', 'partially_effective'].includes(data.status)) {
    errors.push('Missing or invalid status field (must be valid status enum)');
  }

  if (!data.verificationMethod || typeof data.verificationMethod !== 'string' || data.verificationMethod.trim().length === 0) {
    errors.push('Missing or invalid verificationMethod field (must be non-empty string)');
  }

  if (typeof data.durationToVerify !== 'number' || data.durationToVerify < 0 || !Number.isInteger(data.durationToVerify)) {
    errors.push('Missing or invalid durationToVerify field (must be non-negative integer)');
  }

  if (!Array.isArray(data.sideEffects)) {
    errors.push('Missing or invalid sideEffects field (must be array)');
  } else if (!data.sideEffects.every((s: any) => typeof s === 'string')) {
    errors.push('Invalid sideEffects field (all elements must be strings)');
  }

  if (data.testCoverage !== undefined && typeof data.testCoverage !== 'string') {
    errors.push('Invalid testCoverage field (must be string if present)');
  }

  return { valid: errors.length === 0, errors };
}

function validateDocNoteData(data: any): ValidationResult {
  const errors: string[] = [];

  if (!data.url || typeof data.url !== 'string' || data.url.trim().length === 0) {
    errors.push('Missing or invalid url field (must be non-empty string)');
  } else if (!isValidUrl(data.url)) {
    errors.push('Invalid url field (must be valid URL)');
  }

  if (data.title !== undefined && (typeof data.title !== 'string' || data.title.trim().length === 0)) {
    errors.push('Invalid title field (must be non-empty string if present)');
  }

  if (data.site !== undefined && (typeof data.site !== 'string' || data.site.trim().length === 0)) {
    errors.push('Invalid site field (must be non-empty string if present)');
  }

  if (data.author !== undefined && (typeof data.author !== 'string' || data.author.trim().length === 0)) {
    errors.push('Invalid author field (must be non-empty string if present)');
  }

  if (data.published_at !== undefined && (typeof data.published_at !== 'string' || !isValidISO8601(data.published_at))) {
    errors.push('Invalid published_at field (must be valid ISO8601 string if present)');
  }

  if (!data.accessed_at || typeof data.accessed_at !== 'string' || !isValidISO8601(data.accessed_at)) {
    errors.push('Missing or invalid accessed_at field (must be valid ISO8601 string)');
  }

  if (data.archive_url !== undefined && (typeof data.archive_url !== 'string' || !isValidUrl(data.archive_url))) {
    errors.push('Invalid archive_url field (must be valid URL if present)');
  }

  if (data.excerpt !== undefined && (typeof data.excerpt !== 'string' || data.excerpt.length > 500)) {
    errors.push('Invalid excerpt field (must be string <= 500 chars if present)');
  }

  return { valid: errors.length === 0, errors };
}

function validateRunSummaryData(data: any): ValidationResult {
  const errors: string[] = [];

  if (!data.summary || typeof data.summary !== 'string' || data.summary.trim().length === 0) {
    errors.push('Missing or invalid summary field (must be non-empty string)');
  }

  if (!Array.isArray(data.keyEvents) || data.keyEvents.length === 0) {
    errors.push('Missing or invalid keyEvents field (must be non-empty array)');
  } else if (!data.keyEvents.every((e: any) => typeof e === 'string' && e.trim().length > 0)) {
    errors.push('Invalid keyEvents field (all elements must be non-empty strings)');
  }

  if (typeof data.success !== 'boolean') {
    errors.push('Missing or invalid success field (must be boolean)');
  }

  if (typeof data.durationMs !== 'number' || data.durationMs < 0 || !Number.isInteger(data.durationMs)) {
    errors.push('Missing or invalid durationMs field (must be non-negative integer)');
  }

  return { valid: errors.length === 0, errors };
}

function isValidUrl(url: string): boolean {
  try {
    new URL(url);
    return true;
  } catch {
    return false;
  }
}
```

## Integration with Memory MCP

### Validation Hook Integration

All modes must integrate these validation hooks before calling `add_observations`:

```typescript
async function safeAddObservation(entityName: string, observation: any) {
  const validation = validateObservation(observation);
  if (!validation.valid) {
    throw new Error(`Invalid observation: ${validation.errors?.join(', ')}`);
  }

  await use_mcp_tool({
    server_name: "memory",
    tool_name: "add_observations",
    arguments: {
      observations: [{
        entityName,
        contents: [JSON.stringify(observation)]
      }]
    }
  });
}
```

### Error Handling and Logging

Invalid observations should be logged but not written:

```typescript
async function handleInvalidObservation(observation: any, validation: ValidationResult) {
  console.error('Invalid observation rejected:', {
    observation,
    errors: validation.errors,
    timestamp: new Date().toISOString(),
    mode: observation.mode,
    type: observation.type
  });

  // Write to invalid observations log for debugging
  await logInvalidObservation(observation, validation);
}

async function logInvalidObservation(observation: any, validation: ValidationResult) {
  const invalidLogEntry = {
    type: 'invalid_observation',
    ts: new Date().toISOString(),
    originalObservation: observation,
    validationErrors: validation.errors,
    fingerprint: observation.fingerprint || 'unknown'
  };

  // Write to local log file (not Memory MCP to avoid corruption)
  await writeToInvalidObservationsLog(invalidLogEntry);
}
```

### Circuit Breaker for Validation Failures

```typescript
class ValidationCircuitBreaker {
  private failureCount = 0;
  private lastFailureTime = 0;
  private readonly maxFailures = 5;
  private readonly resetTimeout = 300000; // 5 minutes

  shouldAllowValidation(): boolean {
    if (this.failureCount >= this.maxFailures) {
      if (Date.now() - this.lastFailureTime > this.resetTimeout) {
        this.failureCount = 0; // Reset
        return true;
      }
      return false; // Circuit open
    }
    return true;
  }

  recordValidationFailure() {
    this.failureCount++;
    this.lastFailureTime = Date.now();
  }

  recordValidationSuccess() {
    this.failureCount = Math.max(0, this.failureCount - 1);
  }
}
```

## Testing and Validation

### Schema Test Suite

```typescript
// Comprehensive test suite for observation validation
describe('Observation Schema Validation', () => {
  test('valid command.exec observation passes', () => {
    const validObs = {
      type: 'command.exec',
      ts: '2025-11-01T20:00:00.000Z',
      mode: 'test-mode@v1.0',
      repo: 'owner/repo',
      branch: 'main',
      fingerprint: 'a'.repeat(64),
      data: {
        cmd: 'npm test',
        exitCode: 0,
        durationMs: 1500
      }
    };
    expect(validateObservation(validObs).valid).toBe(true);
  });

  test('invalid observation with missing required field fails', () => {
    const invalidObs = {
      type: 'command.exec',
      ts: '2025-11-01T20:00:00.000Z',
      mode: 'test-mode@v1.0',
      repo: 'owner/repo',
      branch: 'main',
      fingerprint: 'a'.repeat(64),
      data: {
        // Missing cmd
        exitCode: 0
      }
    };
    const result = validateObservation(invalidObs);
    expect(result.valid).toBe(false);
    expect(result.errors).toContain('Missing or invalid cmd field');
  });

  test('invalid observation with wrong data type fails', () => {
    const invalidObs = {
      type: 'command.exec',
      ts: '2025-11-01T20:00:00.000Z',
      mode: 'test-mode@v1.0',
      repo: 'owner/repo',
      branch: 'main',
      fingerprint: 'a'.repeat(64),
      data: {
        cmd: 'npm test',
        exitCode: '0', // Should be number
        durationMs: 1500
      }
    };
    const result = validateObservation(invalidObs);
    expect(result.valid).toBe(false);
    expect(result.errors).toContain('Missing or invalid exitCode field');
  });
});
```

## Implementation Requirements

### For All Modes

1. **Import Validation Functions**: Include the validation hooks in mode workflows
2. **Pre-Write Validation**: Always validate observations before `add_observations` calls
3. **Error Handling**: Log invalid observations without writing them to Memory MCP
4. **Testing**: Include schema validation tests in mode test suites

### Memory MCP Integration

1. **Server-Side Validation**: Implement these validations in the Memory MCP server
2. **Client-Side Guards**: Use these hooks as client-side safety nets
3. **Monitoring**: Track validation failure rates and patterns

### Continuous Improvement

1. **Schema Evolution**: Update schemas with new observation types
2. **Validation Updates**: Add new validation rules as issues are discovered
3. **Performance Monitoring**: Ensure validation doesn't significantly impact performance

This validation framework ensures the knowledge graph remains clean, consistent, and trustworthy by preventing corrupted observations from entering the system.