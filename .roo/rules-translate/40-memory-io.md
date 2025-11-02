# .roo/rules-translate/20-memory-integration.md
> What to persist to the Memory MCP during translation operations, validation runs, and localization fixes.

## Observation Envelopes
Stringify and attach to nodes as observations:
- `command.exec` — `{ cmd, cwd?, exitCode, durationMs?, stdoutHead?, stderrHead? }`
- `error.capture` — `{ kind:"TranslationError"|..., message, detector:"find-missing-translations", normalizedKey }`
- `warning.capture` — `{ kind:"TranslationWarning"|..., message, detector:"find-missing-translations", normalizedKey }`
- `fix.apply` — `{ strategy, changes[], result }`
- Optional `doc.note` — `{ url, title?, site?, author?, published_at?, accessed_at, archive_url?, excerpt? }`

> Use stable names/keys and **read-before-write** per `10-idempotency-policy.md`.

## When to Write
1) **After every translation validation command** (find-missing-translations):
   - Create/upsert `Run`, `Command`, optional `Tool` (`node@<ver>`), and `Mode`.
   - Link: `Run EXECUTES Command`; `Run PERFORMED_BY Mode`; `Run USES Tool`.
2) **On translation errors/missing strings**:
   - Derive `normalizedKey` from the primary missing translation (e.g., "missing-key-core-errors").
   - Upsert `Error` as `err#<normalizedKey>` and attach `error.capture` (`detector: "find-missing-translations"`).
   - Optional dependency edges if error cites a locale file (`Error ABOUT Concept`).
3) **On translation fixes**:
   - Upsert `Fix` with `fix.apply { strategy, changes[], result }`.
   - If research informed the translation, upsert `Doc` and link `Fix DERIVED_FROM Doc` (and `Doc REFERENCES Concept` as needed).
4) **Touched files**:
   - For edits made to translation files, add `Run TOUCHES File` for each changed locale file (path-stable node naming).

## Minimal Write Sequence (per event)
1. `open_nodes(names)` → compute missing entities.
2. `create_entities(missing)` → only for missing.
3. `add_observations(...)` → envelopes on existing nodes.
4. `create_relations([...])` → active-voice, directional.

## Data Hygiene
- Truncate `stdoutHead`/`stderrHead` (~8k each).
- Never include secrets or full artifacts; link a file path instead.
- Prefer **small, typed** JSON over raw blob text.

## Ground Rules (Translation specifics)
- Confirm translation scripts are available; otherwise record a `warning.capture` for missing tools.
- Encourage systematic translation workflows with validation at each step.