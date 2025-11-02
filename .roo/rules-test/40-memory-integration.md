# .roo/rules-test/20-memory-integration.md
> What to persist to the Memory MCP during test runs, failures, and remediations.

## Observation Envelopes
Stringify and attach to nodes as observations:
- `command.exec` — `{ cmd, cwd?, exitCode, durationMs?, stdoutHead?, stderrHead? }`
- `error.capture` — `{ kind:"TestFailure"|..., message, detector:"vitest", normalizedKey }`
- `warning.capture` — `{ kind, message, detector:"vitest", normalizedKey }`
- `fix.apply` — `{ strategy, changes[], result }`
- Optional `doc.note` — `{ url, title?, site?, author?, published_at?, accessed_at, archive_url?, excerpt? }`

> Use stable names/keys and **read-before-write** per `10-idempotency-policy.md`.

## When to Write
1) **After every test command** (run/coverage):
   - Create/upsert `Run`, `Command`, optional `Tool` (`vitest@<ver>`), and `Mode`.
   - Link: `Run EXECUTES Command`; `Run PERFORMED_BY Mode`; `Run USES Tool`.
2) **On failing/errored tests**:
   - Derive `normalizedKey` from the *primary* failure message (lowercase → strip hashes → collapse semver → squeeze spaces).
   - Upsert `Error` as `err#<normalizedKey>` and attach `error.capture` (`detector: "vitest"`).
   - Optional dependency edges if failure cites a package (`Error CAUSED_BY Dependency`).
3) **On warnings/flakes**:
   - Upsert `Warning` as `warn#<normalizedKey>`; attach `warning.capture` (e.g., timeout/flaky pattern).
4) **On remediation**:
   - Upsert `Fix` with `fix.apply { strategy, changes[], result }`.
   - If research informed the fix, upsert `Doc` and link `Fix DERIVED_FROM Doc` (and `Doc REFERENCES Concept` as needed).
5) **Touched files**:
   - For edits made to stabilize tests, add `Run TOUCHES File` for each changed path (path-stable node naming).

## Minimal Write Sequence (per event)
1. `open_nodes(names)` → compute missing entities.  
2. `create_entities(missing)` → only for missing.  
3. `add_observations(...)` → envelopes on existing nodes.  
4. `create_relations([...])` → active-voice, directional.

## Data Hygiene
- Truncate `stdoutHead`/`stderrHead` (~8k each).  
- Never include secrets or full artifacts; link a file path instead.  
- Prefer **small, typed** JSON over raw blob text.

## Ground Rules (Vitest specifics)
- Confirm tests are in `*.test.*` / `*.spec.*`; otherwise record a `warning.capture` for misplacement.
- Encourage running via local package script (captures correct config/env).

## Read Patterns
1) **Exact key first** — if you have `normalizedKey`, open `err#<normalizedKey>` directly:
   `open_nodes(["err#<key>"])` → if found, traverse for fixes/docs.
2) **Selective traversal** — from `:Error` follow:
   `(:Fix)-[:RESOLVES]->(:Error)` and optional `(:Fix)-[:DERIVED_FROM]->(:Doc)`.
3) **Fallback search** — if no exact error node, `search_nodes("type:Error normalizedKey:<key>")`, then open and traverse.

> Keep traversals tight and limit early (top-3) to reduce latency and token load; return only fields you'll print.

## Canonical Queries (logical recipes)
### A) Prior fixes for this failure signature
START error = (:Error { name: "err#<normalizedKey>" })
FOLLOW (:Fix)-[:RESOLVES]->(error)
OPTION (:Fix)-[:DERIVED_FROM]->(doc:Doc)
RETURN top 3 fixes with doc metadata (title, site, accessed_at, archive_url)

### B) Flake patterns for this suite/command
START cmd = (:Command { name: "cmd#vitest <args>#<fp8>" }) OR by hash prefix
FOLLOW cmd-[:EMITS]->(w:Warning)
GROUP by w.normalizedKey → COUNT
RETURN top flake keys + representative Fix/mitigation

### C) Dependency-rooted failures
START dep = (:Dependency { name:"<pkg>", version:"<ver?>" })
FOLLOW (e:Error)-[:CAUSED_BY]->(dep)
FOLLOW (f:Fix)-[:RESOLVES]->(e)
RETURN minimal fix set seen to resolve such errors historically

## Ranking & Summarization
- Rank candidates by **recency**, **success ratio**, and **has evidence** (`DERIVED_FROM Doc`).
- Summarize to **≤200 tokens**; include node names (IDs) for drill-down.

## Determinism & Safety
- Reads **never** mutate graph.
- If ties, sort by deterministic keys (`name`, `ts`).
- Cache (`normalizedKey` → fix IDs) within the current task to avoid repeated reads.

## Vitest Context Checks
- If the project lacks a local `vitest` script, suggest adding `"test": "vitest"` in `package.json` and record a `warning.capture` for missing script.
- If tests aren't in `*.test.*` / `*.spec.*`, surface a migration suggestion instead of brittle glob hacks.
