# .roo/rules-mode-validator/30-common-patterns.md
> Reusable validation patterns, templates, and code examples for systematic mode validation.

## Validation Report Templates

### Executive Summary Template
```markdown
# Mode Validation Report

**Validation Date:** [ISO Date]
**Target:** [Single Mode/All Modes]
**Overall Status:** [PASS/FAIL/WARNING]

## Summary
- **Modes Validated:** [count]
- **Critical Issues:** [count]
- **High Priority Issues:** [count]
- **Medium Priority Issues:** [count]
- **Low Priority Issues:** [count]

## Key Findings
- [Top 3 most critical issues]
- [Notable successes or improvements]
- [Trends or patterns identified]

## Recommendations
1. [Highest priority action item]
2. [Second priority action item]
3. [Third priority action item]

## Next Steps
- [Immediate actions required]
- [Scheduled follow-up validations]
- [Process improvements identified]
```

### Detailed Issue Report Template
```markdown
### Issue: [Descriptive Title]

**Severity:** [CRITICAL|HIGH|MEDIUM|LOW|INFO]
**Mode:** [mode-slug]
**Category:** [schema|permissions|rules|functional]

**Description:**
[Clear description of the issue and its impact]

**Evidence:**
- [Specific file/line references]
- [Validation output snippets]
- [Expected vs actual behavior]

**Impact Assessment:**
- **Users Affected:** [who is impacted]
- **Operational Impact:** [how it affects mode operation]
- **Security Impact:** [if applicable]
- **Maintenance Impact:** [difficulty of fixing]

**Recommended Fix:**
[Step-by-step resolution instructions]

**Automated Fix Available:** [Yes/No]
**Estimated Effort:** [hours/days]
**Risk Level:** [LOW|MEDIUM|HIGH]

**Related Issues:**
- [Links to similar issues]
- [Dependencies or prerequisites]
```

## FileRegex Validation Patterns

### Security Boundary Testing
```javascript
// Test patterns against forbidden directories
const forbiddenPatterns = [
  /auth/, /authentication/, /payment/, /billing/,
  /security/, /admin/, /credentials/, /secrets/
];

function testFileRegexSecurity(fileRegex, testPaths) {
  const issues = [];

  for (const testPath of testPaths) {
    if (fileRegex.test(testPath)) {
      for (const forbidden of forbiddenPatterns) {
        if (forbidden.test(testPath)) {
          issues.push({
            path: testPath,
            pattern: forbidden,
            severity: 'CRITICAL',
            message: `FileRegex allows access to forbidden path: ${testPath}`
          });
        }
      }
    }
  }

  return issues;
}
```

### Pattern Completeness Testing
```javascript
// Test that patterns match intended files
function validatePatternCoverage(fileRegex, expectedFiles, actualFiles) {
  const coverage = {
    matched: [],
    missed: [],
    unexpected: []
  };

  for (const file of actualFiles) {
    if (fileRegex.test(file)) {
      if (expectedFiles.includes(file)) {
        coverage.matched.push(file);
      } else {
        coverage.unexpected.push(file);
      }
    } else if (expectedFiles.includes(file)) {
      coverage.missed.push(file);
    }
  }

  return coverage;
}
```

### Regex Syntax Validation
```javascript
// Validate regex patterns compile correctly
function validateRegexPatterns(patterns) {
  const issues = [];

  for (const [mode, pattern] of Object.entries(patterns)) {
    try {
      new RegExp(pattern);
    } catch (error) {
      issues.push({
        mode,
        pattern,
        error: error.message,
        severity: 'CRITICAL',
        message: `Invalid regex pattern: ${error.message}`
      });
    }
  }

  return issues;
}
```

## Schema Validation Patterns

### Required Fields Verification
```javascript
const requiredFields = {
  slug: 'string',
  name: 'string',
  roleDefinition: 'string',
  whenToUse: 'string',
  groups: 'array'
};

function validateRequiredFields(modeConfig) {
  const missing = [];
  const typeMismatches = [];

  for (const [field, expectedType] of Object.entries(requiredFields)) {
    if (!(field in modeConfig)) {
      missing.push(field);
    } else if (typeof modeConfig[field] !== expectedType) {
      typeMismatches.push({
        field,
        expected: expectedType,
        actual: typeof modeConfig[field]
      });
    }
  }

  return { missing, typeMismatches };
}
```

### Field Format Validation
```javascript
function validateFieldFormats(modeConfig) {
  const issues = [];

  // Slug format: lowercase, hyphens allowed
  if (!/^[a-z][a-z0-9-]*$/.test(modeConfig.slug)) {
    issues.push({
      field: 'slug',
      value: modeConfig.slug,
      message: 'Slug must be lowercase with optional hyphens'
    });
  }

  // Name format: starts with emoji, then title case
  if (!/^[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F1E0}-\u{1F1FF}].+/.test(modeConfig.name)) {
    issues.push({
      field: 'name',
      value: modeConfig.name,
      message: 'Name should start with an emoji'
    });
  }

  return issues;
}
```

## Rules Directory Validation Patterns

### File Completeness Checking
```javascript
const requiredRuleFiles = [
  '00-guardrails.md',
  '10-workflow.md',
  '20-memory-integration.md'
  // Add more as needed
];

function validateRulesCompleteness(rulesDir) {
  const issues = [];
  const existingFiles = fs.readdirSync(rulesDir);

  for (const required of requiredRuleFiles) {
    if (!existingFiles.includes(required)) {
      issues.push({
        file: required,
        type: 'missing',
        severity: 'HIGH',
        message: `Required rule file missing: ${required}`
      });
    }
  }

  return issues;
}
```

### Content Quality Assessment
```javascript
function assessRuleContentQuality(filePath) {
  const content = fs.readFileSync(filePath, 'utf8');
  const metrics = {
    lineCount: content.split('\n').length,
    hasCodeExamples: /```/.test(content),
    hasStructuredSections: /^#/.test(content),
    hasActionableGuidance: /\d+\)/.test(content) || /-\s/.test(content)
  };

  const quality = {
    score: 0,
    issues: []
  };

  if (metrics.lineCount < 10) {
    quality.issues.push('File appears too short for meaningful content');
  } else {
    quality.score += 25;
  }

  if (metrics.hasCodeExamples) quality.score += 25;
  if (metrics.hasStructuredSections) quality.score += 25;
  if (metrics.hasActionableGuidance) quality.score += 25;

  return { metrics, quality };
}
```

## Functional Validation Patterns

### Tool Availability Testing
```javascript
async function testToolAvailability(tools) {
  const results = {};

  for (const tool of tools) {
    try {
      // Attempt to invoke tool with safe parameters
      const result = await invokeTool(tool, { dryRun: true });
      results[tool] = {
        available: true,
        responseTime: result.duration,
        status: 'success'
      };
    } catch (error) {
      results[tool] = {
        available: false,
        error: error.message,
        status: 'failed'
      };
    }
  }

  return results;
}
```

### Mode Loading Verification
```javascript
async function validateModeLoading(modeConfigs) {
  const results = {};

  for (const [slug, config] of Object.entries(modeConfigs)) {
    try {
      const mode = await loadMode(config);
      results[slug] = {
        loaded: true,
        warnings: mode.warnings || [],
        status: 'success'
      };
    } catch (error) {
      results[slug] = {
        loaded: false,
        error: error.message,
        status: 'failed'
      };
    }
  }

  return results;
}
```

## Memory Integration Patterns

### Error Capture Templates
```javascript
// Schema validation error
error.capture({
  kind: "SchemaValidationError",
  message: "Missing required field 'roleDefinition'",
  detector: "ajv",
  normalizedKey: "schema-missing-required-field",
  context: {
    mode: modeSlug,
    field: "roleDefinition",
    configPath: ".roomodes"
  }
})

// Permission validation error
error.capture({
  kind: "PermissionValidationError",
  message: "FileRegex allows access to forbidden directory",
  detector: "security-pattern-matcher",
  normalizedKey: "permission-security-breach",
  context: {
    mode: modeSlug,
    fileRegex: pattern,
    forbiddenPath: "/auth/",
    testFile: "src/auth/config.ts"
  }
})
```

### Fix Application Templates
```javascript
// Automated schema fix
fix.apply({
  strategy: "add-missing-field",
  changes: ["Added missing 'whenToUse' field to mode configuration"],
  result: "applied",
  context: {
    mode: modeSlug,
    field: "whenToUse",
    value: "Use this mode when [description]"
  }
})

// Permission fix
fix.apply({
  strategy: "restrict-file-regex",
  changes: ["Updated fileRegex to exclude forbidden directories"],
  result: "applied",
  context: {
    mode: modeSlug,
    oldPattern: "^src/.*",
    newPattern: "^src/(components|utils)/.*"
  }
})
```

## Validation Script Templates

### Comprehensive Validation Runner
```javascript
#!/usr/bin/env node

const { validateSchema, validatePermissions, validateRules } = require('./validators');

async function runComprehensiveValidation() {
  console.log('🔍 Starting comprehensive mode validation...\n');

  const results = {
    schema: await validateSchema(),
    permissions: await validatePermissions(),
    rules: await validateRules(),
    functional: await validateFunctional()
  };

  // Generate report
  const report = generateValidationReport(results);

  // Apply automated fixes
  const fixes = await applyAutomatedFixes(results);

  // Final verification
  const verification = await runVerification(results, fixes);

  console.log('✅ Validation complete');
  console.log(`📊 Report: ${report.path}`);
  console.log(`🔧 Fixes applied: ${fixes.count}`);

  return { results, report, fixes, verification };
}

runComprehensiveValidation().catch(console.error);
```

### Automated Fix Application
```javascript
async function applyAutomatedFixes(validationResults) {
  const fixes = {
    applied: [],
    failed: [],
    skipped: []
  };

  for (const issue of validationResults.allIssues) {
    if (issue.severity === 'CRITICAL' && issue.automatedFix) {
      try {
        await applyFix(issue);
        fixes.applied.push(issue);
      } catch (error) {
        fixes.failed.push({ issue, error: error.message });
      }
    } else {
      fixes.skipped.push(issue);
    }
  }

  return fixes;
}
```

## Quality Assessment Patterns

### Completeness Scoring
```javascript
function calculateCompletenessScore(mode) {
  const weights = {
    schema: 0.2,
    permissions: 0.2,
    rules: 0.3,
    functional: 0.2,
    documentation: 0.1
  };

  const scores = {
    schema: calculateSchemaScore(mode),
    permissions: calculatePermissionsScore(mode),
    rules: calculateRulesScore(mode),
    functional: calculateFunctionalScore(mode),
    documentation: calculateDocumentationScore(mode)
  };

  const totalScore = Object.entries(weights).reduce(
    (sum, [category, weight]) => sum + (scores[category] * weight),
    0
  );

  return {
    total: Math.round(totalScore * 100) / 100,
    breakdown: scores,
    grade: getGradeFromScore(totalScore)
  };
}

function getGradeFromScore(score) {
  if (score >= 0.95) return 'A+';
  if (score >= 0.90) return 'A';
  if (score >= 0.85) return 'B+';
  if (score >= 0.80) return 'B';
  if (score >= 0.70) return 'C+';
  if (score >= 0.60) return 'C';
  return 'D';
}
```

### Cohesion Analysis
```javascript
function analyzeModeCohesion(mode) {
  const cohesion = {
    score: 1.0,
    issues: []
  };

  // Check configuration vs rules alignment
  const configRulesAlignment = checkConfigRulesAlignment(mode);
  if (!configRulesAlignment.aligned) {
    cohesion.score -= 0.2;
    cohesion.issues.push(...configRulesAlignment.issues);
  }

  // Check permissions vs responsibilities
  const permissionResponsibilityFit = checkPermissionResponsibilityFit(mode);
  if (!permissionResponsibilityFit.fits) {
    cohesion.score -= 0.15;
    cohesion.issues.push(...permissionResponsibilityFit.issues);
  }

  // Check tool usage vs declared tools
  const toolUsageConsistency = checkToolUsageConsistency(mode);
  if (!toolUsageConsistency.consistent) {
    cohesion.score -= 0.1;
    cohesion.issues.push(...toolUsageConsistency.issues);
  }

  return cohesion;
}
```

## Continuous Validation Patterns

### Regression Testing
```javascript
function createRegressionTest(issue, fix) {
  return {
    id: `regression-${issue.id}`,
    description: `Prevent regression of: ${issue.description}`,
    test: async () => {
      // Reproduce the original issue conditions
      const reproduction = await reproduceIssue(issue);

      // Verify fix is still effective
      const verification = await verifyFix(fix, reproduction);

      return {
        passed: verification.success,
        details: verification.details
      };
    },
    metadata: {
      originalIssue: issue.id,
      appliedFix: fix.id,
      created: new Date().toISOString()
    }
  };
}
```

### Validation Pipeline Integration
```javascript
function integrateWithCI(validationConfig) {
  return {
    name: 'mode-validation',
    runs: 'node validate-modes.js',
    needs: ['setup', 'lint'],
    if: validationConfig.conditions,
    env: {
      VALIDATION_STRICT: validationConfig.strictMode,
      VALIDATION_REPORT_PATH: './validation-report.json'
    },
    artifacts: {
      name: 'validation-results',
      path: './validation-report.json'
    }
  };
}