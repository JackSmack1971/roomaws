# .roo/rules-design-engineer/10-workflow.md
> Canonical workflow for implementing UI designs with high fidelity and consistency.

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

**CRITICAL EXECUTION GATE**: Do not proceed to Intake & Analysis without successful validation of this step. Historical knowledge prevents repeated mistakes and reduces time-to-resolution.

---

## Intake & Analysis
1) **Review design specifications**: Analyze provided design files (Figma, Sketch, etc.) for component requirements, interactions, and visual details.
2) **Assess technical feasibility**: Evaluate design against existing design system (Shadcn components, Tailwind utilities).
3) **Identify dependencies**: Check for required assets, icons, or shared components.

## Component Development
4) **Create component structure**: Set up TypeScript interfaces, component files, and basic markup.
5) **Implement base styles**: Apply Tailwind classes for layout, colors, and typography.
6) **Add interactivity**: Implement hover states, animations, and user interactions.
7) **Handle responsive behavior**: Ensure mobile-first approach with appropriate breakpoints.

## Quality Assurance
8) **Accessibility audit**: Verify WCAG 2.1 AA compliance (color contrast, keyboard navigation, screen reader support).
9) **Cross-browser testing**: Test in supported browsers and devices.
10) **Performance check**: Ensure components render efficiently and don't cause layout shifts.

## Documentation & Testing
11) **Create Storybook stories**: Document component variants, states, and usage examples.
12) **Write component tests**: Add unit tests for functionality and visual regression tests.
13) **Update documentation**: Maintain component documentation and usage guidelines.

## Integration & Validation
14) **Integrate into application**: Replace placeholder components with implemented versions.
15) **Visual verification**: Compare implementation against original design specifications.
16) **Final accessibility pass**: Confirm all requirements are met before marking complete.

## Completion Criteria
- Component matches design specifications pixel-perfectly
- Passes accessibility audits (WCAG 2.1 AA)
- Responsive across all target devices
- Includes comprehensive Storybook documentation
- Has appropriate test coverage
- Follows established component patterns and conventions

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