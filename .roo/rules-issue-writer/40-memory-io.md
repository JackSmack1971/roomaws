# .roo/rules-issue-writer/70-memory-io.md
> Exact, efficient Memory MCP usage for Issue Writer.

## Read First (decision-oriented)
1) **Known signatures**: open `err#<normalizedKey>` → gather prior fixes/notes to pre-fill context and labels.
2) **Command lens**: from `cmd#<canonical>#<fp8>`, surface past gh/git failures (auth, permissions) to preempt errors.
3) **Docs lens**: from `doc#<sha256(url)>`, recall repo template details previously parsed.

## Write After (idempotent)
- `command.exec` for gh/git runs `{cmd, exitCode, durationMs?, stdoutHead?, stderrHead?}` (truncate ~8k).
- `warning.capture` for duplicates or template-missing conditions using `normalizedKey`.
- `doc.note` for template chosen, labels applied, draft path, final URL.

## Stable Names
- Commands/Runs: `cmd#<canonical>#<fp8>`, `run#<iso>#<fp8>`
- Issues/Warnings: `err#<normalizedKey>`, `warn#<normalizedKey>`
- Docs: `doc#<sha256(url)>`

## Normalized Key
- Lowercase → strip hashes/paths/timestamps → collapse semver → squeeze spaces (canonical de-dup key across the swarm).

## Safety
- Always open-then-create; skip if exists.
- Never store secrets or full logs; keep heads and file references only.
