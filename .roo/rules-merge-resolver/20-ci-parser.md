# .roo/rules-pr-fixer/10-ci-parser.md
> Parse CI signals into a stable error signature and remediation plan.

## Inputs
- PR metadata: branch, SHA, required checks.
- CI runs: names, conclusions, failing job/step logs.
- Lint/test/build artifacts (if provided).

## Parsing Steps
1) **Enumerate failing checks** (name, conclusion, job URL).
2) **Extract first failing step** and **primary error** line(s).
3) **Derive normalizedKey** from the primary error string:
   - Lowercase.
   - Strip volatile hashes/paths/timestamps.
   - Replace semver-like tokens with a placeholder token.
   - Collapse whitespace.
4) **Classify** failure type:
   - Build-tool (e.g., tsc, vite, webpack).
   - Package manager (pnpm/yarn/npm) including peer conflicts.
   - Lint/format (eslint, prettier).
   - Test (vitest/jest/playwright).
   - Runtime (node version mismatch, ESM/CJS loader).
   - Infra (cache miss/permissions/timeout).

## Structured Output (for memory `error.capture`)
```json
{
  "kind": "<Build|Lint|Test|PkgMgr|Runtime|Infra>",
  "message": "<primary error line>",
  "detector": "<ci-system>/<tool>",
  "normalizedKey": "<derived key>",
  "job": { "name": "<job>", "id?": "<id>", "url?": "<url>" },
  "step?": "<failing step name>"
}
## Special Cases

Peer dependency conflicts: capture required vs. found semver ranges.

Node/toolchain mismatch: capture requested vs. actual versions.

Flakes/timeouts: treat as Warning, not Error, unless deterministic.

## 

If no actionable primary error is found, emit a warning.capture with reason UnknownPrimaryError and request a re-run with increased verbosity.
