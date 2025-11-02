# .roo/rules-mode-writer/10-workflow.md
> Canonical authoring workflow (mapped from XML).

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

**CRITICAL EXECUTION GATE**: Do not proceed to Intake & Intent without successful validation of this step. Historical knowledge prevents repeated mistakes and reduces time-to-resolution.

---

## Intake & Intent
1) Determine **new vs edit** (slug, scope, responsibilities). Create TODO ledger.

## Design
2) Draft minimal `.roomodes` entry — fields: `slug`, `name`, `roleDefinition`, `whenToUse`, `groups`.
3) Choose **permission pattern** (documentation_only / test_focused / config_management / full_stack).
4) Define **single** `edit` with `fileRegex` (tight, anchored).

## Rules Pack
5) Create `./.roo/rules-<slug>/` files:
   - `00-guardrails.md` (scope, least-privilege)
   - `10-workflow.md` (step-by-step)
   - `20-best-practices.md`
   - `30-common-patterns.md`
   - `40-tool-usage.md`
   - `50-examples.md`
   - `60-memory-io.md` (hive‑mind I/O exact usage)

## Validation
6) Lint YAML and test regex; ensure **no** contradictions between YAML and rules.
7) Run **cohesion checks** (boundaries, orchestrator clarity, overlaps).

## Ship
8) Produce final diff; write memory envelopes; summarize decisions and constraints.

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
