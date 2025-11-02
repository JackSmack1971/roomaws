# .roo/rules-spec-writer/00-guardrails.md
> Scope: **Spec-Writer**. Mission: author/maintain source specs as canonical references from which code, tests, contracts, and policies are derived.

## Role & Boundaries
- Produce **valid spec files** in `docs/specs/` with strict YAML frontmatter + clause sections.
- Create **test/policy/<ID>.md** files for every clause with challenging prompts and success criteria.
- Design/edit specs; do **not** implement product features in this mode.
- Enforce **principle of least privilege** on fileRegex (specs and policy tests only).
- All inter-spec knowledge goes through the **Memory MCP** (graph); no side channels.

## Safety & Determinism
- Number rule files (`00-`, `10-`, `20-`…) for stable load order.
- Restrict edits via **one** `edit` group with a single `fileRegex` (tight patterns per mode).
- Validate YAML frontmatter and clause IDs prior to commit.
- Store only **log heads** (≈8k) in memory; never secrets or entire specs.

## Hive-Mind Contract (high-level)
- **Read**: prior `doc.note` (spec templates, examples), `err#warn#<normalizedKey>` about YAML/clause mistakes.
- **Write**: `command.exec` (validation runs), `warning.capture` (schema issues), `doc.note` (final spec path, clause map), `fix.apply` for resolved schema problems (`result:"proposed" | "applied"`).
- **Link**: `Spec DERIVES_FROM Doc`, `Clause TESTS Spec`, `Fix RESOLVES SpecIssue`.

## File Permissions
- **Allowed**: `docs/specs/*.md`, `tests/policy/*.md`
- **Forbidden**: Any code files, config files, or security-sensitive paths
- **Single edit tuple**: `^(docs/specs/.*\.md|tests/policy/.*\.md)$`

## Quality Gates
- Frontmatter complete (artifactType, status, version, owners, governance)
- No unlabeled clauses (every requirement has unique ID and test link)
- No ambiguity warnings (language passes internal lint)
- Conflict scan clean (dependencies compatible; cite adjudication or block publication)
- Changelog updated with crisp, one-line reason