# File Access Pattern Standards (v3.29.4)

## Critical Rule: Single Edit Tuple Only

⚠️ **IMPORTANT**: Each mode MUST have exactly ONE edit tuple in its groups array.
Multiple edit tuples cause parser bugs and inconsistent permission enforcement.
```yaml
# ✅ CORRECT: Single edit tuple with alternation
groups:
  - read
  - - edit
    - fileRegex: ^(components/|ui/|pages/).*\.(jsx|tsx|css)$
      description: UI files only
  - command

# ❌ WRONG: Multiple edit tuples (causes parser bugs)
groups:
  - read
  - - edit
    - fileRegex: ^components/.*\.tsx$
  - - edit
    - fileRegex: ^pages/.*\.tsx$
  - command
```

## Pattern Design Principles

### ✅ DO:
- **Use positive allowlists**: Explicitly list what's allowed
- **Anchor patterns**: Always use ^ (start) and $ (end)
- **Be specific**: Prefer explicit paths over wildcards
- **Single edit tuple**: Combine all edit patterns with alternation
- **Test thoroughly**: Validate against both allowed and forbidden paths

### ❌ DON'T:
- **Use multiple edit tuples**: Causes parser bugs
- **Use negative lookaheads for security**: `(?!.*auth)` is ineffective
- **Grant directory-wide access**: `src/.*` is too broad
- **Use unanchored wildcards**: `.*\.ts` matches everything
- **Rely on implicit exclusions**: Always make security explicit

## Pattern Examples

### Good: Explicit UI Component Access (Single Tuple)
```yaml
- - edit
  - fileRegex: ^(components/|ui/|pages/).*\.(jsx|tsx|css|scss)$
    description: React components, UI elements, and styles only
```

### Bad: Attempted Security via Negative Lookahead
```yaml
- - edit
  - fileRegex: ^src/(?!.*auth).*\.ts$  # ❌ INEFFECTIVE!
```
**Problem**: Still matches `src/authentication.ts`, `src/utils/auth-helper.ts`

**Why**: Negative lookahead checks if string exists anywhere, not directory boundaries

### Fixed: Positive Allowlist (Single Tuple)
```yaml
- - edit
  - fileRegex: ^src/(components|utils|hooks)/.*\.ts$
    description: Specific subdirectories only - excludes auth, payment, security
```

### Combining Multiple Patterns (Single Tuple)
```yaml
- - edit
  - fileRegex: ^(__tests__/.*|\\.test\\.(ts|tsx|js|jsx)$|vitest\\.config\\.(js|ts)$|test-utils/.*|fixtures/.*\\.json)$
    description: Test files, test config, test utilities, and fixtures only
```

## Negative Lookaheads: Real-World Failures

### Why Negative Lookaheads Fail for Security

Negative lookaheads `(?!.*pattern)` check if a string **does NOT appear anywhere** in the match, not directory boundaries. This creates false security assumptions.

### Test Cases: What Actually Matches

Given pattern: `^src/(?!.*auth).*\.ts$`

**❌ INCORRECTLY ALLOWS** (matches the pattern):
- `src/authentication.ts` - "auth" appears later, but lookahead only checks position after `src/`
- `src/utils/auth-helper.ts` - Same issue
- `src/lib/payment/auth.ts` - Still matches
- `src/security/auth.ts` - Still matches

**✅ CORRECTLY BLOCKS** (does not match):
- `src/auth.ts` - "auth" appears immediately after `src/`, so lookahead fails

### Real-World Failure Example

From merge-resolver mode:
```yaml
fileRegex: ^(src/(?!.*(?:auth|payment|security|admin)).*|packages/(?!.*(?:auth|payment|security|admin)).*|...)$
```

**This pattern ALLOWS editing**:
- `src/authentication.ts`
- `src/utils/payment-processor.ts`
- `packages/shared/security-tokens.js`

### Migration Guide: From Negative Lookaheads to Positive Allowlists

#### Step 1: Identify Allowed Directories
Instead of excluding forbidden ones, explicitly list allowed ones:

**Before (Vulnerable)**:
```yaml
fileRegex: ^src/(?!.*auth).*\.ts$
```

**After (Secure)**:
```yaml
fileRegex: ^src/(components|hooks|utils|lib/helpers|services)/.*\.ts$
description: UI components, non-auth hooks, utility functions, and services only
```

#### Step 2: Handle Complex Cases with Alternation
For multiple allowed patterns in one tuple:

```yaml
fileRegex: ^(src/(components|hooks|utils)/.*\.ts|packages/(shared|utils)/.*\.js)$
description: Source components/hooks/utils and shared packages only
```

#### Step 3: Validate Against Forbidden Patterns
Test your new pattern against these forbidden paths:
- `**/auth/**`
- `**/payment/**`
- `**/security/**`
- `**/admin/**`
- `**/*credentials*`
- `.env*`
- `**/secrets/**`

#### Step 4: Update Descriptions
Ensure descriptions accurately reflect what IS allowed, not what is excluded:

**❌ Misleading**:
```yaml
description: Source files excluding auth, payment, security
```

**✅ Accurate**:
```yaml
description: UI components, business logic, and utility functions only
```

## Validation Checklist
Before committing a fileRegex pattern:
- [ ] Uses single edit tuple (not multiple)
- [ ] Test against security_baseline.json forbidden patterns
- [ ] Verify positive allowlist approach
- [ ] Patterns are anchored with ^ and $
- [ ] Document rationale for any broad access
- [ ] Run mode-tools validation suite
- [ ] Get security review for modes with write access