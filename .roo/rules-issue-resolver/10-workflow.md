# .roo/rules-issue-resolver/10-workflow.md
> Canonical workflow from intake → draft comment.

## Phase 0: Memory Consultation (MANDATORY - DO NOT SKIP)

**Objective**: Leverage historical knowledge before attempting solutions.

**Steps**:
1. **Extract task signature**:
   - For errors: Normalize error message (strip hashes/paths/versions)
   - For tasks: Extract key entities (component names, file paths, error types)

2. **Query memory**:
   ```javascript
   use_mcp_tool({
     server_name: "memory",
     tool_name: "search_nodes",
     arguments: { query: "type:Error|Fix <signature>" }
   })
   ```

3. **Analyze results**:
   - **If hits found**: Review top 3 fixes/docs
   - **If no hits**: Flag as "novel case" for future learning
   - **If MCP unavailable**: Log degraded mode warning

4. **Document consultation**:
```
✓ Memory consulted: [N results | No matches | MCP unavailable]
✓ Top recommendation: [fix#<id> with strategy X | None applicable]
✓ Evidence: [doc#<id> from <source> | Local knowledge only]
```

5. **Validate consultation execution**:
   - **MANDATORY GATE**: Verify memory consultation was actually executed (not skipped)
   - **MCP Failure Handling**: If MCP unavailable, warn user and proceed in degraded mode with local knowledge only
   - **Skipped Query Handling**: If consultation was bypassed, STOP immediately and require explicit user confirmation to proceed
   - **Degraded Operation Warning**: Display clear user notification: "⚠️ Operating in degraded mode - memory consultation unavailable. Proceeding with local knowledge only."

**CRITICAL EXECUTION GATE**: Do not proceed to Intake phase without successful validation of this step. Historical knowledge prevents repeated mistakes and reduces time-to-resolution.

---

## Phase 1.5: External Evidence Gathering (CONDITIONAL)

**Trigger Conditions**:
- Error involves external dependency (check imports/package.json)
- Memory MCP returned zero results OR low-confidence matches (<0.7)
- Error pattern not found in local codebase search

**Decision Tree**:
```
Error Analysis
│
├─ External library/API error?
│  └─ YES → Exa: get_code_context_exa for library behavior
│
├─ Community-known issue?
│  └─ MAYBE → Perplexity: perplexity_ask for known patterns
│
├─ Complex root cause analysis?
│  └─ YES → Perplexity: perplexity_reason for diagnostic approach
│
└─ Novel/unique error?
   └─ Cascade: Exa domain search → Perplexity synthesis
```

**Execution Pattern**:

### A. Library Documentation Search (Exa)
When error includes library/framework reference:
```javascript
use_mcp_tool({
  server_name: "exa",
  tool_name: "get_code_context_exa",
  arguments: {
    query: "<library> <error_context> documentation",
    tokensNum: 5000
  }
})
```

**Example**: For "TypeError: Cannot read property 'map' of undefined in React":
```javascript
query: "React array rendering map undefined error handling"
```

### B. Working Examples Search (Exa)
When you need implementation patterns:
```javascript
use_mcp_tool({
  server_name: "exa",
  tool_name: "web_search_exa",
  arguments: {
    query: "<library> <method> working example",
    numResults: 3
  }
})
```

### C. Community Pattern Analysis (Perplexity)
When error might be known issue:
```javascript
use_mcp_tool({
  server_name: "perplexity",
  tool_name: "perplexity_ask",
  arguments: {
    messages: [{
      role: "user",
      content: "Is this a known issue: <normalized_error>? What are common solutions?"
    }]
  }
})
```

### D. Diagnostic Reasoning (Perplexity)
For complex/novel errors:
```javascript
use_mcp_tool({
  server_name: "perplexity",
  tool_name: "perplexity_reason",
  arguments: {
    messages: [{
      role: "user",
      content: "Analyze error and suggest diagnostic approach: <error_details>"
    }]
  }
})
```

**Evidence Synthesis**:
1. Merge external findings with Memory patterns
2. Update hypothesis list with evidence-backed candidates
3. Flag contradictions for explicit validation
4. Assign confidence scores to each hypothesis

**Output**: Enhanced investigation plan with:
- Prioritized hypothesis list (ranked by evidence quality)
- External source citations (URLs from Exa, citations from Perplexity)
- Confidence assessment for each potential fix

**Example Decision**:
```
Hypothesis Priority List:
1. [High Confidence] Async timing issue (Memory: 3 prior fixes, Perplexity: cited in 5 sources)
2. [Medium] State management bug (Exa: 2 similar examples, no Memory hits)
3. [Low] Library version incompatibility (Perplexity: mentioned but outdated)
```

---

## Intake
1) Require full GitHub issue URL or `{owner}/{repo}#number`.
2) Fetch issue JSON (title, body, labels, comments).
3) Extract **keywords** (feature names, error strings, functions, files, components).

## Plan
- Create a TODO list: search terms → files to read → hypotheses → disproof steps → draft.

## Issue Analysis
1) **Broad search** with extracted keywords (`codebase_search`).
2) Inspect top-relevant files; **narrow search** using concrete identifiers found.
3) Form a **hypothesis** (probable cause).
4) **Try to disprove it** (alternate paths, configs, edge cases).
5) If disproven, iterate; else proceed to performance triage.

## Step 2: Performance Triage (if applicable)
If the issue involves "slow", "timeout", "freeze", "lag", "memory leak", or performance degradation:
1. Switch to performance-profiler mode
2. Run reproduction benchmark with performance-profiler
3. Capture flamegraph and performance metrics
4. Return to issue-resolver with findings
5. Incorporate performance insights into root cause analysis

## Investigation Loop
1) **Broad search** with extracted keywords (`codebase_search`).
2) Inspect top-relevant files; **narrow search** using concrete identifiers found.
3) Form a **hypothesis** (probable cause).
4) **Try to disprove it** (alternate paths, configs, edge cases).
5) If disproven, iterate; else proceed to solution framing.

## Solution Framing
- Describe a **theoretical fix** ("It seems this could be resolved by…").
- Note downstream effects, tests to add, and unknowns to confirm.

## Draft for Issue
- Friendly opener → concise hypothesis → file paths/functions → next steps/tests → invite maintainer confirmation.

---

## Final Phase: Knowledge Capture (MANDATORY - DO NOT SKIP)

**Objective**: Persist learnings for future runs.

**Steps**:
1. **Create observation envelopes** (see `40-memory-io.md` for schemas):
   - `command.exec` for key operations
   - `error.capture` for failures
   - `fix.apply` for resolutions
   - `doc.note` for research sources

2. **Write to memory**:
   ```javascript
   use_mcp_tool({ server_name: "memory", tool_name: "create_entities", ... })
   use_mcp_tool({ server_name: "memory", tool_name: "add_observations", ... })
   use_mcp_tool({ server_name: "memory", tool_name: "create_relations", ... })
   ```

3. **Validate persistence**:
   ```
   ✓ Entities created: [run#..., cmd#..., fix#...]
   ✓ Relations linked: [EXECUTES, RESOLVES, DERIVED_FROM, PERFORMED_BY, TOUCHES]
   ✓ Memory persistence confirmed
   ```

**If memory write fails**: Log structured event with `{ operation, data, timestamp }` for later replay when MCP recovers.

---

**Update POST-FLIGHT**:
```markdown
☐ Write: Observation envelope with external evidence metadata
☐ Link: Fix→ExternalEvidence (if used), Error→Documentation
☐ Store: Tool provenance (exa|perplexity), confidence scores
☐ Confirm: List entity IDs + external source URLs
```
