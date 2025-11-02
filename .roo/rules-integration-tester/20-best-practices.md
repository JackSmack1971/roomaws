# .roo/rules-integration-tester/30-best-practices.md
> Project-level testing conventions (converted from XML).

## Structure
- TDD interface only; descriptive names; dedicated setup/teardown; store paths in a suite-scoped object.
- Tests must run in any order; strict cleanup to avoid pollution.

## API Interactions
- Use global `api` for extension actions; `waitFor`, `waitUntilCompleted`, `waitUntilAborted` for flow control.
- Set auto-approval (write/execute) when the scenario requires it.
- Prefer terminal shell events to verify command execution; avoid deep parsing of conversational messages.

## File System Handling
- Workspace is created by `runTest.ts` (often under `/tmp/roo-test-workspace-*`).
- Verify files in multiple locations; **create** in the workspace; **log** expected vs actual paths.

## Reliability
- Wait for **task completion**, not specific tool invocations.
- Keep prompts simple; validate outcomes; avoid brittle message schemas.

## Utilities & Sharing
- Factor common helpers; document them; reuse across suites.
