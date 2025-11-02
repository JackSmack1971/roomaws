# 35-memory-integration-examples.md

## Overview

This document provides **complete, worked examples** of memory integration across different modes. Each example shows the full workflow from memory consultation to knowledge capture, demonstrating how modes should systematically consult and update the hivemind memory graph.

## Example 1: issue-resolver handles "ts-node deprecated" error

### Phase 0: Memory Consultation (MANDATORY)

**Task Context**: User reports "Error: ts-node/register is deprecated" when running tests.

**Step 1: Extract Error Signature**
```
Error pattern: "ts-node/register is deprecated"
Normalized key: ts-node-register-deprecated
Search context: TypeScript, testing, node.js
```

**Step 2: Query Memory**
```javascript
// MCP call to memory:search_nodes
{
  "server_name": "memory",
  "tool_name": "search_nodes",
  "arguments": {
    "query": "type:Error normalizedKey:ts-node-register-deprecated"
  }
}
```

**Step 3: Analyze Results**
```
Memory Response:
- Found 1 matching error: err#ts-node-register-deprecated
- Linked to 3 fixes with success rates
- Top fix: fix#ts-node#a1b2c3d4 (verified_successful, 4/4 applications)
- Evidence: doc#<sha> (DERIVED_FROM) → "Official ts-node migration guide"
```

**Step 4: Document Consultation**
```
✓ Memory consulted: 1 relevant error found with 3 proven fixes
✓ Top recommendation: Switch to ts-node/register/transpile-only
✓ Evidence: Official ts-node docs, 100% success rate in past applications
```

### Phase 1: Solution Implementation

**Apply Learned Fix**
```typescript
// Before (causing error):
require('ts-node/register');

// After (learned from memory):
require('ts-node/register/transpile-only');
```

**Verification**
```bash
npm test  # Should now pass without deprecation warning
```

### Phase 2: Knowledge Capture (MANDATORY)

**Step 1: Create Observation Envelope**
```json
{
  "type": "fix.apply",
  "ts": "2025-11-01T17:00:00.000Z",
  "mode": "issue-resolver@v3.29.4",
  "repo": "user/project",
  "branch": "main",
  "fingerprint": "sha256:...",
  "data": {
    "strategy": "Applied learned fix from memory: ts-node/register → ts-node/register/transpile-only",
    "changes": [
      "Updated require('ts-node/register') to require('ts-node/register/transpile-only') in test setup"
    ],
    "result": "applied",
    "memoryHits": 1,
    "fixId": "fix#ts-node#a1b2c3d4"
  }
}
```

**Step 2: Write to Memory**
```javascript
// MCP call to memory:create_entities
{
  "server_name": "memory",
  "tool_name": "create_entities",
  "arguments": {
    "entities": [{
      "name": "run#issue-123#abc123de",
      "entityType": "Run",
      "observations": ["<fix.apply envelope above>"]
    }]
  }
}
```

**Step 3: Create Relations**
```javascript
// MCP call to memory:create_relations
{
  "server_name": "memory",
  "tool_name": "create_relations",
  "arguments": {
    "relations": [
      {
        "from": "run#issue-123#abc123de",
        "to": "err#ts-node-register-deprecated",
        "relationType": "RESOLVES"
      },
      {
        "from": "run#issue-123#abc123de",
        "to": "fix#ts-node#a1b2c3d4",
        "relationType": "APPLIES"
      },
      {
        "from": "run#issue-123#abc123de",
        "to": "mode#issue-resolver@v3.29.4",
        "relationType": "PERFORMED_BY"
      }
    ]
  }
}
```

**Step 4: Confirm Success**
```
✓ Knowledge persisted: Created run#issue-123#abc123de with 1 observation
✓ Relations established: RESOLVES, APPLIES, PERFORMED_BY
✓ Memory integration complete
```

## Example 2: design-engineer creates responsive component

### Phase 0: Memory Consultation

**Task Context**: Create a responsive button component with hover states.

**Step 1: Extract Pattern Signature**
```
Component pattern: "responsive button with hover states"
Context: React, Tailwind CSS, design system
```

**Step 2: Query Memory**
```javascript
{
  "server_name": "memory",
  "tool_name": "search_nodes",
  "arguments": {
    "query": "type:Fix|Doc component:button responsive hover"
  }
}
```

**Step 3: Analyze Results**
```
Memory Response:
- Found 2 similar button implementations
- Common pattern: Use Tailwind responsive prefixes + group hover
- Evidence: doc#<sha> (REFERENCES) → "Tailwind responsive design guide"
```

### Phase 1: Implementation with Learned Patterns

**Apply Learned Patterns**
```tsx
// Using patterns learned from memory
export const ResponsiveButton = ({ children, variant = 'primary' }) => (
  <button className={`
    // Responsive sizing (learned pattern)
    px-4 py-2 sm:px-6 sm:py-3 md:px-8 md:py-4

    // Hover states (learned pattern)
    group-hover:opacity-80 transition-opacity duration-200

    // Variant styles (design system pattern)
    ${variant === 'primary' ? 'bg-blue-600 hover:bg-blue-700' : 'bg-gray-600 hover:bg-gray-700'}
  `}>
    {children}
  </button>
);
```

### Phase 2: Knowledge Capture

**Create Observation**
```json
{
  "type": "fix.apply",
  "data": {
    "strategy": "Applied responsive button patterns from memory",
    "changes": ["Created ResponsiveButton component using learned Tailwind patterns"],
    "result": "applied",
    "memoryHits": 2,
    "patternsApplied": ["responsive-prefixes", "group-hover-states"]
  }
}
```

## Example 3: test mode handles mocking strategy

### Phase 0: Memory Consultation

**Task Context**: Need to mock API calls in Vitest tests.

**Step 1: Extract Pattern**
```
Testing pattern: "API mocking in Vitest"
Context: JavaScript, testing, API integration
```

**Step 2: Query Memory**
```javascript
{
  "server_name": "memory",
  "tool_name": "search_nodes",
  "arguments": {
    "query": "type:Fix test:mock api vitest"
  }
}
```

**Step 3: Analyze Results**
```
Memory Response:
- Found 3 successful mocking strategies
- Top pattern: Vitest globals + fetch mock (3/3 success)
- Evidence: Multiple test suites using this approach
```

### Phase 1: Apply Learned Strategy

**Implementation**
```typescript
// Learned from memory: Use vitest globals for API mocking
import { expect, test, vi } from 'vitest';

global.fetch = vi.fn();

test('API call', async () => {
  // Mock setup learned from memory
  global.fetch.mockResolvedValueOnce({
    ok: true,
    json: () => Promise.resolve({ data: 'mocked' })
  });

  const result = await apiCall();
  expect(result).toBe('mocked');
});
```

### Phase 2: Knowledge Capture

**Observation Envelope**
```json
{
  "type": "fix.apply",
  "data": {
    "strategy": "Applied Vitest API mocking pattern from memory",
    "changes": ["Used global.fetch = vi.fn() pattern learned from successful tests"],
    "result": "applied",
    "memoryHits": 3,
    "patternSource": "fix#vitest-api-mock#def456"
  }
}
```

## Example 4: Degraded Operation Handling

### When Memory MCP is Unavailable

**Detection**
```
⚠️ DEGRADED MODE: Memory MCP unavailable, operating without historical knowledge
⚠️ Continuing with local context only
⚠️ Will queue memory writes for later replay
```

**Fallback Behavior**
```javascript
// Mode continues execution but logs degradation
console.warn("Memory MCP unavailable - proceeding without historical context");

// Queue writes for later
const queuedWrites = [{
  operation: "create_entities",
  data: { entities: [...] },
  timestamp: new Date().toISOString()
}];

// Continue with task using local knowledge
// ... normal execution ...

// Report degradation in completion summary
return {
  result: "Task completed",
  warnings: ["Memory MCP unavailable - knowledge not persisted"],
  queuedWrites: queuedWrites.length
};
```

**Recovery Process**
```javascript
// When MCP recovers, replay queued writes
for (const write of queuedWrites) {
  try {
    await use_mcp_tool({
      server_name: "memory",
      tool_name: write.operation,
      arguments: write.data
    });
    console.log(`✓ Replayed queued memory write: ${write.operation}`);
  } catch (error) {
    console.error(`✗ Failed to replay memory write: ${error}`);
  }
}
```

## Example 5: Fix Effectiveness Tracking

### Adding Outcome Observation

**After Fix Application**
```json
{
  "type": "fix.outcome",
  "ts": "2025-11-01T18:00:00.000Z",
  "mode": "issue-resolver@v3.29.4",
  "data": {
    "fixId": "fix#ts-node#a1b2c3d4",
    "status": "verified_successful",
    "verificationMethod": "ci_green",
    "durationToVerify": 300000, // 5 minutes in ms
    "sideEffects": [],
    "testCoverage": "increased from 85% to 87%"
  }
}
```

**Create Effectiveness Relation**
```javascript
{
  "server_name": "memory",
  "tool_name": "create_relations",
  "arguments": {
    "relations": [{
      "from": "fix#ts-node#a1b2c3d4",
      "to": "outcome#verified_successful#abc123",
      "relationType": "HAS_OUTCOME"
    }]
  }
}
```

## Key Patterns Demonstrated

### 1. Systematic Memory Consultation
- Always extract signature before querying
- Use specific search terms (type:Error, normalizedKey, etc.)
- Analyze top results before proceeding
- Document consultation outcome

### 2. Evidence-Based Decision Making
- Prefer fixes with high success rates
- Check for official documentation links
- Consider recency of successful applications
- Document reasoning for chosen approach

### 3. Complete Knowledge Capture
- Create observation envelopes with full context
- Use stable keys for idempotency
- Establish all relevant relations
- Confirm write success

### 4. Graceful Degradation
- Detect MCP unavailability
- Continue execution with warnings
- Queue writes for later replay
- Report degradation status

### 5. Continuous Learning Loop
- Track fix effectiveness over time
- Update success rates based on outcomes
- Enable better future recommendations
- Maintain audit trail of all decisions

These examples demonstrate how the memory integration creates a true learning system where each mode contributes to and benefits from the collective knowledge of all modes.