# .roo/rules-mode-writer/80-memory-io.md
> Exact, efficient Memory MCP usage for Mode Writer (idempotent, shared across swarm).

## Read First
1) **Docs**: open `doc#<sha256(url|path)>` for prior mode templates and examples.
2) **Command lens**: from `cmd#<canonical>#<fp8>` roll up past YAML/regex validation failures.
3) **Error/Warning**: `err#warn#<normalizedKey>` for schema/permission mistakes and their fixes.

## Write After
- `command.exec` for validation runs `{cmd,cwd?,exitCode,durationMs?,stdoutHead?,stderrHead?}` (truncate ~8k).
- `warning.capture` for schema/regex issues with `normalizedKey` (e.g., `yaml:missing-field:groups`).
- `fix.apply` summarizing changes `{strategy,changes[],result}`.
- `doc.note` with artifact pointers (final YAML path, rules map).

## Stable Names
- Runs/Commands: `run#<iso>#<fp8>`, `cmd#<canonical>#<fp8>`
- Docs: `doc#<sha256(url|path)>`
- Issues/Warnings: `err#warn#<normalizedKey>`

## Normalized Key
- Lowercase → strip hashes/paths/timestamps → collapse semver → squeeze spaces.

## Safety
- **Open‑then‑create**; skip if exists. Never store secrets or whole files.
