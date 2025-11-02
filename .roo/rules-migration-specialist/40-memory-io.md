# .roo/rules-migration-specialist/20-memory-integration.md
> What to persist to the Memory MCP during migration runs, failures, and fixes.

## Observation Envelopes
Stringify and attach to nodes as observations:
- `command.exec` — `{ cmd, cwd?, exitCode, durationMs?, stdoutHead?, stderrHead? }`
- `error.capture` — `{ kind:"MigrationFailure"|..., message, detector:"codemod", normalizedKey }`
- `fix.apply` — `{ strategy, changes[], result }`
- Optional `doc.note` — `{ url, title?, site?, author?, published_at?, accessed_at, archive_url?, excerpt? }`

> Use stable names/keys and **read-before-write** per `10-idempotency-policy.md`.

## When to Write
1) **After every migration command** (codemod, build):
   - Create/upsert `Run`, `Command`, optional `Tool` (`react-codemod@<ver>`), and `Mode`.
   - Link: `Run EXECUTES Command`; `Run PERFORMED_BY Mode`; `Run USES Tool`.
2) **On migration failures**:
   - Derive `normalizedKey` from the primary error (e.g., "react-18-migration-build-error").
   - Upsert `Error` as `err#<normalizedKey>` and attach `error.capture` (`detector: "codemod"`).
   - Optional dependency edges if failure cites a package (`Error CAUSED_BY Dependency`).
3) **On successful migrations**:
   - Upsert `Fix` with `fix.apply { strategy, changes[], result }`.
   - If research informed the fix, upsert `Doc` and link `Fix DERIVED_FROM Doc` (and `Doc REFERENCES Concept` as needed).
4) **Touched files**:
   - For edits made during migration, add `Run TOUCHES File` for each changed path (path-stable node naming).

## Minimal Write Sequence (per event)
1. `open_nodes(names)` → compute missing entities.
2. `create_entities(missing)` → only for missing.
3. `add_observations(...)` → envelopes on existing nodes.
4. `create_relations([...])` → active-voice, directional.

## Data Hygiene
- Truncate `stdoutHead`/`stderrHead` (~8k each).
- Never include secrets or full artifacts; link a file path instead.
- Prefer **small, typed** JSON over raw blob text.

## Ground Rules (Migration specifics)
- Confirm migration tools are available; otherwise record a `error.capture` for missing tools.
- Encourage phased rollouts with rollback plans.