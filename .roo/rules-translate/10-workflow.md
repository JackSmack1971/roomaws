# .roo/rules-translate/10-workflow.md
> Canonical workflow from intake → translation completion.

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

**CRITICAL EXECUTION GATE**: Do not proceed to Intake without successful validation of this step. Historical knowledge prevents repeated mistakes and reduces time-to-resolution.

---

## Intake
1) Require specific translation task: identify source strings, target languages, and context
2) Understand the string's purpose and UI context (button, tooltip, error message, etc.)
3) Check existing translations for consistency and terminology

## Translation Process
1) **Update English first**: Add or modify English strings in en.json files
2) **Identify context**: Use search_files to find nearby keys for apply_diff context
3) **Translate systematically**: Create translations for all supported languages using apply_diff
4) **Preserve structure**: Maintain JSON structure, placeholders, and interpolation variables
5) **Validate changes**: Run node scripts/find-missing-translations.js to check completeness

## Quality Assurance
1) **Check placeholders**: Ensure {{variable}} syntax is preserved exactly
2) **Verify terminology**: Maintain consistent translations for repeated terms
3) **Test context**: Consider UI constraints (button length, tooltip readability)
4) **Cultural adaptation**: Use natural, informal language appropriate for each locale

## Completion Criteria
- All supported languages have translations for new/modified strings
- Placeholders and interpolation variables are preserved
- Informal tone is maintained consistently
- Technical terms remain in English where appropriate
- Missing translations script passes without errors

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