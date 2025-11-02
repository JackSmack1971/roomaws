# 50-examples.md
> Complete workflow examples demonstrating Sequential Thinking patterns in real scenarios.

## Example 1: P2 Hypothesis-Test Loop - API Timeout Debugging

**Scenario**: API calls timing out intermittently. Need to identify root cause.

**Reasoning Chain**:

```javascript
// Step 1: Form initial hypothesis
sequentialthinking({
  thought: "Hypothesis 1: Timeout caused by slow database queries. Test: Monitor query execution times",
  thoughtNumber: 1,
  totalThoughts: 6,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Identify root cause of API timeout issues",
    pattern: "P2",
    hypothesisState: "proposed",
    testPlan: "Database query profiling"
  }
});

// Step 2: Gather evidence
// Execute: Monitor database queries during timeout period
const dbMetrics = await execute_command({
  command: "pg_stat_statements_query_time",
});

// Step 3: Evaluate hypothesis
sequentialthinking({
  thought: "Test result: DB queries averaging 50ms during timeouts. Hypothesis 1 FALSIFIED - queries not slow enough",
  thoughtNumber: 2,
  totalThoughts: 6,
  isRevision: true,
  revisesThought: 1,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Identify root cause of API timeout issues",
    pattern: "P2",
    hypothesisState: "falsified",
    evidenceRefs: ["cmd:db_query_monitoring"],
    contradictions: ["queries_fast_but_timeout_occurs"]
  }
});

// Step 4: Form new hypothesis
sequentialthinking({
  thought: "Hypothesis 2: Timeout caused by network connectivity issues. Test: Check network latency and packet loss",
  thoughtNumber: 3,
  totalThoughts: 6,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Identify root cause of API timeout issues",
    pattern: "P2",
    hypothesisState: "proposed",
    testPlan: "Network diagnostics"
  }
});

// Step 5: Test and confirm
// Execute: Network connectivity tests
const networkTest = await execute_command({
  command: "ping -c 10 api.endpoint.com",
});

sequentialthinking({
  thought: "Network test: 2% packet loss, 150ms latency. Within acceptable range. Hypothesis 2 FALSIFIED",
  thoughtNumber: 4,
  totalThoughts: 6,
  isRevision: true,
  revisesThought: 3,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Identify root cause of API timeout issues",
    pattern: "P2",
    hypothesisState: "falsified",
    evidenceRefs: ["cmd:network_ping_test"]
  }
});

// Step 6: Final hypothesis and validation
sequentialthinking({
  thought: "Hypothesis 3: Timeout caused by thread pool exhaustion. Test: Monitor thread pool usage",
  thoughtNumber: 5,
  totalThoughts: 6,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Identify root cause of API timeout issues",
    pattern: "P2",
    hypothesisState: "proposed",
    testPlan: "Thread pool monitoring"
  }
});

// Step 7: Confirm root cause
const threadMetrics = await execute_command({
  command: "jstack -l <pid> | grep 'pool-' | wc -l",
});

sequentialthinking({
  thought: "Thread pool at 95% capacity during timeouts. Root cause CONFIRMED: thread pool exhaustion",
  thoughtNumber: 6,
  totalThoughts: 6,
  nextThoughtNeeded: false,
  metadata: {
    goal: "Identify root cause of API timeout issues",
    pattern: "P2",
    hypothesisState: "confirmed",
    decision: "Thread pool exhaustion causing timeouts",
    evidenceRefs: ["cmd:thread_pool_monitoring"],
    fixRecommendation: "Increase thread pool size or implement queuing"
  }
});
```

**Memory Persistence**:
- Creates `reasoning#run#<id>#<sha8>#timeout_debug` entity
- Links `FALSIFIES err#api_timeout` for DB and network hypotheses
- Links `VALIDATES fix#increase_thread_pool` for confirmed solution

## Example 2: P3 Spec Refiner - UI Component Requirements

**Scenario**: "Build a responsive button component" - ambiguous requirements need clarification.

**Reasoning Chain**:

```javascript
// Step 1: Identify ambiguities
sequentialthinking({
  thought: "Ambiguity 1: 'Responsive' undefined. Options: mobile-first, breakpoint-based, fluid scaling",
  thoughtNumber: 1,
  totalThoughts: 5,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Clarify button component requirements",
    pattern: "P3",
    ambiguityDebt: 6,
    threshold: 1
  }
});

// Step 2: Propose clarification
sequentialthinking({
  thought: "Proposal: Mobile-first responsive with breakpoints at 640px, 768px, 1024px, 1280px",
  thoughtNumber: 2,
  totalThoughts: 5,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Clarify button component requirements",
    pattern: "P3",
    ambiguityDebt: 5,
    clarification: "responsive_breakpoints_defined"
  }
});

// Step 3: Check for more ambiguities
sequentialthinking({
  thought: "Ambiguity 2: 'Button' variants undefined. Primary, secondary, outline, ghost?",
  thoughtNumber: 3,
  totalThoughts: 5,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Clarify button component requirements",
    pattern: "P3",
    ambiguityDebt: 4,
    currentFocus: "button_variants"
  }
});

// Step 4: Stakeholder validation
// Simulate stakeholder feedback
const stakeholderFeedback = "Breakpoints good, but need loading states and icon support";

sequentialthinking({
  thought: "Stakeholder feedback: Breakpoints approved, but add loading spinner and icon support",
  thoughtNumber: 4,
  totalThoughts: 5,
  isRevision: true,
  revisesThought: 3,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Clarify button component requirements",
    pattern: "P3",
    ambiguityDebt: 2,
    revisions: ["add_loading_states", "add_icon_support"]
  }
});

// Step 5: Final specification
sequentialthinking({
  thought: "Final spec: Responsive button (640px,768px,1024px,1280px) with variants (primary,secondary,outline,ghost), loading states, and icon support",
  thoughtNumber: 5,
  totalThoughts: 5,
  nextThoughtNeeded: false,
  metadata: {
    goal: "Clarify button component requirements",
    pattern: "P3",
    ambiguityDebt: 0,
    decision: "Complete button specification",
    finalRequirements: ["responsive_breakpoints", "button_variants", "loading_states", "icon_support"]
  }
});
```

**Memory Persistence**:
- Creates `reasoning#run#<id>#<sha8>#button_spec` entity
- Links to design system documentation
- Enables future component creation to reference clarified requirements

## Example 3: P1 Receding-Horizon Planner - System Migration

**Scenario**: Migrate legacy authentication system to JWT-based auth. Unknown scope.

**Reasoning Chain**:

```javascript
// Step 1: Initial scope assessment
sequentialthinking({
  thought: "Step 1: Identify migration scope - Legacy system has 15 auth endpoints, 3 client apps, 2 databases",
  thoughtNumber: 1,
  totalThoughts: 4,  // Conservative estimate
  nextThoughtNeeded: true,
  metadata: {
    goal: "Plan JWT authentication system migration",
    pattern: "P1",
    constraints: ["time<=2weeks", "zero_downtime"],
    initialScope: "15_endpoints_3_clients_2_dbs"
  }
});

// Step 2: Risk assessment
sequentialthinking({
  thought: "Step 2: High-risk areas identified - Session migration, client token refresh, rollback strategy",
  thoughtNumber: 2,
  totalThoughts: 4,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Plan JWT authentication system migration",
    pattern: "P1",
    risks: ["session_migration", "token_refresh", "rollback_complexity"]
  }
});

// Step 3: Adjust planning horizon
sequentialthinking({
  thought: "Step 3: Scope expanded - Need parallel systems for 5 days, gradual rollout, comprehensive testing. Total steps: 12",
  thoughtNumber: 3,
  totalThoughts: 12,  // Adjust based on evidence
  nextThoughtNeeded: true,
  metadata: {
    goal: "Plan JWT authentication system migration",
    pattern: "P1",
    adjustedScope: "parallel_system_5days_gradual_rollout",
    totalSteps: 12
  }
});

// Step 4: Phase planning
sequentialthinking({
  thought: "Step 4: Phase 1 (Days 1-2): JWT service setup, Phase 2 (Days 3-4): Parallel operation, Phase 3 (Day 5): Cutover",
  thoughtNumber: 4,
  totalThoughts: 12,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Plan JWT authentication system migration",
    pattern: "P1",
    phases: ["jwt_service_setup", "parallel_operation", "cutover"],
    timeline: "5_days_total"
  }
});

// Continue with detailed planning...
sequentialthinking({
  thought: "Step 8: Database migration strategy - Dual writes for 48 hours, validate data consistency",
  thoughtNumber: 8,
  totalThoughts: 12,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Plan JWT authentication system migration",
    pattern: "P1",
    currentPhase: "database_migration",
    strategy: "dual_writes_48h"
  }
});

// Step 12: Final migration plan
sequentialthinking({
  thought: "Step 12: Complete migration plan with rollback procedures, monitoring, and go/no-go criteria",
  thoughtNumber: 12,
  totalThoughts: 12,
  nextThoughtNeeded: false,
  metadata: {
    goal: "Plan JWT authentication system migration",
    pattern: "P1",
    decision: "Migration plan complete",
    deliverables: ["jwt_service", "migration_scripts", "rollback_plan", "monitoring_dashboard"],
    confidence: 90
  }
});
```

**Memory Persistence**:
- Creates `reasoning#run#<id>#<sha8>#auth_migration` entity
- Links to migration patterns from similar projects
- Provides template for future system migrations

## Example 4: P9 Evaluation Harness - Performance Optimization

**Scenario**: Optimize React component render performance. Need measurable improvement.

**Reasoning Chain**:

```javascript
// Step 1: Establish baseline
const baselineProfile = await execute_command({
  command: "react-devtools profile Component",
});

sequentialthinking({
  thought: "Baseline: Component renders in 45ms, re-renders on every prop change. Target: <15ms with stable props",
  thoughtNumber: 1,
  totalThoughts: 6,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Optimize React component performance",
    pattern: "P9",
    baselineMetric: 45,
    targetMetric: 15,
    unit: "milliseconds"
  }
});

// Step 2: Test optimization A - React.memo
const memoResult = await execute_command({
  command: "react-devtools profile MemoizedComponent",
});

sequentialthinking({
  thought: "Candidate A (React.memo): 28ms render time (37% improvement). Still above target",
  thoughtNumber: 2,
  totalThoughts: 6,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Optimize React component performance",
    pattern: "P9",
    candidate: "react_memo",
    score: 28,
    improvement: 37.8
  }
});

// Step 3: Test optimization B - useMemo for expensive calculations
const useMemoResult = await execute_command({
  command: "react-devtools profile UseMemoComponent",
});

sequentialthinking({
  thought: "Candidate B (useMemo): 12ms render time (73% improvement). Meets target!",
  thoughtNumber: 3,
  totalThoughts: 6,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Optimize React component performance",
    pattern: "P9",
    candidate: "useMemo_optimization",
    score: 12,
    improvement: 73.3
  }
});

// Step 4: Test combination A + B
const combinedResult = await execute_command({
  command: "react-devtools profile CombinedOptimizationComponent",
});

sequentialthinking({
  thought: "Candidate C (memo + useMemo): 10ms render time (77% improvement). Best result so far",
  thoughtNumber: 4,
  totalThoughts: 6,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Optimize React component performance",
    pattern: "P9",
    candidate: "memo_plus_usememo",
    score: 10,
    improvement: 77.8
  }
});

// Step 5: Regression testing
const regressionTest = await execute_command({
  command: "npm test -- --testPathPattern=Component",
});

sequentialthinking({
  thought: "Regression test: All tests pass. No functionality broken by optimizations",
  thoughtNumber: 5,
  totalThoughts: 6,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Optimize React component performance",
    pattern: "P9",
    regressionStatus: "passed",
    testCoverage: "component_tests_all_green"
  }
});

// Step 6: Final decision
sequentialthinking({
  thought: "Winner: React.memo + useMemo combination (10ms, 77% improvement). Meets target with no regressions",
  thoughtNumber: 6,
  totalThoughts: 6,
  nextThoughtNeeded: false,
  metadata: {
    goal: "Optimize React component performance",
    pattern: "P9",
    decision: "Combined memo and useMemo optimization",
    winner: "memo_plus_usememo",
    finalScore: 10,
    improvement: 77.8,
    confidence: 95
  }
});
```

**Memory Persistence**:
- Creates `reasoning#run#<id>#<sha8>#react_perf_opt` entity
- Links `EVALUATES candidate#react_memo`, `EVALUATES candidate#useMemo`, etc.
- Provides optimization template for similar performance issues

## Example 5: P6 Threat-Model / Risk Review - API Security

**Scenario**: Security review of new payment API endpoint.

**Reasoning Chain**:

```javascript
// Step 1: Asset identification
sequentialthinking({
  thought: "Asset: Payment processing endpoint handling credit card data. Threat: Unauthorized access via API key exposure",
  thoughtNumber: 1,
  totalThoughts: 8,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Complete security threat model for payment API",
    pattern: "P6",
    assets: ["payment_endpoint", "credit_card_data"],
    threats: ["api_key_exposure"]
  }
});

// Step 2: Branch mitigation options
sequentialthinking({
  thought: "Branch A: API key rotation every 24h. Security: High, Complexity: Medium",
  thoughtNumber: 2,
  totalThoughts: 8,
  branchFromThought: 1,
  branchId: "key_rotation_24h",
  nextThoughtNeeded: true,
  metadata: {
    goal: "Complete security threat model for payment API",
    pattern: "P6",
    mitigation: "api_key_rotation",
    securityScore: 8,
    implementationCost: "medium",
    operationalImpact: "key_management_overhead"
  }
});

// Step 3: Alternative mitigation
sequentialthinking({
  thought: "Branch B: OAuth 2.0 with short-lived tokens. Security: Very High, Complexity: High",
  thoughtNumber: 3,
  totalThoughts: 8,
  branchFromThought: 1,
  branchId: "oauth2_tokens",
  nextThoughtNeeded: true,
  metadata: {
    goal: "Complete security threat model for payment API",
    pattern: "P6",
    mitigation: "oauth2_short_lived_tokens",
    securityScore: 9,
    implementationCost: "high",
    operationalImpact: "complex_integration"
  }
});

// Step 4: Risk assessment
sequentialthinking({
  thought: "Risk evaluation: API key exposure likelihood: Medium, Impact: Critical. Need strong mitigation",
  thoughtNumber: 4,
  totalThoughts: 8,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Complete security threat model for payment API",
    pattern: "P6",
    riskLikelihood: "medium",
    riskImpact: "critical",
    riskLevel: "high"
  }
});

// Step 5: Mitigation selection
sequentialthinking({
  thought: "Selected: OAuth 2.0 with JWT tokens. Balances security needs with implementation cost",
  thoughtNumber: 5,
  totalThoughts: 8,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Complete security threat model for payment API",
    pattern: "P6",
    selectedMitigation: "oauth2_jwt",
    rationale: "Security first for payment data",
    tradeoffsAccepted: ["higher_complexity"]
  }
});

// Step 6: Implementation planning
sequentialthinking({
  thought: "Implementation: Auth server setup, token validation middleware, client integration guide",
  thoughtNumber: 6,
  totalThoughts: 8,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Complete security threat model for payment API",
    pattern: "P6",
    implementationSteps: ["auth_server", "middleware", "client_guide"]
  }
});

// Step 7: Monitoring and response
sequentialthinking({
  thought: "Monitoring: Failed auth attempts, token expiration tracking, security event logging",
  thoughtNumber: 7,
  totalThoughts: 8,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Complete security threat model for payment API",
    pattern: "P6",
    monitoring: ["failed_auth", "token_tracking", "security_events"]
  }
});

// Step 8: Final threat model
sequentialthinking({
  thought: "Complete threat model: Payment API secured with OAuth 2.0, monitoring active, incident response defined",
  thoughtNumber: 8,
  totalThoughts: 8,
  nextThoughtNeeded: false,
  metadata: {
    goal: "Complete security threat model for payment API",
    pattern: "P6",
    decision: "Threat model complete with OAuth 2.0 implementation",
    residualRisk: "low",
    confidence: 85
  }
});
```

**Memory Persistence**:
- Creates `reasoning#run#<id>#<sha8>#payment_api_security` entity
- Links `MITIGATES threat#api_key_exposure` with selected OAuth solution
- Provides security review template for future APIs

These examples demonstrate how Sequential Thinking patterns create structured, auditable reasoning processes that integrate deeply with the Memory MCP for continuous learning and improvement.