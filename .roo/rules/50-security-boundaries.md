# Security Boundaries (applies to all modes)

## Forbidden Modifications
NEVER edit files matching these patterns, regardless of mode permissions:
- `**/auth/**` - Authentication systems
- `**/authentication/**` - Auth utilities
- `**/payment/**` - Payment processing
- `**/billing/**` - Billing systems
- `**/security/**` - Security infrastructure
- `**/admin/**` - Administrative interfaces
- `**/*credentials*` - Credential handling
- `.env*` (except `.env.example`)
- `**/secrets/**` - Secret storage

## Pre-Edit Validation Protocol
Before ANY file edit operation:

1. **Path Check**: Verify target file path against forbidden patterns
2. **Match Detection**: If ANY pattern matches, STOP immediately
3. **Human Escalation**: Request explicit human review and approval
4. **Memory Logging**: Record attempted access to Memory MCP:
```
warning.capture {
  kind: "SecurityBoundaryViolation",
  path: "<file_path>",
  mode: "<current_mode>",
  normalizedKey: "security-boundary-attempt",
  action: "blocked"
}
```

## Defense-in-Depth Strategy
Even if fileRegex permissions seem to allow access:
- Treat forbidden patterns as **read-only**
- Log all security-relevant file access
- Document unclear boundaries in Memory MCP
- Escalate ambiguous cases before proceeding

## Runtime Guardrails
If you receive edit permissions that conflict with these boundaries:
1. Assume the MORE RESTRICTIVE interpretation
2. Verify intent with human operator
3. Document the permission ambiguity for mode-writer review

## Validating Mode Permissions Against Boundaries

### Regex Test Suite for Validation

Before deploying any mode with edit permissions, validate the fileRegex pattern against these forbidden patterns:

```javascript
// security_boundary_tests.js
const forbiddenPatterns = [
  /.*\/auth\/.*/,
  /.*\/authentication\/.*/,
  /.*\/payment\/.*/,
  /.*\/billing\/.*/,
  /.*\/security\/.*/,
  /.*\/admin\/.*/,
  /.*credentials.*/,
  /^\.env.*/,
  /.*\/secrets\/.*/
];

const testPaths = [
  // Should be BLOCKED (forbidden)
  'src/auth/login.ts',
  'src/authentication/utils.ts',
  'src/payment/processor.ts',
  'src/billing/invoice.ts',
  'src/security/encryption.ts',
  'src/admin/dashboard.ts',
  'src/config/credentials.ts',
  '.env.production',
  'src/secrets/keys.ts',

  // Should be ALLOWED (safe)
  'src/components/Button.tsx',
  'src/hooks/useState.ts',
  'src/utils/format.ts',
  'src/services/api.ts',
  'packages/shared/types.ts'
];

function validateFileRegex(modeRegex, modeName) {
  const violations = [];
  const falsePositives = [];

  testPaths.forEach(path => {
    const matchesMode = modeRegex.test(path);
    const isForbidden = forbiddenPatterns.some(fp => fp.test(path));

    if (matchesMode && isForbidden) {
      violations.push(`VIOLATION: ${path} matches mode but is forbidden`);
    }
    if (!matchesMode && !isForbidden) {
      falsePositives.push(`FALSE POSITIVE: ${path} blocked by mode but is safe`);
    }
  });

  return { violations, falsePositives };
}
```

### Enforcement Checklist for Mode-Writer

Before committing a mode configuration:

- [ ] **Pattern Compilation**: Verify fileRegex compiles without syntax errors
- [ ] **Boundary Testing**: Run regex test suite against all forbidden patterns
- [ ] **Positive Allowlist**: Confirm pattern uses explicit allowlists, not negative exclusions
- [ ] **Single Tuple**: Ensure only one edit tuple in groups array
- [ ] **Anchored Patterns**: Verify all patterns start with ^ and end with $
- [ ] **Description Accuracy**: Confirm description matches actual pattern behavior
- [ ] **Security Review**: Get explicit approval for any broad access patterns
- [ ] **Memory Logging**: Document permission rationale in mode's 00-guardrails.md

### Automated Validation Integration

Integrate with `validate_roomodes.py`:

```python
def validate_security_boundaries(mode_config):
    """Validate mode permissions against security boundaries"""
    if 'groups' not in mode_config:
        return []

    violations = []
    for group in mode_config['groups']:
        if isinstance(group, dict) and 'edit' in group:
            for edit_rule in group['edit']:
                if 'fileRegex' in edit_rule:
                    regex = edit_rule['fileRegex']
                    # Test against forbidden patterns
                    test_results = validate_regex_against_forbidden(regex)
                    if test_results['violations']:
                        violations.extend(test_results['violations'])

    return violations
```

## Audit Trail Requirement
All security boundary violation attempts must be logged to Memory MCP:
- Entity: `warning.capture` with `normalizedKey: "security-boundary-<pattern-matched>"`
- Relation: `(:Run)-[:BLOCKED_BY]->(:SecurityBoundary {pattern: "..."})`
- Human escalation timestamp and decision recorded

See also: 40-memory-mcp-reference.md for complete Memory MCP integration details.