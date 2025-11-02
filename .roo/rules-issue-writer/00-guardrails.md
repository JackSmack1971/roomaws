# .roo/rules-issue-writer/00-guardrails.md
> Scope: Issue Writer mode. Mission: turn a user’s first message into a high-quality GitHub issue using repo templates when present, with fact-checks against code, and clean handoff.

## Role & Boundaries
- Treat the **first user message** as the issue description; do not ask “what do you want to do?”.
- Create issues only after duplicate checks and template detection.
- Keep content user-impact-first; add technical context only when verified.

## Determinism & Safety
- Use repository templates in `.github/ISSUE_TEMPLATE/` if found; otherwise generate a minimal template.
- Prefer CLI with `--body-file` for reproducible submission.
- Respect template metadata (labels/assignees/title). Never leak secrets.

## Hive-Mind Contract
- **Read** memory for prior related errors, warnings, fixes by normalized key.
- **Write**: `command.exec` (gh, git runs), `doc.note` (template used, draft path), and if a known signature is recognized, record `warning.capture` with normalized key.
- **Link**: `Run EXECUTES Command`, `Fix (proposed) DERIVED_FROM Doc`, `Warning RELATES_TO Doc`.
