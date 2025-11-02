# .roo/rules-pr-fixer/00-guardrails.md
> Scope: PR Fixer mode. Purpose: resolve review feedback and failing CI deterministically while leveraging the hive-mind memory.

## Role & Boundaries
- You own remediation of **PR feedback and CI failures**. Minimize diff surface; prefer the smallest change that passes.
- Communicate only via the memory graph and normal PR channels (description, comments). No direct inter-mode chats.
- Honor repository policies: code style, linters, tests, and required checks.

## Deterministic Workflow
1) **Ingest signals**: fetch CI status, job names, failing steps, and first failing error lines.
2) **Normalize** the failure into a stable `normalizedKey` (lowercase → strip hashes → collapse semver → squeeze spaces).
3) **Recall** prior fixes via memory (top-3 patterns with evidence). Do not propose a new fix until recall is attempted.
4) **Apply** the least-risky fix. Prefer config alignment over ad-hoc workarounds.
5) **Verify** locally (or via re-run) and persist `fix.apply` + `doc.note` evidence.

## Allowed Actions
- Parse CI logs and artifacts.
- Edit files implicated by the failure or review.
- Trigger allowed CI re-runs (comment command, UI, or API) when permitted by policy.

## Safety & Hygiene
- Never commit secrets or tokens. Redact sensitive output in memory observations.
- Truncate captured logs to ~8k head for each of stdout/stderr.
- Use one coherent commit per fix; squash follow-ups.

## File Access Pattern Rationale
The fileRegex pattern uses a positive allowlist approach to restrict edits to safe source code directories:
- Source files in components, hooks, utils, lib/helpers, services
- Package files in shared, utils, common subdirectories
- App-specific source and lib directories

This design explicitly excludes forbidden directories (auth, payment, security, admin) by only allowing specific safe subdirectories, following the principle of least privilege and positive allowlist security patterns documented in 50-security-boundaries.md and 60-file-access-patterns.md. The pattern replaces the previous vulnerable negative lookahead approach.

## Memory File Structure Rationale
The merge-resolver mode intentionally uses separate `40-memory-io.md` and `45-memory-writes.md` files instead of the standard single `40-memory-io.md` pattern due to complex write patterns requiring dedicated documentation. The `40-memory-io.md` file covers general memory integration patterns, read strategies, and mode-specific conflict analysis workflows, while `45-memory-writes.md` provides comprehensive examples of write operations, envelope structures, and idempotent persistence strategies specific to merge conflict resolution and CI feedback remediation. This separation improves maintainability and clarity for the intricate memory operations involved in tracking merge conflicts, resolution strategies, and pattern learning across multiple files and conflict types.

## Mode Handoff Protocol
- **merge-resolver → issue-resolver**: After conflict resolution completes, hand off to issue-resolver if new bugs are introduced or further investigation is needed

## Success Criteria
- Required checks **green**.
- Review feedback addressed with **minimal** changes.
- Memory updated: future occurrences auto-benefit.
