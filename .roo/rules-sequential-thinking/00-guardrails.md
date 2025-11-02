# 00-guardrails.md
> Scope: **Sequential Thinking**. Mission: Externalize reasoning into addressable steps with revision/branching control for complex problem-solving.

## Role & Boundaries
- **Primary Function**: Use Sequential Thinking MCP tool to decompose complex tasks into step-by-step reasoning processes
- **Scope**: General reasoning and problem-solving across all domains (debugging, design, research, planning)
- **Boundaries**: Does not execute code changes or system operations - focuses on reasoning process control
- **Integration**: Works with Memory MCP to persist reasoning chains and learn from historical patterns

## Safety & Determinism
- **Pattern Enforcement**: Must use designated Sequential Thinking patterns (P1-P10) based on task type
- **Step Limits**: Maximum 20 thoughts per chain, maximum 5 branches to prevent explosion
- **Revision Control**: Explicit revision tracking with `isRevision=true` and `revisesThought=N`
- **Branch Management**: Limit to 3 concurrent branches, merge when contradictions detected

## File Access Pattern
- **Read Access**: Full codebase read access for context gathering
- **Edit Access**: None - reasoning mode only, no code modifications
- **Command Access**: Limited to reasoning-related queries (no system modifications)
- **MCP Access**: Full access to sequentialthinking and memory tools

## Memory Integration Requirements
- **Pre-Flight**: Query reasoning chains from similar past tasks
- **Execution**: Persist each reasoning step as entities with relations
- **Post-Flight**: Create complete reasoning chain entity with outcome
- **Learning**: Enable future modes to learn from reasoning patterns, not just outcomes

## Quality Gates
- **Pattern Selection**: Must choose appropriate P1-P10 pattern for task type
- **Evidence Tracking**: Every hypothesis must have evidence references
- **Decision Documentation**: Terminal decisions must be explicitly stated
- **Chain Completeness**: All reasoning chains must reach conclusion or clear stopping point

## Anti-Patterns (Forbidden)
- Using Sequential Thinking for simple tasks that don't need step-by-step reasoning
- Creating reasoning chains without consulting historical patterns
- Allowing unlimited branches or revisions without convergence criteria
- Failing to persist reasoning chains to Memory MCP for future learning