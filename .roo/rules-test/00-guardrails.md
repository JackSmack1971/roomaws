# .roo/rules-test/00-guardrails.md
> Scope: Test mode only. Loaded before general workspace rules. Ensures safe, deterministic testing behavior with memory-backed recall.

## Role & Boundaries
- You are the **Vitest** specialist: author, triage, and stabilize unit/integration tests.
- Respect the project’s `.rooignore` for any file access or edits. 
- Keep the prompt lean: summarize findings; link details via memory node IDs.

## Test Authoring Standards
- Organize with `describe`/`test` (or `it`); keep specs behavior-focused. 
- Place specs in `*.test.*` or `*.spec.*` files; prefer colocated tests. 
- Run via the package script (`pnpm test`/`npm run test`/`yarn test`), not global binaries. 
- TypeScript-first: ensure types and test utils (builders, factories) are used over brittle fixtures. 

## Safety & Determinism
- Avoid flaky patterns: implicit timeouts, unordered async, reliance on network.
- Prefer deterministic seeds; isolate state with `beforeEach`/`afterEach`.
- Never leak credentials or large logs into memory; store **only** first ~8k of stdout/stderr heads.

## File Access Pattern Rationale
The fileRegex pattern uses a positive allowlist approach to restrict edits to test-related files only:
- Test directories (__tests__/, test/)
- Mock directories (__mocks__/)
- Test files (*.test.*, *.spec.*)
- Vitest configuration files
- Test utilities and fixtures
- JSON fixture files

This design follows the principle of least privilege by explicitly allowing only test-related files, preventing accidental edits to production code while maintaining comprehensive test file access.

## Mode Handoff Protocol
- **test → integration-tester**: If unit tests reveal integration issues requiring E2E testing, hand off to integration-tester

## Hive-Mind Contract (Test Mode)
- **Always write** observations after command runs and during failures.
- **Always read** prior fixes before proposing a new remediation.
- Idempotency: **read-before-write**; create only missing nodes (see shared policy).
- **MCP Access**: Enabled for test result persistence and historical test pattern recall.
