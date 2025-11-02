# Failure Triage Loop (Test mode)

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

**CRITICAL EXECUTION GATE**: Do not proceed to Failure Triage Loop without successful validation of this step. Historical knowledge prevents repeated mistakes and reduces time-to-resolution.

---

1) On command completion: emit `command.exec` with stdoutHead/stderrHead (first ~8k chars), exitCode, durationMs.
2) If exitCode != 0:
   - Derive `normalizedKey` from the primary error line (lowercase, strip hashes/semver).
   - Persist `error.capture {kind: "TestFailure", message, detector: "vitest", normalizedKey}`.
   - Query: search_nodes("type:Error normalizedKey:<key>") → follow (:Fix)-[:RESOLVES]->(:Error) and (:Fix)-[:DERIVED_FROM]->(:Doc).
   - Summarize top 3 prior Fix patterns; apply the safest minimal-change fix first.
3) After remediation: persist `fix.apply {strategy, changes[], result}` and any `doc.note {url,title,excerpt}`; link Fix DERIVED_FROM Doc.

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
