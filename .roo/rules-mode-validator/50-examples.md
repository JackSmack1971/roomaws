# .roo/rules-mode-validator/50-examples.md
> Complete workflow examples demonstrating mode validation from start to finish.

## Example 1: New Mode Configuration Validation

### Scenario
A new mode `api-documenter` has been added to .roomodes and needs comprehensive validation before deployment.

### Workflow Execution

**Step 1: Intake & Preparation**
- Task: Validate new `api-documenter` mode configuration
- Scope: Single mode validation with full analysis
- Prerequisites: .roomodes updated, rules directory created
- Tools prepared: validate_roomodes.py, file access testers

**Step 2: Schema Validation Phase**
```bash
# Run basic schema validation
python validate_roomodes.py --mode api-documenter

# Output:
✅ Schema validation passed for mode: api-documenter
- All required fields present
- Data types correct
- Field formats valid
```

**Step 3: Permission Analysis Phase**
- **FileRegex pattern**: `^(src|packages)/.*\.(ts|tsx|js|jsx)$`
- **Security check**: Test against forbidden directories
- **Coverage analysis**: Verify pattern matches intended API files

```javascript
// Test fileRegex pattern
const testResults = await testFileRegex(
  '^(src|packages)/.*\\.(ts|tsx|js|jsx)$',
  ['src/api/user.ts', 'src/auth/login.ts', 'packages/shared/utils.ts']
);

// Expected results:
// ✅ src/api/user.ts - MATCH (intended)
// ❌ src/auth/login.ts - MATCH (forbidden - security violation)
// ✅ packages/shared/utils.ts - MATCH (intended)
```

**Issue discovered:** Pattern allows access to `src/auth/login.ts` which violates security boundaries.

**Step 4: Rules Directory Validation**
- Check required files exist: 00-guardrails.md, 10-workflow.md, 20-memory-integration.md
- Assess content quality: Each file has substantial, structured content
- Verify consistency: Rules align with .roomodes configuration

```javascript
const rulesCheck = checkRulesCompleteness('./.roo/rules-api-documenter/');
// Output:
// ✅ 00-guardrails.md - Present (245 lines)
// ✅ 10-workflow.md - Present (89 lines)
// ✅ 20-memory-integration.md - Present (156 lines)
// ✅ 30-best-practices.md - Present (78 lines)
```

**Step 5: Functional Testing Phase**
- Test mode loading: Attempt to load api-documenter mode
- Verify tool availability: Check declared tools can be invoked
- Test file access: Confirm fileRegex works in practice

```javascript
const loadTest = await testModeLoading('api-documenter');
// Output:
// ✅ Mode loaded successfully
// ⚠️  Warning: Tool 'codebase_search' response time: 450ms (expected <300ms)
// ✅ All declared tools available
// ❌ File access test failed: Pattern allows forbidden path src/auth/
```

**Step 6: Comprehensive Analysis Phase**
- **Completeness score**: 78% (needs improvement)
- **Cohesion assessment**: Issues found with permission boundaries
- **Best practice compliance**: Good structure, needs security fixes

**Step 7: Reporting & Recommendations**
```markdown
# Mode Validation Report: api-documenter

**Overall Status:** WARNING (Issues require attention)

## Critical Issues
1. **Security Violation**: fileRegex allows access to `src/auth/` directory
   - **Impact**: Potential exposure of authentication code
   - **Fix**: Restrict pattern to `^(src/(api|components|utils)|packages)/.*\.(ts|tsx|js|jsx)$`

## High Priority Issues
2. **Performance Concern**: codebase_search tool response time above threshold
   - **Impact**: Slow mode operation
   - **Fix**: Investigate tool configuration or consider alternatives

## Recommendations
1. Update fileRegex pattern to exclude security-sensitive directories
2. Optimize tool configuration for better performance
3. Add comprehensive test cases for file access patterns
4. Consider adding automated tests for mode loading
```

**Step 8: Remediation Support**
- **Automated fix applied**: Updated fileRegex pattern
- **Verification run**: Re-validated configuration
- **Final status**: PASS with warnings resolved

**Step 9: Memory Integration**
```javascript
// Record validation issues
error.capture({
  kind: "PermissionValidationError",
  message: "fileRegex allows access to forbidden auth directory",
  detector: "security-pattern-matcher",
  normalizedKey: "permission-security-breach",
  context: { mode: "api-documenter", forbiddenPath: "src/auth/" }
});

// Record applied fix
fix.apply({
  strategy: "restrict-file-regex",
  changes: ["Updated fileRegex to exclude auth, payment, security directories"],
  result: "applied",
  context: { mode: "api-documenter", oldPattern: "...", newPattern: "..." }
});
```

## Example 2: Rules Directory Completeness Audit

### Scenario
Multiple modes have incomplete rules directories after a bulk update, requiring systematic validation.

### Workflow Execution

**Step 1: Intake & Preparation**
- Task: Audit rules directory completeness across all modes
- Scope: All modes, focus on rules quality and completeness
- Tools: Rules completeness checker, content quality analyzer

**Step 2: Directory Structure Analysis**
```javascript
const allModes = ['issue-resolver', 'docs-manager', 'mode-validator', 'api-documenter'];
const completenessResults = {};

for (const mode of allModes) {
  const rulesDir = `./.roo/rules-${mode}/`;
  completenessResults[mode] = checkRulesCompleteness(rulesDir);
}

// Output:
// issue-resolver: ✅ Complete (7 files, all required present)
// docs-manager: ⚠️ Incomplete (4 files, missing 30-best-practices.md)
// mode-validator: ✅ Complete (5 files, all required present)
// api-documenter: ❌ Incomplete (3 files, missing 30-best-practices.md, 40-tool-usage.md)
```

**Step 3: Content Quality Assessment**
```javascript
const qualityResults = {};

for (const mode of allModes) {
  const rulesDir = `./.roo/rules-${mode}/`;
  qualityResults[mode] = analyzeRulesQuality(rulesDir);
}

// Output:
// issue-resolver: Score 95% (Excellent content quality)
// docs-manager: Score 82% (Good, needs best practices file)
// mode-validator: Score 88% (Good content, some files could be expanded)
// api-documenter: Score 65% (Needs significant expansion)
```

**Step 4: Gap Analysis**
- **docs-manager**: Missing 30-best-practices.md (needs creation)
- **api-documenter**: Missing 30-best-practices.md and 40-tool-usage.md
- **General**: Some files could benefit from more detailed examples

**Step 5: Remediation Planning**
```javascript
const remediationPlan = {
  'docs-manager': {
    action: 'create_file',
    file: '30-best-practices.md',
    template: 'best-practices-template.md',
    priority: 'HIGH'
  },
  'api-documenter': {
    actions: [
      {
        action: 'create_file',
        file: '30-best-practices.md',
        template: 'best-practices-template.md',
        priority: 'HIGH'
      },
      {
        action: 'create_file',
        file: '40-tool-usage.md',
        template: 'tool-usage-template.md',
        priority: 'MEDIUM'
      }
    ]
  }
};
```

**Step 6: Automated Content Generation**
- Use templates to generate missing best practices files
- Apply consistent structure and content patterns
- Customize content for each mode's specific needs

**Step 7: Quality Verification**
- Re-run completeness and quality checks
- Verify generated content meets standards
- Get peer review for critical content

**Step 8: Final Report**
```markdown
# Rules Completeness Audit Report

**Audit Date:** 2023-10-15
**Modes Audited:** 4
**Overall Completeness:** 78%

## Summary by Mode
- **issue-resolver**: 100% Complete (Reference implementation)
- **docs-manager**: 85% Complete (Missing best practices)
- **mode-validator**: 95% Complete (Minor gaps)
- **api-documenter**: 75% Complete (Multiple missing files)

## Completed Actions
- ✅ Created 30-best-practices.md for docs-manager
- ✅ Created 30-best-practices.md for api-documenter
- ✅ Created 40-tool-usage.md for api-documenter
- ✅ Verified all generated content meets quality standards

## Quality Improvements
- Overall completeness increased from 78% to 92%
- All modes now have basic best practices documentation
- Tool usage guidance added where missing
```

## Example 3: Security Boundary Validation

### Scenario
A recent security audit revealed potential permission issues with multiple modes accessing sensitive directories.

### Workflow Execution

**Step 1: Intake & Preparation**
- Task: Comprehensive security boundary validation
- Scope: All modes, focus on fileRegex patterns and forbidden access
- Security baseline: Define forbidden patterns and test cases

**Step 2: Security Pattern Definition**
```javascript
const securityBaseline = {
  forbiddenPatterns: [
    /\/auth\//,
    /\/authentication\//,
    /\/payment\//,
    /\/billing\//,
    /\/security\//,
    /\/admin\//,
    /credentials/,
    /\.env/
  ],
  testFiles: [
    'src/auth/login.ts',
    'src/payment/stripe.ts',
    'src/security/encryption.ts',
    'src/admin/dashboard.ts',
    'config/credentials.json',
    '.env.production'
  ]
};
```

**Step 3: Pattern Testing Across Modes**
```javascript
const securityResults = {};

for (const mode of allModes) {
  const config = loadModeConfig(mode);
  if (config.fileRegex) {
    securityResults[mode] = checkSecurityBoundaries(
      new RegExp(config.fileRegex),
      securityBaseline.testFiles
    );
  }
}

// Output:
// issue-resolver: ❌ 2 violations (auth/, payment/)
// docs-manager: ✅ No violations
// mode-validator: ✅ No violations
// api-documenter: ❌ 1 violation (auth/)
```

**Step 4: Violation Analysis**
- **issue-resolver**: Allows access to auth and payment directories
- **api-documenter**: Allows access to auth directory
- **Impact**: Potential exposure of sensitive authentication and payment code

**Step 5: Fix Development**
```javascript
// For issue-resolver - current pattern too broad
const currentPattern = '^(src/|packages/|apps/|lib/|server/|client/)(?!.*(?:auth/|payment/|security/|admin/)).*\\.(ts|tsx|js|jsx|py|java|go|rs|cpp|c|php|rb)$';

// Fixed pattern - positive allowlist
const fixedPattern = '^(src/(components|hooks|utils|lib/helpers)|packages/(shared|utils)|apps/(components|utils)|lib/(helpers|utils)|server/(api|utils)|client/(components|utils)).*\\.(ts|tsx|js|jsx|py|java|go|rs|cpp|c|php|rb)$';

// For api-documenter
const apiFixedPattern = '^(src/(api|components|utils)|packages/(shared|utils)).*\\.(ts|tsx|js|jsx)$';
```

**Step 6: Fix Application & Verification**
- Apply pattern fixes to .roomodes
- Re-run security validation
- Confirm no violations remain
- Test that legitimate file access still works

**Step 7: Security Report**
```markdown
# Security Boundary Validation Report

**Validation Date:** 2023-10-15
**Security Status:** CRITICAL ISSUES FOUND

## Critical Security Violations

### Mode: issue-resolver
**FileRegex Pattern:** `^(src/|packages/|apps/|lib/|server/|client/)(?!.*(?:auth/|payment/|security/|admin/)).*...`
**Violations:**
- Allows access to `src/auth/login.ts`
- Allows access to `src/payment/stripe.ts`

**Risk:** Potential exposure of authentication and payment processing code

### Mode: api-documenter
**FileRegex Pattern:** `^(src|packages)/.*\\.(ts|tsx|js|jsx)$`
**Violations:**
- Allows access to `src/auth/config.ts`

**Risk:** Potential exposure of authentication configuration

## Recommended Fixes

### For issue-resolver:
Change fileRegex to: `^(src/(components|hooks|utils|lib/helpers)|packages/(shared|utils)|apps/(components|utils)|lib/(helpers|utils)|server/(api|utils)|client/(components|utils)).*\\.(ts|tsx|js|jsx|py|java|go|rs|cpp|c|php|rb)$`

### For api-documenter:
Change fileRegex to: `^(src/(api|components|utils)|packages/(shared|utils)).*\\.(ts|tsx|js|jsx)$`

## Verification
After applying fixes:
- ✅ No security violations detected
- ✅ All legitimate file access preserved
- ✅ Mode functionality maintained
```

## Example 4: Performance and Functional Testing

### Scenario
Mode performance degradation reported, requiring comprehensive functional validation.

### Workflow Execution

**Step 1: Intake & Preparation**
- Task: Performance and functional validation of all modes
- Scope: Tool response times, mode loading, error handling
- Performance baseline: Define acceptable thresholds

**Step 2: Performance Benchmarking**
```javascript
const performanceBaseline = {
  toolResponseTime: 300, // ms
  modeLoadTime: 500, // ms
  memoryUsage: 50 * 1024 * 1024, // 50MB
  errorRate: 0.01 // 1%
};

const performanceResults = {};

for (const mode of allModes) {
  performanceResults[mode] = await benchmarkMode(mode, performanceBaseline);
}

// Output:
// issue-resolver: ✅ All metrics within baseline
// docs-manager: ⚠️ codebase_search: 450ms (above 300ms threshold)
// mode-validator: ✅ All metrics within baseline
// api-documenter: ❌ Mode load time: 750ms (above 500ms threshold)
```

**Step 3: Functional Testing**
```javascript
const functionalResults = {};

for (const mode of allModes) {
  functionalResults[mode] = await testModeFunctionality(mode);
}

// Output:
// issue-resolver: ✅ All functions working
// docs-manager: ✅ All functions working
// mode-validator: ✅ All functions working
// api-documenter: ⚠️ Warning: 2 tool availability warnings
```

**Step 4: Error Handling Validation**
```javascript
const errorTestResults = {};

for (const mode of allModes) {
  errorTestResults[mode] = await testErrorHandling(mode);
}

// Output:
// issue-resolver: ✅ Proper error handling
// docs-manager: ✅ Proper error handling
// mode-validator: ✅ Proper error handling
// api-documenter: ❌ Unhandled promise rejection in 1 test case
```

**Step 5: Issue Analysis & Prioritization**
- **api-documenter**: Performance issues with mode loading and error handling
- **docs-manager**: Minor performance issue with codebase_search tool
- **Overall**: Good functional health with some optimization opportunities

**Step 6: Optimization Recommendations**
```javascript
const optimizationPlan = {
  'api-documenter': {
    actions: [
      'Optimize mode initialization code',
      'Add proper error boundaries',
      'Cache frequently used tool results',
      'Review tool configurations for performance'
    ],
    expectedImprovement: '50% faster load time'
  },
  'docs-manager': {
    actions: [
      'Review codebase_search configuration',
      'Consider alternative search strategies',
      'Implement result caching'
    ],
    expectedImprovement: '30% faster search responses'
  }
};
```

**Step 7: Implementation & Verification**
- Apply performance optimizations
- Re-run benchmarks to verify improvements
- Update performance baselines if needed

**Step 8: Final Assessment Report**
```markdown
# Performance & Functional Validation Report

**Test Date:** 2023-10-15
**Overall Status:** PASS WITH OPTIMIZATION OPPORTUNITIES

## Performance Summary
- **Average Mode Load Time:** 320ms (Target: <500ms)
- **Average Tool Response Time:** 280ms (Target: <300ms)
- **Memory Usage:** 35MB average (Target: <50MB)
- **Error Rate:** 0.2% (Target: <1%)

## Mode Performance Breakdown

### ✅ issue-resolver
- Load Time: 250ms
- Tool Response: 220ms
- Status: Excellent

### ⚠️ docs-manager
- Load Time: 280ms
- Tool Response: 450ms (codebase_search slow)
- Status: Good with optimization opportunity

### ✅ mode-validator
- Load Time: 310ms
- Tool Response: 260ms
- Status: Good

### ❌ api-documenter
- Load Time: 750ms (above threshold)
- Tool Response: 290ms
- Status: Needs optimization

## Functional Test Results
- **Test Coverage:** 95% of mode functions tested
- **Pass Rate:** 98.5%
- **Critical Failures:** 0
- **Warning Conditions:** 3 (all performance-related)

## Recommendations

### Immediate Actions
1. Optimize api-documenter mode loading (high priority)
2. Review docs-manager search performance

### Monitoring
1. Implement continuous performance monitoring
2. Set up alerts for performance regressions
3. Track mode usage patterns for optimization opportunities

### Future Improvements
1. Implement mode loading caching
2. Optimize tool configurations
3. Add performance profiling capabilities
```

## Example 5: Continuous Validation Integration

### Scenario
Setting up automated validation in CI/CD pipeline to prevent configuration regressions.

### Workflow Execution

**Step 1: Intake & Preparation**
- Task: Implement continuous validation in CI/CD
- Scope: Automated validation on every PR and deployment
- Integration: GitHub Actions, pre-commit hooks, deployment gates

**Step 2: CI Pipeline Design**
```yaml
# .github/workflows/validate-modes.yml
name: Mode Validation

on:
  push:
    branches: [main, develop]
    paths: ['.roomodes', '.roo/rules/**']
  pull_request:
    branches: [main, develop]
    paths: ['.roomodes', '.roo/rules/**']

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup validation environment
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements-validation.txt

      - name: Run schema validation
        run: python validate_roomodes.py --strict --json-report

      - name: Run security validation
        run: python validate_security.py --comprehensive

      - name: Run functional tests
        run: npm run test:modes

      - name: Generate validation report
        run: python generate_report.py --input results/ --output validation-report.json

      - name: Upload validation artifacts
        uses: actions/upload-artifact@v3
        with:
          name: validation-results
          path: |
            validation-report.json
            results/

      - name: Fail on critical issues
        run: |
          if jq '.summary.critical > 0' validation-report.json > /dev/null; then
            echo "❌ Critical validation issues found. See validation-report.json"
            exit 1
          fi

      - name: Comment PR with results
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v6
        with:
          script: |
            const report = require('./validation-report.json');
            const summary = report.summary;

            const body = `
            ## 🔍 Mode Validation Results

            **Status:** ${summary.failed > 0 ? '❌ Failed' : '✅ Passed'}

            ### Summary
            - Critical: ${summary.critical}
            - High: ${summary.high}
            - Medium: ${summary.medium}
            - Low: ${summary.low}

            ${summary.failed > 0 ?
              '### Issues Found\nSee validation-report.json for details.' :
              '### All Checks Passed\nNo validation issues detected.'
            }

            [Download Full Report](https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }}/artifacts/validation-results)
            `;

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: body
            });
```

**Step 3: Pre-commit Hook Setup**
```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "🔍 Running pre-commit validation..."

# Quick validation (fast feedback)
python validate_roomodes.py --quick --fail-on-warnings

if [ $? -ne 0 ]; then
  echo "❌ Validation failed. Please fix issues before committing."
  echo "Run 'python validate_roomodes.py --verbose' for details."
  exit 1
fi

echo "✅ Pre-commit validation passed"
```

**Step 4: Deployment Gate Configuration**
```yaml
# deployment-gate.yml
validation_gate:
  name: "Mode Configuration Validation"
  type: "validation"
  required: true

  checks:
    - name: "Schema Validation"
      command: "python validate_roomodes.py --strict"
      timeout: 300

    - name: "Security Validation"
      command: "python validate_security.py"
      timeout: 300

    - name: "Functional Testing"
      command: "npm run test:modes:functional"
      timeout: 600

  failure_policy:
    on_failure: "block"
    notify_channels: ["#devops", "#security"]
    create_incident: true

  success_policy:
    notify_channels: ["#releases"]
    update_status: "validation-passed"
```

**Step 5: Monitoring & Alerting Setup**
```javascript
// monitoring-config.js
const validationMonitoring = {
  alerts: [
    {
      name: "Validation Failure Rate",
      query: "rate(validation_failures_total[5m]) > 0.1",
      severity: "critical",
      channels: ["#alerts"]
    },
    {
      name: "Performance Degradation",
      query: "validation_duration_seconds{quantile='0.95'} > 300",
      severity: "warning",
      channels: ["#devops"]
    }
  ],

  dashboards: [
    {
      name: "Mode Validation Health",
      panels: [
        "validation_pass_rate",
        "validation_duration",
        "issues_by_severity",
        "issues_by_category"
      ]
    }
  ]
};
```

**Step 6: Testing & Verification**
- Test CI pipeline with various validation scenarios
- Verify pre-commit hooks work correctly
- Test deployment gates with failing validations
- Confirm monitoring and alerting function properly

**Step 7: Documentation & Training**
- Document CI/CD integration process
- Create troubleshooting guide for validation failures
- Train team on validation requirements and processes

**Step 8: Go-Live & Monitoring**
- Deploy validation pipeline to production
- Monitor for false positives and adjust thresholds
- Collect feedback and iterate on validation processes
- Establish regular review process for validation effectiveness