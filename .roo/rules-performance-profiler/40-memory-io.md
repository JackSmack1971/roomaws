# .roo/rules-performance-profiler/20-memory-integration.md
> What to persist to the Memory MCP during profiling runs, regressions, and optimizations.

## Observation Envelopes
Stringify and attach to nodes as observations:
- `command.exec` — `{ cmd, cwd?, exitCode, durationMs?, stdoutHead?, stderrHead? }`
- `warning.capture` — `{ kind:"PerformanceRegression"|..., message, detector:"lighthouse", normalizedKey }`
- `fix.apply` — `{ strategy, changes[], result }`
- Optional `doc.note` — `{ url, title?, site?, author?, published_at?, accessed_at, archive_url?, excerpt? }`

> Use stable names/keys and **read-before-write** per `10-idempotency-policy.md`.

## When to Write
1) **After every profiling command** (lighthouse, benchmark):
   - Create/upsert `Run`, `Command`, optional `Tool` (`lighthouse@<ver>`), and `Mode`.
   - Link: `Run EXECUTES Command`; `Run PERFORMED_BY Mode`; `Run USES Tool`.
2) **On regressions/warnings**:
   - Derive `normalizedKey` from the primary metric (e.g., "lcp-regression").
   - Upsert `Warning` as `warn#<normalizedKey>` and attach `warning.capture` (`detector: "lighthouse"`).
   - Optional dependency edges if regression cites a package (`Warning CAUSED_BY Dependency`).
3) **On optimizations**:
   - Upsert `Fix` with `fix.apply { strategy, changes[], result }`.
   - If research informed the fix, upsert `Doc` and link `Fix DERIVED_FROM Doc` (and `Doc REFERENCES Concept` as needed).
4) **Touched files**:
   - For edits made to optimize, add `Run TOUCHES File` for each changed path (path-stable node naming).

## Minimal Write Sequence (per event)
1. `open_nodes(names)` → compute missing entities.
2. `create_entities(missing)` → only for missing.
3. `add_observations(...)` → envelopes on existing nodes.
4. `create_relations([...])` → active-voice, directional.

## Data Hygiene
- Truncate `stdoutHead`/`stderrHead` (~8k each).
- Never include secrets or full artifacts; link a file path instead.
- Prefer **small, typed** JSON over raw blob text.

## Ground Rules (Performance specifics)
- Confirm profiling tools are available; otherwise record a `warning.capture` for missing tools.
- Encourage reproducible benchmarks with consistent environments.