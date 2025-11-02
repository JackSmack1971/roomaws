# 30-common-patterns.md
> Complete implementations of Sequential Thinking patterns P1-P10 with mode-specific adaptations.

## P1 — Receding-Horizon Planner

**Use when:** Large tasks with unknown scope (research, system design, complex refactoring).

**Implementation:**
```javascript
// Initialize with conservative estimate
sequentialthinking({
  thought: "Step 1: Break down the large task into initial manageable chunks",
  thoughtNumber: 1,
  totalThoughts: 5,  // Start low, will adjust
  nextThoughtNeeded: true,
  metadata: {
    goal: "Complete complex multi-phase task",
    pattern: "P1",
    constraints: ["time<=2h", "scope=unknown"]
  }
})

// After assessment, adjust horizon
sequentialthinking({
  thought: "Step 2: Scope assessment complete. This requires 12 steps total. Next: Phase 1 planning",
  thoughtNumber: 2,
  totalThoughts: 12,  // Adjust based on evidence
  nextThoughtNeeded: true,
  metadata: {
    goal: "Complete complex multi-phase task",
    pattern: "P1",
    evidenceRefs: ["scope_assessment_obs"],
    constraints: ["time<=2h", "scope=assessed"]
  }
})
```

**Memory Integration:**
- Query: `type:ReasoningChain pattern:P1 <task_domain>`
- Persist: Chain with adaptive planning decisions
- Learn: Effective horizon adjustment patterns

## P2 — Hypothesis-Test Loop

**Use when:** Debugging, root-cause analysis, benchmark regressions.

**Implementation:**
```javascript
// Form initial hypothesis
sequentialthinking({
  thought: "Hypothesis 1: Timeout caused by network latency. Test: Measure response times",
  thoughtNumber: 1,
  totalThoughts: 8,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Identify root cause of performance issue",
    pattern: "P2",
    hypothesisState: "proposed",
    testPlan: "Network latency measurement"
  }
})

// Test and evaluate
sequentialthinking({
  thought: "Test result: Network latency within normal range (50ms). Hypothesis 1 FALSIFIED.",
  thoughtNumber: 2,
  totalThoughts: 8,
  isRevision: true,
  revisesThought: 1,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Identify root cause of performance issue",
    pattern: "P2",
    hypothesisState: "falsified",
    evidenceRefs: ["network_latency_test"],
    contradictions: ["latency_normal_but_timeout_occurs"]
  }
})

// Form new hypothesis
sequentialthinking({
  thought: "Hypothesis 2: Timeout caused by database connection pool exhaustion",
  thoughtNumber: 3,
  totalThoughts: 8,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Identify root cause of performance issue",
    pattern: "P2",
    hypothesisState: "proposed",
    testPlan: "Check connection pool metrics"
  }
})
```

**Memory Integration:**
- Query: `type:ReasoningChain pattern:P2 <error_type>`
- Relations: `FALSIFIES err#<normalized_key>`, `VALIDATES fix#<strategy>`
- Learn: Common falsification patterns, effective test designs

## P3 — Spec Refiner (Source-Spec First)

**Use when:** Requirements/spec writing before code, ambiguity reduction.

**Implementation:**
```javascript
// Identify ambiguities
sequentialthinking({
  thought: "Ambiguity 1: 'Responsive' undefined. Options: mobile-first, breakpoints, fluid design",
  thoughtNumber: 1,
  totalThoughts: 6,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Eliminate design specification ambiguities",
    pattern: "P3",
    ambiguityDebt: 8,
    threshold: 2
  }
})

// Propose clarification
sequentialthinking({
  thought: "Proposal: Define responsive as mobile-first with breakpoints at 768px, 1024px, 1440px",
  thoughtNumber: 2,
  totalThoughts: 6,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Eliminate design specification ambiguities",
    pattern: "P3",
    ambiguityDebt: 7,
    clarification: "responsive_breakpoints"
  }
})

// Validate with stakeholders
sequentialthinking({
  thought: "Stakeholder feedback: Breakpoints accepted, but need fluid typography spec",
  thoughtNumber: 3,
  totalThoughts: 6,
  isRevision: true,
  revisesThought: 2,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Eliminate design specification ambiguities",
    pattern: "P3",
    ambiguityDebt: 6,
    revisions: ["add_fluid_typography"]
  }
})
```

**Memory Integration:**
- Query: `type:ReasoningChain pattern:P3 <domain>_specs`
- Persist: Ambiguity patterns, successful clarification strategies
- Learn: Common specification gaps, effective clarification approaches

## P4 — Research Sprint Orchestrator

**Use when:** Multi-source desk research, literature reviews, API evaluations.

**Implementation:**
```javascript
// Plan research sources
sequentialthinking({
  thought: "Step 1: Identify 5 authoritative sources for React state management comparison",
  thoughtNumber: 1,
  totalThoughts: 8,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Compare React state management solutions",
    pattern: "P4",
    sourcesPlanned: ["react_docs", "redux_docs", "zustand_docs", "jotai_docs", "valtio_docs"]
  }
})

// Execute research phase
sequentialthinking({
  thought: "Step 2: Researched Zustand - lightweight, 1.1kB, TypeScript-first, no boilerplate",
  thoughtNumber: 2,
  totalThoughts: 8,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Compare React state management solutions",
    pattern: "P4",
    sourcesCompleted: ["zustand_docs"],
    findings: ["lightweight", "typescript_first"]
  }
})

// Synthesize findings
sequentialthinking({
  thought: "Step 4: Synthesis - Zustand best for small apps, Redux for complex state, Jotai for atomic updates",
  thoughtNumber: 4,
  totalThoughts: 8,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Compare React state management solutions",
    pattern: "P4",
    synthesisComplete: true,
    recommendations: ["zustand_small", "redux_complex", "jotai_atomic"]
  }
})
```

**Memory Integration:**
- Query: `type:ReasoningChain pattern:P4 <research_domain>`
- Relations: `REFERENCES doc#<source>`, `PRODUCES concept#<synthesis>`
- Learn: Effective source selection, synthesis methodologies

## P5 — TDD Builder

**Use when:** New features/bugfixes with test-driven development.

**Implementation:**
```javascript
// Define acceptance criteria
sequentialthinking({
  thought: "Step 1: Acceptance test - User can filter products by price range $10-50",
  thoughtNumber: 1,
  totalThoughts: 7,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Implement product filtering feature",
    pattern: "P5",
    acceptanceTests: ["filter_by_price_range"]
  }
})

// Write failing test
sequentialthinking({
  thought: "Step 2: Test written and failing: filterProducts() returns unfiltered list",
  thoughtNumber: 2,
  totalThoughts: 7,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Implement product filtering feature",
    pattern: "P5",
    testState: "red",
    testFailure: "returns_unfiltered"
  }
})

// Implement minimal pass
sequentialthinking({
  thought: "Step 3: Implemented basic filter - test passes for price range filtering",
  thoughtNumber: 3,
  totalThoughts: 7,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Implement product filtering feature",
    pattern: "P5",
    testState: "green",
    implementation: "basic_price_filter"
  }
})

// Refactor and expand
sequentialthinking({
  thought: "Step 5: Refactored to support multiple filters (price, category, rating)",
  thoughtNumber: 5,
  totalThoughts: 7,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Implement product filtering feature",
    pattern: "P5",
    testState: "green",
    refactoring: "multi_criteria_filter"
  }
})
```

**Memory Integration:**
- Query: `type:ReasoningChain pattern:P5 <feature_domain>`
- Relations: `PRODUCES fix#<feature>`, `VALIDATES test#<acceptance>`
- Learn: Effective test design patterns, refactoring triggers

## P6 — Threat-Model / Risk Review

**Use when:** Security, safety, or policy gate reviews.

**Implementation:**
```javascript
// Enumerate assets and threats
sequentialthinking({
  thought: "Step 1: Asset identified - User authentication tokens. Threat - XSS via malicious input",
  thoughtNumber: 1,
  totalThoughts: 10,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Complete security threat model for user authentication",
    pattern: "P6",
    assetsCatalogued: 1,
    threatsIdentified: 1
  }
})

// Branch mitigation options
sequentialthinking({
  thought: "Branch A: HttpOnly cookies - High security, breaks SPA auth requirements",
  thoughtNumber: 3,
  totalThoughts: 10,
  branchFromThought: 2,
  branchId: "mitigation-httponly",
  nextThoughtNeeded: true,
  metadata: {
    goal: "Complete security threat model for user authentication",
    pattern: "P6",
    securityScore: 9,
    implementationCost: "medium",
    userImpact: "breaking"
  }
})

// Evaluate trade-offs
sequentialthinking({
  thought: "Step 6: Mitigation selected - JWT with httpOnly refresh token + localStorage access token",
  thoughtNumber: 6,
  totalThoughts: 10,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Complete security threat model for user authentication",
    pattern: "P6",
    selectedMitigation: "hybrid_jwt_strategy",
    tradeoffsBalanced: true
  }
})
```

**Memory Integration:**
- Query: `type:ReasoningChain pattern:P6 <security_domain>`
- Relations: `MITIGATES threat#<type>`, `ABOUT asset#<type>`
- Learn: Common threat patterns, effective mitigation strategies

## P7 — ADR/Decision Logger

**Use when:** Architecture decisions that must be revisitable.

**Implementation:**
```javascript
// Frame the decision
sequentialthinking({
  thought: "Step 1: Decision required - Choose between GraphQL and REST for new API",
  thoughtNumber: 1,
  totalThoughts: 5,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Document API architecture decision",
    pattern: "P7",
    options: ["graphql", "rest"],
    criteria: ["developer_experience", "performance", "learning_curve"]
  }
})

// Branch evaluation
sequentialthinking({
  thought: "Branch: GraphQL option - Better DX, complex caching, steeper learning curve",
  thoughtNumber: 2,
  totalThoughts: 5,
  branchFromThought: 1,
  branchId: "option-graphql",
  nextThoughtNeeded: true,
  metadata: {
    goal: "Document API architecture decision",
    pattern: "P7",
    option: "graphql",
    pros: ["better_dx", "flexible_queries"],
    cons: ["complex_caching", "steep_learning"]
  }
})

// Converge on decision
sequentialthinking({
  thought: "Decision: Choose GraphQL for better developer experience and future flexibility",
  thoughtNumber: 4,
  totalThoughts: 5,
  nextThoughtNeeded: false,
  metadata: {
    goal: "Document API architecture decision",
    pattern: "P7",
    decision: "graphql_selected",
    rationale: "DX and flexibility outweigh complexity concerns",
    confidence: 85
  }
})
```

**Memory Integration:**
- Query: `type:ReasoningChain pattern:P7 <architecture_domain>`
- Relations: `PRODUCES adr#<decision>`, `DERIVED_FROM doc#<context>`
- Learn: Decision patterns, criteria weighting, option evaluation

## P8 — Agent-to-Agent Relay (Coordinator Pattern)

**Use when:** A lead agent sequences specialists.

**Implementation:**
```javascript
// Plan handoff
sequentialthinking({
  thought: "Step 1: Coordinator analysis complete. Handoff to design-engineer for UI implementation",
  thoughtNumber: 1,
  totalThoughts: 6,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Coordinate multi-agent feature implementation",
    pattern: "P8",
    nextAgent: "design-engineer",
    handoffContract: "ui_spec_complete",
    acceptanceCriteria: ["components_implemented", "responsive_design"]
  }
})

// Monitor progress
sequentialthinking({
  thought: "Step 3: Design-engineer completed components. Handoff to test mode for validation",
  thoughtNumber: 3,
  totalThoughts: 6,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Coordinate multi-agent feature implementation",
    pattern: "P8",
    agentProgress: "design-engineer:complete",
    nextAgent: "test",
    handoffData: "component_files"
  }
})

// Verify completion
sequentialthinking({
  thought: "Step 5: All agents completed successfully. Feature ready for integration",
  thoughtNumber: 5,
  totalThoughts: 6,
  nextThoughtNeeded: false,
  metadata: {
    goal: "Coordinate multi-agent feature implementation",
    pattern: "P8",
    decision: "feature_complete",
    agentChain: ["orchestrator", "design-engineer", "test"]
  }
})
```

**Memory Integration:**
- Query: `type:ReasoningChain pattern:P8 <coordination_type>`
- Relations: `SEQUENCES mode#<agent>`, `PRODUCES handoff#<contract>`
- Learn: Effective agent sequencing, handoff patterns

## P9 — Evaluation Harness (Self-Critique/Compare)

**Use when:** You need measurable improvement (optimization, A/B testing).

**Implementation:**
```javascript
// Establish baseline
sequentialthinking({
  thought: "Step 1: Baseline measured - API response time: 850ms, target: <200ms",
  thoughtNumber: 1,
  totalThoughts: 7,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Optimize API response time",
    pattern: "P9",
    baselineMetric: 850,
    targetMetric: 200,
    unit: "milliseconds"
  }
})

// Test candidate A
sequentialthinking({
  thought: "Step 2: Candidate A (caching) result: 180ms improvement (78.8% faster)",
  thoughtNumber: 2,
  totalThoughts: 7,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Optimize API response time",
    pattern: "P9",
    candidate: "caching",
    score: 180,
    improvement: 78.8
  }
})

// Test candidate B
sequentialthinking({
  thought: "Step 3: Candidate B (query optimization) result: 420ms (50.6% faster)",
  thoughtNumber: 3,
  totalThoughts: 7,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Optimize API response time",
    pattern: "P9",
    candidate: "query_optimization",
    score: 420,
    improvement: 50.6
  }
})

// Select winner
sequentialthinking({
  thought: "Step 4: Winner selected - Caching (180ms) outperforms query optimization (420ms)",
  thoughtNumber: 4,
  totalThoughts: 7,
  nextThoughtNeeded: false,
  metadata: {
    goal: "Optimize API response time",
    pattern: "P9",
    decision: "caching_selected",
    winner: "caching",
    score: 180,
    improvement: 78.8
  }
})
```

**Memory Integration:**
- Query: `type:ReasoningChain pattern:P9 <optimization_domain>`
- Relations: `EVALUATES candidate#<option>`, `PRODUCES metric#<result>`
- Learn: Effective evaluation rubrics, comparison methodologies

## P10 — Postmortem Generator

**Use when:** Incidents/build failures, structured root cause analysis.

**Implementation:**
```javascript
// Collect timeline
sequentialthinking({
  thought: "Step 1: Timeline established - Deploy at 14:00, errors at 14:15, rollback at 14:30",
  thoughtNumber: 1,
  totalThoughts: 8,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Generate postmortem for deployment failure",
    pattern: "P10",
    timelineEvents: ["deploy_14:00", "errors_14:15", "rollback_14:30"]
  }
})

// Cluster causes
sequentialthinking({
  thought: "Step 2: Causes clustered - Primary: DB migration timeout, Secondary: Insufficient testing",
  thoughtNumber: 2,
  totalThoughts: 8,
  nextThoughtNeeded: true,
  metadata: {
    goal: "Generate postmortem for deployment failure",
    pattern: "P10",
    primaryCause: "db_migration_timeout",
    secondaryCauses: ["insufficient_testing"]
  }
})

// Branch corrective actions
sequentialthinking({
  thought: "Branch A: Action - Add migration dry-run in CI, Owner: DevOps team",
  thoughtNumber: 4,
  totalThoughts: 8,
  branchFromThought: 3,
  branchId: "action-migration-testing",
  nextThoughtNeeded: true,
  metadata: {
    goal: "Generate postmortem for deployment failure",
    pattern: "P10",
    action: "migration_dry_run_ci",
    owner: "devops_team",
    impact: "prevents_future_migration_failures"
  }
})

// Finalize RCA
sequentialthinking({
  thought: "Step 7: RCA complete - Migration timeout due to large dataset, fixed with batching and testing",
  thoughtNumber: 7,
  totalThoughts: 8,
  nextThoughtNeeded: false,
  metadata: {
    goal: "Generate postmortem for deployment failure",
    pattern: "P10",
    decision: "rca_complete",
    rootCause: "large_dataset_migration_timeout",
    fixes: ["batch_migrations", "add_migration_testing"],
    owners: ["devops_team", "backend_team"]
  }
})
```

**Memory Integration:**
- Query: `type:ReasoningChain pattern:P10 <incident_type>`
- Relations: `ANALYZES incident#<id>`, `PRODUCES rca#<findings>`, `RECOMMENDS fix#<action>`
- Learn: Common incident patterns, effective postmortem structures