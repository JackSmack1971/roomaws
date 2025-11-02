# .roo/rules-security-auditor/40-memory-io.md
> Exact Memory MCP patterns for this mode

## Read First
- By signature: open `err#<normalizedKey>` (e.g., `cve:pkg@ver`, `codeql:<rule-id>`, `semgrep:<rule-id>`), traverse to `(:Fix)-[:RESOLVES]->(:Error)` and `(:Fix)-[:DERIVED_FROM]->(:Doc)`.
- By dependency: from `dep#<name>@<ver?>` list linked Errors and Fixes.
- By command: from `cmd#<canonical>#<fp8>` surface prior tool failures.

## Write After (idempotent upserts via @roo/memory-hooks.ts)
- `command.exec` for each run `{cmd,cwd?,exitCode,durationMs?,stdoutHead?,stderrHead?}`.
- `warning.capture` for low/medium severity or config gaps; `error.capture` for high/critical or easily exploitable items. Normalize keys.
- `doc.note` for artifact pointers: `sbom.json`, `grype.json|trivy.json`, `codeql.sarif`, `semgrep.json`.
- `Dependency` nodes for packages/images with links: `Error CAUSED_BY Dependency`.
- `fix.apply` with `{strategy, changes[], result}`; link **DERIVED_FROM** docs.

## Stable Names
- `cmd#<canonical>#<fp8>` · `run#<iso>#<fp8>` · `err#warn#<normalizedKey>` · `dep#name@ver` · `doc#sha256(path|url)` · `fix#<issue>#<sha8>`
