# .roo/rules-merge-resolver/10-workflow.md
> Comprehensive workflow for merge conflict resolution, from detection through validation and documentation.

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

**CRITICAL EXECUTION GATE**: Do not proceed to Intake & Preparation Phase without successful validation of this step. Historical knowledge prevents repeated mistakes and reduces time-to-resolution.

---

## Intake & Preparation Phase

1) **Parse pull request identifier**: Accept formats like `#123`, `123`, or full PR URL
2) **Fetch pull request metadata**: Retrieve title, description, branch names, and commit history
3) **Assess merge complexity**: Evaluate number of commits, files changed, and potential conflict areas
4) **Prepare working environment**: Ensure clean git state and proper branch checkout
5) **Gather context**: Review PR description, related issues, and recent changes to base branch

## Environment Setup & Safety Checks

1) **Verify repository state**: Ensure working directory is clean and on correct branch
2) **Backup current state**: Create safety checkpoints before merge operations
3) **Check merge prerequisites**: Verify all required tools and permissions are available
4) **Set up conflict resolution environment**: Configure git merge tools and diff viewers
5) **Establish rollback procedures**: Document steps to return to pre-merge state if needed

## Merge Attempt & Conflict Detection

1) **Execute merge operation**: Attempt to merge target branch into current branch
2) **Detect conflict status**: Identify if merge succeeded or conflicts were encountered
3) **Catalog conflicted files**: List all files with merge conflicts and their locations
4) **Assess conflict scope**: Evaluate number of conflicts, files affected, and complexity level
5) **Prioritize resolution order**: Sort conflicts by importance and interdependencies

## Conflict Analysis & Understanding

1) **Examine conflict markers**: Review each conflict block with `<<<<<<<`, `=======`, `>>>>>>>` markers
2) **Analyze change intent**: Use git blame and commit history to understand purpose of each change
3) **Identify conflict types**: Categorize as logical conflicts, formatting conflicts, or overlapping changes
4) **Map dependency relationships**: Understand how conflicts in different files relate to each other
5) **Research historical context**: Check related commits, issues, and documentation for guidance

## Resolution Strategy Development

1) **Apply intent-aware merging**: Preserve bug fixes, combine compatible features, resolve logical conflicts
2) **Consider change hierarchy**: Prioritize logic changes over formatting, recent changes over older ones
3) **Evaluate test impact**: Assess how resolutions affect existing test coverage and functionality
4) **Plan documentation updates**: Identify documentation that needs updating alongside code changes
5) **Develop rollback strategy**: Plan for reverting changes if resolution proves incorrect

## Detailed Conflict Resolution

### Content Conflict Resolution
1) **Semantic analysis**: Understand what each side of the conflict is trying to achieve
2) **Change integration**: Combine compatible changes while preserving important modifications
3) **Logic preservation**: Ensure business logic and functionality remain intact
4) **Code style consistency**: Maintain consistent formatting and style across resolved sections
5) **Comment preservation**: Keep important comments and documentation from both sides

### Structural Conflict Resolution
1) **Import organization**: Resolve conflicting import statements and module references
2) **Function signature alignment**: Ensure function signatures match across merged code
3) **Type definition consistency**: Maintain consistent type definitions and interfaces
4) **Configuration merging**: Properly combine configuration files and settings
5) **Resource reference updates**: Update file paths and resource references as needed

### Documentation Conflict Resolution
1) **Comment synchronization**: Merge code comments that describe different aspects of functionality
2) **README updates**: Ensure documentation reflects merged functionality
3) **API documentation alignment**: Update API docs to reflect resolved interfaces
4) **Changelog integration**: Combine changelog entries from both branches
5) **Migration guide updates**: Update migration documentation for breaking changes

## Implementation & Validation

1) **Apply resolutions incrementally**: Resolve conflicts one file at a time with validation after each
2) **Syntax validation**: Ensure resolved code compiles and passes basic syntax checks
3) **Logic verification**: Test that resolved code maintains intended functionality
4) **Integration testing**: Verify that resolved changes work with dependent components
5) **Performance validation**: Ensure resolutions don't introduce performance regressions

## Quality Assurance & Testing

1) **Unit test execution**: Run affected unit tests to verify functionality preservation
2) **Integration test validation**: Execute integration tests to ensure system-wide compatibility
3) **Build verification**: Confirm that project builds successfully after resolution
4) **Code quality checks**: Run linters and static analysis tools on resolved code
5) **Manual testing**: Perform exploratory testing of resolved functionality

## Documentation & Communication

1) **Resolution documentation**: Record what was changed and why for each conflict
2) **Decision rationale**: Document reasoning behind resolution choices for future reference
3) **Impact assessment**: Note any side effects or considerations for stakeholders
4) **PR comment preparation**: Prepare clear explanation of changes for pull request
5) **Team notification**: Inform relevant team members of significant resolution decisions

## Finalization & Cleanup

1) **Conflict marker removal**: Ensure all `<<<<<<<`, `=======`, `>>>>>>>` markers are removed
2) **File staging**: Stage resolved files and complete merge operation
3) **Final validation**: Run comprehensive tests to ensure merge stability
4) **Branch cleanup**: Remove temporary branches or merge artifacts
5) **Status reporting**: Provide final summary of merge resolution outcome

## Memory Integration Points

1) **Conflict logging**: Record merge conflicts with details about resolution strategies used
2) **Resolution pattern tracking**: Store successful resolution approaches for similar future conflicts
3) **Learning capture**: Document insights gained from complex conflict resolutions
4) **Pattern recognition**: Identify recurring conflict types and proven resolution methods
5) **Knowledge preservation**: Maintain searchable history of merge challenges and solutions

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
