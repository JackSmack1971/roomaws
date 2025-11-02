o# 40-memory-mcp-reference.md
> Comprehensive reference for all Memory MCP integration details. This file consolidates scattered information from other rules files to serve as the central reference for all modes.

## Complete Observation Type Taxonomy

All allowed `type` values in observation envelopes:

- `command.exec` — Records command execution with metadata like cmd, cwd?, exitCode, durationMs?, stdoutHead?, stderrHead?
- `error.capture` — Captures errors with normalizedKey, kind, message, detector, and optional context
- `warning.capture` — Captures warnings with normalizedKey, kind, message, detector, and optional context
- `fix.apply` — Records applied fixes with strategy, changes[], result ("proposed"|"applied")
- `fix.outcome` — Tracks fix effectiveness with status ("verified_successful"|"failed"|"partially_effective"), verificationMethod, durationToVerify, sideEffects, testCoverage
- `doc.note` — Stores documentation metadata with url, title?, site?, author?, published_at?, accessed_at, archive_url?, excerpt?
- `run.summary` — High-level summary of a run's outcomes and key events

## Complete Relation Vocabulary

All canonical relations in active voice:

- `Run EXECUTES Command` — Links a run to the command it executed
- `Command EMITS Error|Warning` — Links commands to errors or warnings they produced
- `Error CAUSED_BY Dependency` — Links errors to dependencies that caused them
- `Fix RESOLVES Error` / `Fix MITIGATES Warning` — Links fixes to the issues they address
- `Fix HAS_OUTCOME Outcome` — Links fixes to their effectiveness outcomes
- `Fix DERIVED_FROM Doc` — Links fixes to documentation that informed them
- `Doc REFERENCES Concept` — Links documentation to concepts it discusses
- `Error ABOUT Concept` — Links errors to concepts they relate to
- `Run PERFORMED_BY Mode` / `Run USES Tool` / `Run TOUCHES File` — Links runs to modes, tools, and files involved

## Entity Schema Reference

Complete schema for all entity types with required/stable key formats:

### Run
- **Key Format**: `run#<ISO8601>#<fp8>` where `fp8 = sha256(cmd|cwd|exit|stdoutHead|stderrHead).slice(0,8)`
- **Purpose**: Represents a single execution session
- **Observations**: `command.exec`, `run.summary`

### Command
- **Key Format**: `cmd#<canonical-cmd>#<fp8>` (collapse whitespace; trim to 120 chars)
- **Purpose**: Represents a specific command that was executed
- **Observations**: `command.exec`

### Error
- **Key Format**: `err#<normalizedKey>` where `normalizedKey = lowercase(message) → strip hashes → collapse semver → squeeze spaces`
- **Purpose**: Represents captured errors
- **Observations**: `error.capture`

### Warning
- **Key Format**: `warn#<normalizedKey>` where `normalizedKey = lowercase(message) → strip hashes → collapse semver → squeeze spaces`
- **Purpose**: Represents captured warnings
- **Observations**: `warning.capture`

### Dependency
- **Key Format**: `dep#<name>@<version?>`
- **Purpose**: Represents software dependencies
- **Observations**: None directly (linked via relations)

### Fix
- **Key Format**: `fix#<issueName>#<sha8(JSON(strategy,changes))>`
- **Purpose**: Represents applied or proposed fixes
- **Observations**: `fix.apply`, `fix.outcome`

### Outcome
- **Key Format**: `outcome#<status>#<sha8(JSON(fixId,verificationMethod,durationToVerify))>`
- **Purpose**: Represents the effectiveness outcome of applied fixes
- **Observations**: `fix.outcome`

### Doc
- **Key Format**: `doc#<sha256(url)>`
- **Purpose**: Represents documentation sources
- **Observations**: `doc.note`

### Mode
- **Key Format**: `mode#<slug@ver?>`
- **Purpose**: Represents execution modes
- **Observations**: None directly (linked via relations)

### Tool
- **Key Format**: `tool#<name@ver?>`
- **Purpose**: Represents tools used in execution
- **Observations**: None directly (linked via relations)

### File
- **Key Format**: `file#<path>`
- **Purpose**: Represents files touched during execution
- **Observations**: None directly (linked via relations)

### Concept
- **Key Format**: `concept#<slug>`
- **Purpose**: Represents abstract concepts referenced in docs/errors
- **Observations**: None directly (linked via relations)

## Fallback Strategies

Guidance when Memory MCP is unavailable:

1. **Soft match**: Search observations for the normalized key or its stem (strip versions/paths)
2. **Neighbor signal**: Start from `:Command` or `:Dependency` context nearest to the current failure
3. **Concept expansion**: If the error is tagged with `:Concept` (e.g., "ts-node loader"), traverse `(:Doc)-[:REFERENCES]->(:Concept)` to pull authoritative docs

For local caching approaches when MCP is down:
- Cache key → top-K fix IDs for the current session
- Expire cache at task boundary
- Use structured JSON logs with level, event, key, durationMs, retries for offline analysis

## Performance Tuning

Query optimization tips, indexing guidance, and cost discipline measures:

### Read Order (must-follow)
1. **Exact keys first (cheap & precise)**: Prefer `open_nodes(names)` or exact-key search when you have stable keys
2. **Selective graph traversals**: Start from most selective node, traverse only necessary hops
3. **Limit early**: Cap K (e.g., top-3 fixes) and project only needed fields
4. **Use indexes-aware predicates**: Query on indexed properties (e.g., `:Error{name}`)

### Performance Guidelines
- **Filter early**: Put most selective predicates at start node; avoid unbounded traversals
- **Avoid Cartesian products**: Join via explicit relationships only
- **Exploit indexes**: Query on indexed properties; planner picks automatically or use hints
- **Return projections**: Only fields actually used (names, ts, key fields)
- **LIMIT early**: Reduce intermediate cardinality; early LIMIT cuts DB hits dramatically

### Cost Discipline
- Use structured JSON logs with `level`, `event`, `key`, `durationMs`, `retries`
- Sample non-error events; always keep ERROR/WARN
- Never log secrets; truncate payloads; hash/redact long identifiers

## Error Handling Patterns

How modes should handle Memory MCP failures, retries, and degraded operation:

### Retry & Backoff (client policy)
- **Transient failures**: Perform bounded retries with exponential backoff + jitter
- **Default**: 3 attempts, base 250ms, full jitter, cap 4s
- **Abort on**: Non-retryable errors (4xx schema/validation)
- **Avoid**: Retry storms by not retrying in multiple layers concurrently
- **Centralize**: Retries in memory hooks

### Concurrency & Exactly-Once Equivalence
- **Accept at-least-once execution**: Achieve exactly-once equivalence via stable keys + read-before-write
- **Prefer open-then-create patterns**: Over fuzzy search for idempotency decisions
- **Race handling**: If two writers race, second writer skips creation after seeing first result

### Validation Gates
- **Before create_entities**: Ensure name/type present; envelope parses; type ∈ allowed set
- **Before create_relations**: Ensure source/target exist (open check); relationType ∈ canonical list
- **Before add_observations**: JSON parse check; envelope type valid

### Anti-Patterns (forbidden)
- Generating random names for deterministic entities
- Append-only "error spam" nodes per attempt
- Retrying non-idempotent operations without keys/guards
- Writing full stdout/stderr blobs to observations by default

### Degraded Operation
When MCP is unavailable:
- Continue execution with local caching
- Log structured events for later replay
- Use fallback strategies for reads
- Defer writes until MCP recovers
- Provide clear user feedback about degraded state