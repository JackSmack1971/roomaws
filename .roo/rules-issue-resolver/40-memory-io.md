# .roo/rules-issue-resolver/40-memory-io.md
> Exact, efficient Memory MCP usage for Issue Resolver: read patterns, write patterns, entity schema, and relation vocabulary.

## Read Patterns
1) **Exact key**: if a failure signature exists, open `err#<normalizedKey>` → traverse `(:Fix)-[:RESOLVES]->(:Error)` (+ optional `(:Fix)-[:DERIVED_FROM]->(:Doc)`).
2) **Command lens**: from `cmd#<canonical>#<fp8>`, traverse to `Error|Warning` and roll up top keys.
3) **Dependency lens**: from `dep#<name>@<ver?>`, find linked Errors and their Fixes.
- **Limit** to top-3; project only fields you'll print (strategy, minimal change set, evidence titles).

## Write Patterns
### When to Write
1) **After every investigation command** (debug, test):
   - Create/upsert `Run`, `Command`, optional `Tool` (`debugger@<ver>`), and `Mode`.
   - Link: `Run EXECUTES Command`; `Run PERFORMED_BY Mode`; `Run USES Tool`.
2) **On issue failures**:
   - Derive `normalizedKey` from the primary issue (e.g., "null-pointer-exception").
   - Upsert `Error` as `err#<normalizedKey>` and attach `error.capture` (`detector: "debugger"`).
   - Optional dependency edges if failure cites a package (`Error CAUSED_BY Dependency`).
3) **On successful fixes**:
   - Upsert `Fix` with `fix.apply { strategy, changes[], result }`.
   - If research informed the fix, upsert `Doc` and link `Fix DERIVED_FROM Doc` (and `Doc REFERENCES Concept` as needed).
4) **Touched files**:
   - For edits made to fix issues, add `Run TOUCHES File` for each changed path (path-stable node naming).

### Minimal Write Sequence (per event)
1. `open_nodes(names)` → compute missing entities.
2. `create_entities(missing)` → only for missing.
3. `add_observations(...)` → envelopes on existing nodes.
4. `create_relations([...])` → active-voice, directional.

### Observation Envelopes
Stringify and attach to nodes as observations:
- `command.exec` — `{ cmd, cwd?, exitCode, durationMs?, stdoutHead?, stderrHead? }`
- `error.capture` — `{ kind:"IssueFailure"|..., message, detector:"debugger", normalizedKey }`
- `fix.apply` — `{ strategy, changes[], result }`
- Optional `doc.note` — `{ url, title?, site?, author?, published_at?, accessed_at, archive_url?, excerpt? }`

### Data Hygiene
- Truncate `stdoutHead`/`stderrHead` (~8k each).
- Never include secrets or full artifacts; link a file path instead.
- Prefer **small, typed** JSON over raw blob text.

## Entity Schema
### Stable Names
- Runs/Commands: `run#<iso>#<fp8>`, `cmd#<canonical>#<fp8>`
- Issues: `err#<normalizedKey>`, `warn#<normalizedKey>`
- Fixes/Docs/Deps: `fix#<issue>#<sha8>`, `doc#<sha256(url)>`, `dep#<name>@<ver?>`

### Normalized Key
- Lowercase → strip hashes/paths/timestamps → collapse semver → squeeze spaces (one canonical string across the swarm).

## Relation Vocabulary
- `Run EXECUTES Command`
- `Command EMITS Error|Warning`
- `Error CAUSED_BY Dependency`
- `Fix RESOLVES Error` / `Fix MITIGATES Warning`
- `Fix DERIVED_FROM Doc`
- `Doc REFERENCES Concept`
- `Error ABOUT Concept`
- `Run PERFORMED_BY Mode` / `Run USES Tool` / `Run TOUCHES File`

## Safety
- Reads never mutate; **open-then-create**; skip if exists.
- Use stable names/keys and **read-before-write** per `10-idempotency-policy.md`.
- Never store secrets or entire logs; reference file paths when needed.
- Confirm debugging tools are available; otherwise record a `error.capture` for missing tools.
- Encourage thorough investigation and testing.