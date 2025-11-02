# .roo/rules-integration-tester/20-test-patterns.md
> Reusable patterns (converted from XML).

## Mocha TDD Structure
- Suite/case skeleton; `suiteSetup` creates workspace/files; `suiteTeardown` cancels tasks & cleans files.
- Event-listening tests: collect messages & task events; assert completion, not internal chatter.
- File-creation tests: search multiple plausible locations in workspace/OS temp; assert content.

## API Interaction Patterns
- Start tasks; wait for completion/abortion; update auto-approval settings when behavior requires writes/exec.
- Validate observable outcomes and essential message types (only those guaranteed by the framework).

## Error Handling Patterns
- Task abortion flow; invalid input handling; condition-based waits (`waitFor`) over fixed sleeps.

## Utility Patterns
- **File Locator**, **Event Collector**, **Assertion Helpers** for consistent validations across suites.

## Debugging Patterns
- Comprehensive logging at critical phases; state validation helpers (workspace listing, CWD, status, event counts).
