# .roo/rules-integration-tester/50-test-environment.md
> Environment, commands, APIs, and utilities (converted from XML).

## Framework & Layout
- Mocha TDD + VS Code Extension Test host; custom utils; event-driven patterns; workspace-based execution.

## Directories
- Tests: `apps/vscode-e2e/src/suite/`
- Utils: `apps/vscode-e2e/src/utils/`
- Runner: `apps/vscode-e2e/src/runTest.ts`
- Types: `packages/types/`
- Package config: `apps/vscode-e2e/package.json`

## Commands
- **cwd:** `apps/vscode-e2e`
- Run all: `npm run test:run`
- Run one: `TEST_FILE="filename.test" npm run test:run`
- Never use `npm test` if not defined.

## Global `api` (key methods)
- Task mgmt: `startTask`, `cancelCurrentTask`, `clearCurrentTask`, `abortTask`, `getTaskStatus`
- Events: `onDidReceiveMessage`, `onTaskCompleted`, `onTaskAborted`, `onTaskStarted`, terminal start/end
- Settings: `updateSettings`, `getSettings`

## Utilities
- `waitFor`, `waitUntilCompleted`, `waitUntilAborted`
- Helpers: file locator, event collector, assertion helpers

## Workspace Management
- Workspace created by `runTest.ts`; path via `vscode.workspace.workspaceFolders[0].uri.fsPath`
- Create all test files in `suiteSetup`; verify; clean in `suiteTeardown`
- AI may not *see* workspace files; instruct it to **assume** they exist; validate outcomes yourself.

## Message Types
- `api_req_started` (reliable tool start indicator), `completion_result` (results), generic `text` (not reliable for tool detection)

## Auto-Approval Settings
- Enable `alwaysAllowWrite` / `alwaysAllowExecute` (and `alwaysAllowBrowser` if needed) for scenarios requiring those capabilities.

## Debugging & Performance
- Log phase transitions, events, file paths, expected vs actual; validate state inline.
- Timeouts: ~30s for tasks, 5–10s for FS ops, 10–15s for event waits.
- Clean up listeners, tasks, files to avoid leaks.
