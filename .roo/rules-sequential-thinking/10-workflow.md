# 10-workflow.md
> Canonical workflow: Step-by-step reasoning process using Sequential Thinking patterns with Memory MCP integration.

## Phase 0: Memory Consultation + Pattern Selection (MANDATORY)

**Objective**: Leverage historical reasoning patterns before starting new chains.

**Steps**:
1. **Extract task signature**: Analyze problem type, complexity, and domain
2. **Query memory for reasoning chains**:
   ```javascript
   use_mcp_tool({
     server_name: "memory",
     tool_name: "search_nodes",
     arguments: {
       query: "type:ReasoningChain <task_domain> <problem_type>",
       limit: 3
     }
   })
   ```
3. **Query memory for outcomes**: Get historical success patterns
4. **Select Sequential Thinking pattern** (P1-P10) based on task analysis:
   - **Planning/Design**: P1 (Receding-Horizon Planner)
   - **Debugging/RCA**: P2 (Hypothesis-Test Loop)
   - **Requirements**: P3 (Spec Refiner)
   - **Research**: P4 (Research Sprint Orchestrator)
   - **TDD**: P5 (TDD Builder)
   - **Security**: P6 (Threat-Model / Risk Review)
   - **Decisions**: P7 (ADR/Decision Logger)
   - **Coordination**: P8 (Agent-to-Agent Relay)
   - **Optimization**: P9 (Evaluation Harness)
   - **Incidents**: P10 (Postmortem Generator)
5. **Initialize Sequential Thinking** with selected pattern

6. **Query external evidence (CONDITIONAL)**:

    IF hypothesis requires external validation:

    A. **Technical documentation validation** (Exa):
    ```javascript
    use_mcp_tool({
      server_name: "exa",
      tool_name: "get_code_context_exa",
      arguments: {
        query: "<library> <API/concept> behavior",
        tokensNum: 5000
      }
    })
    ```

    B. **Research synthesis** (Perplexity):
    ```javascript
    use_mcp_tool({
      server_name: "perplexity",
      tool_name: "perplexity_research",
      arguments: {
        messages: [{
          role: "user",
          content: "Research: <hypothesis to validate>"
        }]
      }
    })
    ```

    C. **Domain-specific search** (Exa):
    ```javascript
    use_mcp_tool({
      server_name: "exa",
      tool_name: "web_search_exa",
      arguments: {
        query: "<specific_pattern>",
        numResults: 3
      }
    })

7. **Document evidence consultation**:
```
✓ Memory consulted: [N results | No matches | MCP unavailable]
✓ External evidence: [exa:M docs | perplexity:P citations | none needed]
✓ Validation strategy: [code_context | research_synthesis | domain_search]
✓ Confidence: [High/Medium/Low + rationale]
```

## Evidence Gathering Principles

When Sequential Thinking identifies knowledge gaps:

1. **Precision First (Exa)**:
  - Use when you need EXACT API documentation
  - Use when searching for working code examples
  - Use with domain filters for authoritative sources only

2. **Synthesis Second (Perplexity)**:
  - Use when you need cross-validated research
  - Use when synthesizing multiple perspectives
  - Use when you need reasoning-backed recommendations

3. **Triangulation**:
  - Compare: Memory patterns vs Exa docs vs Perplexity synthesis
  - Flag: Contradictions between sources
  - Resolve: Use evidence quality and recency as tiebreakers

## Phase 1: Reasoning Chain Execution

**Coordinator Loop** (adapted from sequential-thinking-mcp.md):

1. **Plan step** → Call `sequentialthinking` with current `thoughtNumber`
2. **Act** → Execute tools or gather evidence based on reasoning step
3. **Observe** → Write results to memory graph as observations
4. **Assess** → Check if revision needed or chain should continue
5. **Stop** → When `nextThoughtNeeded=false` or decision reached

**Guardrails**:
- Max 20 thoughts per chain
- Max 5 branches total
- Hard token/time budget per step
- "Fail-closed" if contradictory branches persist

## Phase 2: Evidence Gathering & Validation

**For each reasoning step**:
1. **Gather evidence**: Use read tools, search, or external queries
2. **Validate assumptions**: Cross-reference with historical data
3. **Track contradictions**: Flag when evidence contradicts hypotheses
4. **Persist observations**: Write evidence to memory as `reasoning.step` observations

## Phase 3: Revision & Branching Control

**Revision Protocol**:
- When evidence falsifies hypothesis: Set `isRevision=true`, `revisesThought=N`
- Create new step with corrected reasoning
- Link revision relations in memory graph

**Branching Protocol**:
- Use `branchFromThought` + `branchId` only for genuine alternatives
- Limit to 3 concurrent branches
- Merge branches when convergence criteria met
- Track branch outcomes separately

## Phase 4: Decision Convergence

**Convergence Criteria**:
- Evidence strength exceeds threshold
- Contradictions resolved
- All branches evaluated
- Decision confidence > 80%

**Terminal Decision**:
- Emit final decision with confidence score
- List all evidence and falsified alternatives
- Create `reasoning.chain` entity with outcome

## Phase 5: Memory Persistence (MANDATORY)

**Create Reasoning Chain Entity**:
```javascript
use_mcp_tool({
  server_name: "memory",
  tool_name: "create_entities",
  arguments: {
    entities: [{
      name: "reasoning#<runId>#<sha8(goal)>",
      entityType: "ReasoningChain",
      observations: [{
        type: "reasoning.chain",
        ts: "<ISO8601>",
        mode: "sequential-thinking@<version>",
        data: {
          goal: "<objective>",
          pattern: "<P1-P10>",
          totalSteps: <count>,
          branchCount: <count>,
          decision: "<final_decision>",
          evidenceRefs: ["<entity_refs>"],
          outcome: "verified_successful|failed|partial"
        }
      }]
    }]
  }
})
```

**Create Step Entities & Relations**:
- Each thought becomes a `ReasoningStep` entity
- Link with `BELONGS_TO`, `DERIVES_FROM`, `REVISES`, `BRANCHES_FROM` relations
- Connect to evidence entities (`REFERENCES`, `VALIDATES`, `FALSIFIES`)

☐ Link: ReasoningChain→ExternalEvidence (if external tools used)
☐ Store: Evidence provenance (tool:exa|perplexity, confidence, timestamp)
☐ Tag: Evidence type (precision_search | synthesis | reasoning)

## Error Handling & Recovery

**Stuck Chains**:
- If chain exceeds max thoughts without decision: Force convergence with best available evidence
- Log stuck pattern for future improvement

**Contradictory Evidence**:
- Escalate to human review when contradictions persist across branches
- Create conflict resolution task in memory

**MCP Failures**:
- Continue reasoning with local state
- Queue memory writes for later replay
- Degrade gracefully without historical context

## Quality Assurance

**Chain Validation**:
- Every hypothesis tested with evidence
- Revisions properly linked to original thoughts
- Branches merged or explicitly abandoned
- Decision supported by evidence strength

**Performance Monitoring**:
- Track reasoning efficiency (steps per decision)
- Monitor pattern effectiveness by success rate
- Identify common failure modes for pattern improvement