# .roo/rules-spec-writer/40-memory-io.md
> Exact, efficient Memory MCP usage for Spec-Writer (idempotent, shared across swarm).

## Read First
1) **Docs**: open `doc#<sha256(url|path)>` for prior spec templates and examples.
2) **Command lens**: from `cmd#<canonical>#<fp8>` roll up past YAML/clause validation failures.
3) **Error/Warning**: `err#warn#<normalizedKey>` for schema/spec mistakes and their fixes.

## Write After
- `command.exec` for validation runs `{cmd,cwd?,exitCode,durationMs?,stdoutHead?,stderrHead?}` (truncate ~8k).
- `warning.capture` for schema/clause issues with `normalizedKey` (e.g., `yaml:missing-field:owners`).
- `fix.apply` summarizing changes `{strategy,changes[],result}`.
- `doc.note` with artifact pointers (final spec path, clause map).

## Stable Names
- Specs: `spec#<slug>@<version>` (e.g., `spec#payment-api@v1.2.3`)
- Clauses: `clause#<specSlug>#<clauseId>` (e.g., `clause#payment-api#sy73`)
- Tests: `test#<clauseId>` (e.g., `test#sy73`)

## Relations (active voice)
- `Spec DERIVES_FROM Doc` (spec informed by documentation)
- `Clause TESTS Spec` (clause has test file)
- `Fix RESOLVES SpecIssue` (fix addresses spec problem)
- `Spec REFERENCES Concept` (spec discusses concept)

## Write Path (idempotent)

1. **Open by exact name:** `open_nodes(names:[...])` → build `existingNames`.
2. **Create missing entities only:** `create_entities(missing)`.
3. **Add observations:** `add_observations({entityName, observation})` — attach envelopes to existing node.
4. **Create relations (best-effort):** `create_relations([...])`. Relations are named in active voice and may be deduplicated server-side.
5. **Never delete on failure paths;** prefer additional observations (diagnostics) to preserve auditability.

## Observation Envelope (stringified JSON on nodes)
```json
{
  "type": "command.exec|error.capture|warning.capture|fix.apply|doc.note|spec.created",
  "ts": "<ISO8601>", "mode": "spec-writer@v1.0", "repo": "...", "branch": "...",
  "fingerprint": "<sha256>", "data": { /* type-specific */ }
}
```

## Fallback Strategy (no exact hit)
1) **Soft match**: search observations for the spec slug or clause ID.
2) **Neighbor signal**: start from `:Spec` or `:Doc` context nearest to the current spec.
3) **Concept expansion**: if the spec is tagged with `:Concept`, traverse `(:Doc)-[:REFERENCES]->(:Concept)` to pull authoritative docs.

## Safety
- **Open-then-create**; skip if exists. Never store secrets or entire specs.
- Use `normalizedKey = lowercase(message) → strip hashes → collapse semver → squeeze spaces` for errors/warnings.