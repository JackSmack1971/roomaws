# Hivemind Memory Contract (applies to all modes)

You MUST persist and reuse knowledge via the Memory MCP.

Observation Envelope (stringified JSON):
{ "type": "command.exec|error.capture|warning.capture|fix.apply|doc.note|run.summary",
  "ts": "<ISO8601>", "mode": "<slug>@<ver?>", "repo": "...", "branch": "...",
  "fingerprint": "<sha256>", "data": { ... } }

Relations (active voice):
Run EXECUTES Command; Command EMITS Error|Warning; Error CAUSED_BY Dependency;
Fix RESOLVES Error | Fix MITIGATES Warning; Fix DERIVED_FROM Doc; Doc REFERENCES Concept;
Error ABOUT Concept; Run PERFORMED_BY Mode; Run USES Tool; Run TOUCHES File.

Idempotency:
- BEFORE create_*: search_nodes by stable keys (e.g., normalizedKey, command hash, entity name).
- Use open_nodes for exact names; only create missing entities/relations.

Always call MCP tools via `use_mcp_tool(server_name="memory", tool_name=<tool>, arguments=<json>)`.

## Mode Orchestration and Handoff Protocol

### Terminal vs Orchestrator Modes

**Terminal Modes** (complete tasks independently):
- `test` - Writes and maintains tests
- `translate` - Manages localization files
- `docs-manager` - Handles documentation extraction and verification
- `mode-writer` - Creates and maintains custom modes

**Orchestrator Modes** (coordinate multi-step workflows):
- `orchestrator` - Routes tasks to appropriate specialized modes
- `issue-resolver` - Investigates bugs, may hand off to test/design-engineer
- `merge-resolver` - Resolves conflicts, may hand off to issue-resolver
- `design-engineer` - Implements UI, may hand off to issue-resolver

### Handoff Triggers

**issue-resolver → test mode**:
- After code fix is applied
- When fix requires new test coverage
- When existing tests need updates

**issue-resolver → design-engineer**:
- When root cause is UI/UX design flaw
- When fix requires design system changes
- When issue involves component architecture

**merge-resolver → issue-resolver**:
- After conflict resolution completes
- When merge introduces new bugs
- When conflict resolution requires code investigation

**design-engineer → issue-resolver**:
- After UI implementation completes
- When implementation reveals integration issues
- When new components need backend integration

### Handoff Protocol

1. **Assess Completion**: Verify current mode's objectives are met
2. **Identify Dependencies**: Check if next mode needs different tools/permissions
3. **Prepare Context**: Document current state and remaining work
4. **Trigger Switch**: Use `switch_mode` with clear handoff rationale
5. **Memory Continuity**: Ensure observations link across mode transitions

### Orchestrator Decision Tree

```
New task received
├── Consult Memory MCP for similar past tasks
│   ├── Found proven effective mode?
│   │   ├── Yes → Route to proven mode with context
│   │   └── No → Continue to type-based routing
├── Has GitHub issue URL or #number?
│   ├── Yes → issue-resolver
│   └── No → Continue
├── Is it a merge conflict?
│   ├── Yes → merge-resolver
│   └── No → Continue
├── Is it UI/component design?
│   ├── Yes → design-engineer
│   └── No → Continue
├── Is it testing-related?
│   ├── Yes → test
│   └── No → Continue
├── Is it documentation?
│   ├── Yes → docs-manager
│   └── No → Continue
└── Default → orchestrator for routing
```

## External Evidence Protocol (Exa/Perplexity MCPs)

### Decision Matrix: When to Query External

**Query Memory FIRST** (always):
```javascript
use_mcp_tool({
  server_name: "memory",
  tool_name: "search_nodes",
  arguments: {query: "type:Error|Fix|Research <signature>"}
})
```

**Query Exa** when:
- Need precise technical documentation
- Searching for code examples/patterns
- Validating API behavior against official sources
- Filtering by specific domains required
- Token-efficient extraction needed

**Query Perplexity** when:
- Need multi-source synthesis with citations
- Researching best practices across community
- Validating complex technical claims
- Need reasoning-backed diagnostic approach
- Exploring unknown problem space

**NEVER query external** when:
- Working with purely internal code/configs
- Memory MCP has high-confidence results
- Simple mechanical tasks (formatting, refactoring)
- Network latency would impact UX

### Tool Selection Flowchart

```
Knowledge Need Identified
│
├─ Check Memory MCP
│  ├─ High confidence result? → USE IT
│  └─ Low/no confidence → Continue
│
├─ Need precise docs/code?
│  └─ YES → Exa (get_code_context_exa OR web_search_exa)
│
├─ Need synthesis/reasoning?
│  └─ YES → Perplexity (perplexity_research OR perplexity_reason)
│
└─ Complex/exploratory?
   └─ Cascade: Exa precision → Perplexity synthesis → Triangulate
```

### Evidence Storage Schema

**ExternalEvidence Entity**:
```javascript
{
  type: "ExternalEvidence",
  name: "evidence#<runId>#<sha8(query)>",
  observations: [
    "Tool: exa|perplexity",
    "Query: <original_query>",
    "Source: <URL or citation>",
    "Timestamp: <ISO8601>",
    "Confidence: High|Medium|Low",
    "Content: <extracted_content_summary>"
  ]
}
```
