# .roo/rules-mode-validator/20-memory-integration.md
> What to persist to the Memory MCP during validation runs, failures, and fixes.

## Observation Envelopes
Stringify and attach to nodes as observations:
- `command.exec` — `{ cmd, cwd?, exitCode, durationMs?, stdoutHead?, stderrHead? }`
- `error.capture` — `{ kind:"ValidationFailure"|..., message, detector:"ajv", normalizedKey }`
- `fix.apply` — `{ strategy, changes[], result }`
- Optional `doc.note` — `{ url, title?, site?, author?, published_at?, accessed_at, archive_url?, excerpt? }`

> Use stable names/keys and **read-before-write** per `10-idempotency-policy.md`.

## When to Write
1) **After every validation command** (schema check, lint):
   - Create/upsert `Run`, `Command`, optional `Tool` (`ajv@<ver>`), and `Mode`.
   - Link: `Run EXECUTES Command`; `Run PERFORMED_BY Mode`; `Run USES Tool`.
2) **On validation failures**:
   - Derive `normalizedKey` from the primary error (e.g., "mode-schema-invalid").
   - Upsert `Error` as `err#<normalizedKey>` and attach `error.capture` (`detector: "ajv"`).
   - Optional dependency edges if failure cites a package (`Error CAUSED_BY Dependency`).
3) **On successful validations**:
   - Upsert `Fix` with `fix.apply { strategy, changes[], result }`.
   - If research informed the fix, upsert `Doc` and link `Fix DERIVED_FROM Doc` (and `Doc REFERENCES Concept` as needed).
4) **Touched files**:
   - For edits made to fix modes, add `Run TOUCHES File` for each changed path (path-stable node naming).

## Minimal Write Sequence (per event)
1. `open_nodes(names)` → compute missing entities.
2. `create_entities(missing)` → only for missing.
3. `add_observations(...)` → envelopes on existing nodes.
4. `create_relations([...])` → active-voice, directional.

## Data Hygiene
- Truncate `stdoutHead`/`stderrHead` (~8k each).
- Never include secrets or full artifacts; link a file path instead.
- Prefer **small, typed** JSON over raw blob text.

## Ground Rules (Validation specifics)
- Confirm validation tools are available; otherwise record a `error.capture` for missing tools.
- Encourage schema compliance and consistency checks.