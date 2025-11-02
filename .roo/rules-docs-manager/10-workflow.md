# .roo/rules-docs-manager/10-workflow.md
> Canonical workflow from documentation task intake → verification → final delivery.

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

**CRITICAL EXECUTION GATE**: Do not proceed to Intake & Requirements Gathering without successful validation of this step. Historical knowledge prevents repeated mistakes and reduces time-to-resolution.

---

## Research Phase - External Documentation Intelligence

### When to Use External MCPs:
1. **Extraction**: When source code references external APIs/libraries
2. **Verification**: When validating technical claims against official docs
3. **Accuracy**: When cross-referencing implementation details

### Documentation Discovery Workflow

#### Step 1: Official Documentation (Exa)
For each technical concept requiring external validation:

```javascript
use_mcp_tool({
  server_name: "exa",
  tool_name: "web_search_exa",
  arguments: {
    query: "<concept> official documentation",
    numResults: 2
  }
})
```

**Domain filtering for trusted sources**:
```javascript
// Example: React documentation
arguments: {
  query: "React hooks useEffect",
  numResults: 2,
  includeDomains: ["react.dev", "github.com/facebook/react"]
}
```

#### Step 2: Code Context Extraction (Exa)
When documenting library usage patterns:

```javascript
use_mcp_tool({
  server_name: "exa",
  tool_name: "get_code_context_exa",
  arguments: {
    query: "<library> <feature> usage examples best practices",
    tokensNum: 5000
  }
})
```

#### Step 3: Technical Claim Validation (Perplexity)
Before writing documentation assertions:

```javascript
use_mcp_tool({
  server_name: "perplexity",
  tool_name: "perplexity_ask",
  arguments: {
    messages: [{
      role: "user",
      content: "Verify technical claim: <claim_from_code_analysis>"
    }]
  }
})
```

### Cross-Reference Matrix

Create validation table for each technical assertion:
```
Claim: "useEffect runs after render"
├─ Source 1: Local code analysis (EXTRACTION-2024-01.md)
├─ Source 2: Exa → react.dev/reference/react/useEffect
├─ Source 3: Perplexity → Cited in 8 sources with examples
└─ Confidence: HIGH (3/3 sources agree)
```

### Discrepancy Handling

IF sources contradict:
1. Flag for manual review
2. Document both perspectives in output
3. Note recency and authority of each source
4. Defer to official docs (Exa domain-filtered) when available

**Example**:
```markdown
**Note**: Some community sources suggest X, but official documentation
(verified via Exa on 2024-11-01) clarifies that Y is the recommended approach.
See: [official docs link]
```

### Storage Protocol

POST-FLIGHT additions:
```markdown
☐ Store: External doc sources with URLs and access timestamps
☐ Link: Doc→ExternalSource, TechnicalClaim→Evidence
☐ Tag: Validation status (verified|unverified|conflicting)
☐ Metadata: Tool used (exa|perplexity), confidence score
```

---

## Intake & Requirements Gathering
1) **Identify documentation task type**: extraction, verification, writing, or updating existing docs.
2) **Gather context**: Source code paths, API endpoints, components, or existing documentation to update.
3) **Extract keywords**: Function names, class names, file paths, error messages, or feature descriptions.
4) **Assess scope**: Determine if task requires code analysis, API documentation, or general documentation writing.

## Documentation Analysis Phase
1) **Code examination**: Use `codebase_search` and `read_file` to understand the codebase structure and functionality.
2) **Pattern identification**: Identify documentation patterns, comment styles, and existing documentation quality.
3) **Gap analysis**: Compare current documentation against code functionality to identify missing or outdated content.
4) **Stakeholder identification**: Determine who will review and approve the documentation changes.

## Extraction & Content Generation
1) **API documentation**: Extract function signatures, parameters, return types, and usage examples from code.
2) **Code comments**: Generate or update inline comments explaining complex logic or business rules.
3) **README files**: Create or update project READMEs with setup instructions, usage examples, and architecture overviews.
4) **Technical specifications**: Document interfaces, data flows, and system interactions.

## Verification & Quality Assurance
1) **Accuracy check**: Verify that extracted information matches actual code behavior.
2) **Completeness validation**: Ensure all public APIs, functions, and features are documented.
3) **Consistency review**: Check that documentation follows project conventions and style guides.
4) **Technical review**: Validate that code examples are syntactically correct and runnable.

## Documentation Writing & Updates
1) **Content organization**: Structure documentation with clear sections, headings, and navigation.
2) **Example inclusion**: Add practical code examples and usage scenarios.
3) **Cross-referencing**: Link related documentation and create internal navigation.
4) **Version control**: Ensure documentation reflects current codebase state.

## Final Validation & Delivery
1) **Peer review**: Submit documentation for stakeholder review and feedback incorporation.
2) **Testing validation**: Verify that documentation examples work with current codebase.
3) **Publication**: Commit documentation changes and update any deployment processes.
4) **Maintenance planning**: Identify triggers for future documentation updates.

## Error Handling & Recovery
1) **Documentation failure detection**: Identify extraction errors, verification mismatches, or outdated content.
2) **Root cause analysis**: Determine why documentation became outdated or inaccurate.
3) **Corrective actions**: Apply fixes based on identified issues and update processes to prevent recurrence.
4) **Quality improvement**: Use failures as opportunities to improve documentation generation processes.
## Memory Integration Points

1) **Task completion logging**: Emit `command.exec` with stdoutHead/stderrHead (first ~8k chars), exitCode, durationMs.
2) **Error capture**: For documentation failures, persist `error.capture {kind: "DocFailure", message, detector: "extractor", normalizedKey}`.
3) **Prior fix retrieval**: Query Memory MCP for similar documentation issues and proven solutions.
4) **Success logging**: After successful documentation updates, persist `fix.apply {strategy, changes[], result}` and `doc.note {url,title,excerpt}`.
5) **Knowledge linking**: Connect fixes to source documentation via DERIVED_FROM relationships.

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