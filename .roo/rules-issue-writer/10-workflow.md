# .roo/rules-issue-writer/10-workflow.md
> Canonical workflow from intake → created issue.

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

**CRITICAL EXECUTION GATE**: Do not proceed to Initialize without successful validation of this step. Historical knowledge prevents repeated mistakes and reduces time-to-resolution.

---

1) **Initialize**
   - Start TODOs; detect repo + monorepo/standard; begin codebase discovery.

2) **Discover & Verify**
   - Extract keywords from the user message.
   - Search codebase to verify components, errors, and data flow.
   - Classify **bug vs feature** with evidence.

3) **Template Detection**
   - Scan `.github/ISSUE_TEMPLATE/` (YAML forms first, then MD).
   - If multiple templates exist, present choices (name/description).
   - If none, use minimal generator (bug/feature).

4) **Draft Issue**
   - Fill the chosen template with user-impact first; insert verified code context (paths/lines).
   - Add acceptance criteria only when contributing scope is requested.

5) **Duplicate Check**
   - `gh issue list --search "<keywords>" --state all --limit 20`; show candidates; proceed or comment instead.

6) **Confirm & Submit**
   - Save draft to `./github_issue_draft.md`; confirm; `gh issue create … --body-file ./github_issue_draft.md` with template labels.

7) **Post-Create**
   - Return created URL; clean up draft file; write memory envelopes.

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
