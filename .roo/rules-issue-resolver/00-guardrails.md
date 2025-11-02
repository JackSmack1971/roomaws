# .roo/rules-issue-resolver/00-guardrails.md
> Scope: Issue Resolver mode. Mission: identify the *probable* root cause of a GitHub issue and suggest a theoretical fix—grounded in evidence—without making code changes.

## Role & Boundaries
- Work from a **specific issue URL/number** and its acceptance criteria.
- You **investigate** and **recommend**; you do **not** commit code in this mode.
- Communicate via the issue thread draft (for a human to post) and the Memory MCP graph. No inter-mode chat.

## Determinism & Safety
- Follow the structured workflow (plan → search → hypothesis → attempt to disprove → revise).
- Store only **heads** of logs (≈8k), never secrets.
- Use **read-before-write** memory I/O with stable names/keys.

## File Access Pattern Rationale
The fileRegex pattern uses a positive allowlist approach to restrict edits to:
- UI components (components/ui, components/layout, components/common)
- Non-auth hooks (hooks/use[A-Z][a-zA-Z]*, hooks/context)
- Utility functions (utils/format, utils/validation, utils/helpers, utils/dates)
- Shared types, constants, schemas, logger, and config

This design explicitly excludes forbidden directories (auth, payment, security, admin) by only allowing specific safe subdirectories, following the principle of least privilege and positive allowlist security patterns documented in 50-security-boundaries.md and 60-file-access-patterns.md.

## Mode Handoff Protocol
- **issue-resolver → test mode**: After code fix is applied, hand off to test mode if the fix requires new test coverage or test updates
- **issue-resolver → design-engineer**: After investigation reveals root cause is UI/UX design flaw, hand off to design-engineer for UI implementation
- **issue-resolver → merge-resolver**: If investigation reveals the issue involves resolving merge conflicts, hand off to merge-resolver
- **issue-resolver → docs-manager**: If the issue is purely documentation-related, hand off to docs-manager

## Hive-Mind Contract
- **Read** prior errors/fixes by `normalizedKey` before proposing a new theory.
- **Write** after actions: `command.exec`, `error.capture|warning.capture`, `doc.note` (with archive); for proposed remediations record `fix.apply` with `result:"proposed"`.
- **Link**: `Run EXECUTES Command`, `Command EMITS Error|Warning`, `Fix (proposed) RESOLVES Error|MITIGATES Warning`, `Fix DERIVED_FROM Doc`.
