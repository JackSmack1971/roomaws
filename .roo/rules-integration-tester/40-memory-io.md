# .roo/rules-integration-tester/40-memory-io.md
> Exact, efficient Memory MCP usage for Integration Tester: general rules + mode-specific patterns for test development, failures, and improvements.

## Read First (decision-oriented)
1) **Exact key**: if a failure signature exists, open `err#<normalizedKey>` and follow `(:Fix)-[:RESOLVES]->(:Error)` (+ optional `(:Fix)-[:DERIVED_FROM]->(:Doc)`).
2) **Command lens**: from `cmd#<canonical>#<fp8>`, traverse `EMITS` to `Error|Warning` and roll up top keys.
3) **Dependency lens**: given `dep#<name>@<ver?>`, find linked Errors and their Fixes.
- Limit to **top-3** candidates; return only fields needed for prompt (strategy, minimal changes, evidence titles).

## Write After (idempotent)
- `command.exec` after runs with `{cmd,cwd?,exitCode,durationMs?,stdoutHead?,stderrHead?}` (truncate heads ~8k).
- On failure/flake: `error.capture` or `warning.capture` with `{kind,message,detector,normalizedKey,job?,step?}`.
- On remediation: `fix.apply` with `{strategy,changes[],result}`; if docs used, `doc.note` and link `Fix DERIVED_FROM Doc`.
- On dependency conflicts: create `Dependency`; link `Error CAUSED_BY Dependency`.

## Stable Names
- Runs/Commands: `run#<iso>#<fp8>`, `cmd#<canonical>#<fp8>`
- Issues: `err#<normalizedKey>`, `warn#<normalizedKey>`
- Fixes/Docs/Deps: `fix#<issue>#<sha8>`, `doc#<sha256(url)>`, `dep#<name>@<ver?>`

## Normalized Key
- Lowercase → strip hashes/paths/timestamps → collapse semver → squeeze spaces (one canonical string across the swarm).

## Safety
- Reads never mutate; open-then-create; skip if exists.
- Never store secrets or full logs; reference files by path when needed.

## Mode-Specific Patterns

### Test Failure Analysis
**When investigating test failures:**
```javascript
// Query for similar test failures
const similarFailures = await search_nodes({
  query: "test failure",
  filters: {
    testSuite: currentTestSuite,
    errorType: extractedErrorType,
    component: affectedComponent
  }
});

// Get resolution patterns for this failure type
const resolutionPatterns = await open_nodes({
  names: similarFailures.map(f => f.resolutionStrategy)
});
```

### Test Development History
**When starting new test development:**
```javascript
// Find successful test patterns for similar scenarios
const successfulPatterns = await search_nodes({
  query: "successful test implementation",
  filters: {
    testType: "integration",
    scenario: similarScenario,
    framework: targetFramework
  }
});

// Retrieve proven test structures
const testTemplates = await open_nodes({
  names: successfulPatterns.map(p => p.templateId)
});
```

### Test Execution Logging
**After each test run:**
```javascript
// Log successful test execution
await create_entities({
  entities: [{
    name: `test-run-${testId}-${timestamp}`,
    entityType: "TestRun",
    observations: [{
      type: "command.exec",
      ts: new Date().toISOString(),
      mode: "integration-tester",
      data: {
        command: testCommand,
        exitCode: 0,
        durationMs: executionTime,
        stdoutHead: testOutput,
        testSuite: suiteName,
        testCount: testCount,
        passCount: passCount,
        failCount: failCount
      }
    }]
  }]
});
```

### Test Failure Capture
**When tests fail:**
```javascript
// Capture test failure details
await create_entities({
  entities: [{
    name: `test-failure-${testId}-${timestamp}`,
    entityType: "TestFailure",
    observations: [{
      type: "error.capture",
      ts: new Date().toISOString(),
      mode: "integration-tester",
      data: {
        kind: "TestFailure",
        message: failureMessage,
        detector: "test-runner",
        normalizedKey: `test-${failureType}`,
        context: {
          testFile: failingTestFile,
          testName: failingTestName,
          errorStack: errorStack,
          environment: testEnvironment,
          dependencies: testDependencies
        }
      }
    }]
  }]
});
```

### Test Fix Documentation
**After resolving test issues:**
```javascript
// Document successful test fix
await create_entities({
  entities: [{
    name: `test-fix-${issueId}-${timestamp}`,
    entityType: "TestFix",
    observations: [{
      type: "fix.apply",
      ts: new Date().toISOString(),
      mode: "integration-tester",
      data: {
        strategy: fixStrategy,
        changes: fixChanges,
        result: "applied",
        context: {
          originalFailure: failureId,
          testFile: affectedTestFile,
          fixType: fixCategory,
          validationResults: postFixTestResults
        }
      }
    }]
  }]
});
```

### Test Pattern Documentation
**When creating reusable test patterns:**
```javascript
// Document successful test pattern
await create_entities({
  entities: [{
    name: `test-pattern-${patternId}`,
    entityType: "TestPattern",
    observations: [{
      type: "doc.note",
      ts: new Date().toISOString(),
      mode: "integration-tester",
      data: {
        url: `file://${testFilePath}`,
        title: patternTitle,
        site: "Test Suite",
        author: "Integration Tester",
        accessed_at: new Date().toISOString(),
        excerpt: patternDescription,
        context: {
          patternType: "integration-test",
          applicability: patternUseCases,
          successRate: patternSuccessMetrics,
          complexity: patternComplexityLevel
        }
      }
    }]
  }]
});
```

### Test Development Workflow Memory
**Track the complete test development process:**
```javascript
// Log each phase of test development
const phases = [
  "requirements-gathering",
  "design-phase",
  "implementation-phase",
  "testing-phase",
  "refinement-phase"
];

for (const phase of phases) {
  await add_observations({
    entityName: `test-dev-${testId}`,
    contents: [{
      type: "run.summary",
      ts: new Date().toISOString(),
      mode: "integration-tester",
      data: {
        phase: phase,
        status: phaseStatus,
        duration: phaseDuration,
        outputs: phaseOutputs,
        challenges: phaseChallenges
      }
    }]
  });
}
```

This memory integration ensures that test development knowledge accumulates over time, enabling better test creation, faster debugging, and continuous improvement of testing practices.