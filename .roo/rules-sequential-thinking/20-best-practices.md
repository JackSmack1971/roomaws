# 20-best-practices.md
> Guidelines and conventions for effective Sequential Thinking implementation.

## Pattern Selection Guidelines

### Choose the Right Pattern (P1-P10)
- **P1 (Receding-Horizon Planner)**: Unknown scope, adaptive planning needed
- **P2 (Hypothesis-Test Loop)**: Debugging, RCA, validation testing
- **P3 (Spec Refiner)**: Requirements clarification, ambiguity reduction
- **P4 (Research Sprint Orchestrator)**: Multi-source research, synthesis
- **P5 (TDD Builder)**: Feature development with test-first approach
- **P6 (Threat-Model / Risk Review)**: Security, safety, policy reviews
- **P7 (ADR/Decision Logger)**: Architecture decisions needing audit trail
- **P8 (Agent-to-Agent Relay)**: Multi-agent coordination
- **P9 (Evaluation Harness)**: Optimization, A/B comparison
- **P10 (Postmortem Generator)**: Incident analysis, RCA

### Pattern Anti-Patterns
- Don't use P2 for simple lookups (use direct search)
- Don't use P1 for well-understood tasks (use checklists)
- Don't use P9 for subjective decisions (use explicit rubrics)

## Step Construction Best Practices

### Thought Content Guidelines
- **Compact**: ≤ 8 lines, focus on key insight or action
- **Actionable**: Each thought should advance the reasoning
- **Evidence-Based**: Reference specific observations or facts
- **Hypothesis-Driven**: When testing, state clear falsification criteria

### Metadata Usage
- **goal**: One-line objective for the entire chain
- **evidenceRefs**: ULID-style references to observations/docs
- **constraints**: Time, token, or resource limits
- **decision**: Only set in terminal thoughts

## Branching and Revision Control

### When to Branch
- **Genuine Alternatives**: Different solution approaches
- **Risk Assessment**: High-uncertainty decisions
- **Exploratory**: Understanding option trade-offs

### When NOT to Branch
- **Minor Variations**: Slight parameter changes
- **Sequential Dependencies**: One approach must precede another
- **Resource Exhaustion**: When hitting branch limits

### Branch Management
- **Limit Concurrent Branches**: Maximum 3 active branches
- **Clear Branch IDs**: Descriptive names (e.g., "optimistic-path", "conservative-path")
- **Merge Criteria**: Evidence strength, consistency, resource cost
- **Abandon Branches**: When falsified or dominated by better alternatives

## Evidence Quality Standards

### Evidence Hierarchy
1. **Primary Sources**: Direct observations, test results, code analysis
2. **Secondary Sources**: Historical patterns, documentation
3. **Tertiary Sources**: Analogous cases, expert opinion

### Evidence Validation
- **Reproducibility**: Can the evidence be gathered again?
- **Relevance**: Directly supports or falsifies the hypothesis?
- **Recency**: Is the evidence still valid?
- **Independence**: Not circularly dependent on the conclusion?

## Decision Convergence

### Convergence Signals
- **Evidence Saturation**: Additional evidence doesn't change confidence
- **Contradiction Resolution**: All major objections addressed
- **Resource Limits**: Time/budget constraints reached
- **Sufficient Confidence**: >80% confidence threshold met

### Premature Convergence (Avoid)
- **Confirmation Bias**: Only seeking supporting evidence
- **Authority Bias**: Accepting without verification
- **Sunk Cost**: Continuing flawed paths due to invested effort

## Memory Integration Patterns

### Observation Linking
- **reasoning.step**: Each thought becomes a step entity
- **reasoning.chain**: Complete chain with outcome
- **reasoning.revision**: When hypotheses are falsified

### Relation Patterns
- **BELONGS_TO**: Steps belong to chains
- **DERIVES_FROM**: Sequential progression
- **REVISES**: Corrections of previous thoughts
- **BRANCHES_FROM**: Alternative paths
- **REFERENCES**: Evidence sources
- **VALIDATES/FALSIFIES**: Hypothesis testing outcomes

## Error Recovery and Degradation

### Chain Recovery
- **Stuck Chains**: Force convergence with best available evidence
- **Failed Branches**: Mark as abandoned with reason
- **Incomplete Chains**: Save partial progress for resumption

### MCP Degradation
- **Memory Unavailable**: Continue with local reasoning state
- **Sequential Thinking Unavailable**: Fall back to linear reasoning
- **Partial Failures**: Degrade gracefully, preserve what works

## Performance Optimization

### Chain Efficiency
- **Early Termination**: Stop when decision criteria met
- **Batch Evidence Gathering**: Group related information requests
- **Parallel Branches**: When branches are independent
- **Incremental Persistence**: Save progress without full chain completion

### Resource Management
- **Token Budgeting**: Allocate tokens across chain steps
- **Time Boxing**: Set time limits per phase
- **Evidence Caching**: Reuse evidence across branches
- **Pruning**: Remove dominated or falsified branches early

## Quality Assurance

### Chain Validation Checklist
- [ ] Pattern appropriate for task type
- [ ] All hypotheses tested with evidence
- [ ] Revisions properly linked to originals
- [ ] Branches merged or explicitly handled
- [ ] Decision supported by evidence strength
- [ ] Memory entities created and linked
- [ ] Chain outcome clearly stated

### Continuous Improvement
- **Success Metrics**: Track decision accuracy, time to conclusion
- **Pattern Effectiveness**: Monitor which patterns work for which tasks
- **Failure Analysis**: Review stuck/incomplete chains for improvement
- **Evidence Quality**: Assess evidence reliability over time