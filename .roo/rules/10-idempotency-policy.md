# 10-idempotency-policy.md
> Applies to all modes. Enforced by convention in `.roomodes` and executed via `use_mcp_tool` against the Memory MCP.

## Goals
Make every memory write **safe to retry** and **harmless to repeat** so modes can run with at-least-once semantics without creating duplicates.

## Golden Rules
1. **Design for idempotence:** The same logical write may occur multiple times; the graph state **must** be equivalent to a single write.
2. **Upsert, don’t append:** Treat entities/relations as **upserts** keyed by **stable identifiers**, not fire-and-forget inserts.
3. **Reads guard writes:** Always **read before write** (or use exact-name opens) to decide **create vs. skip**.

## Stable Keys (required)
Use deterministic names/keys across the swarm:
- **Run:** `run#<ISO8601>#<fp8>` where `fp8 = sha256(cmd|cwd|exit|stdoutHead|stderrHead).slice(0,8)`
- **Command:** `cmd#<canonical-cmd>#<fp8>` (collapse whitespace; trim to 120 chars)
- **Issue:**  
  - Errors: `err#<normalizedKey>`  
  - Warnings: `warn#<normalizedKey>`  
  `normalizedKey = lowercase(message) → strip hashes → collapse semver → squeeze spaces`
- **Dependency:** `dep#<name>@<version?>`
- **Fix:** `fix#<issueName>#<sha8(JSON(strategy,changes))>`
- **Doc:** `doc#<sha256(url)>`
- **Mode/Tool/File/Concept:** `mode#<slug@ver?>`, `tool#<name@ver?>`, `file#<path>`, `concept#<slug>`

## Observation Envelope (stringified JSON on nodes)
```json
{
  "type": "command.exec|error.capture|warning.capture|fix.apply|doc.note|run.summary",
  "ts": "<ISO8601>", "mode": "<slug>@<ver?>",
  "repo": "<owner/repo or path>", "branch": "<git-branch>",
  "fingerprint": "<sha256>", "data": { /* type-specific */ }
}
````

* Keep `stdoutHead`/`stderrHead` to ~8k each. Never dump entire logs by default.

## Write Path (idempotent)

1. **Open by exact name:** `open_nodes(names:[...])` → build `existingNames`.
2. **Create missing entities only:** `create_entities(missing)`.
3. **Add observations:** `add_observations({entityName, observation})` — attach envelopes to the **existing** node. Do not create new nodes for observations.
4. **Create relations (best-effort):** `create_relations([...])`. Relations are named in **active voice** and may be deduplicated server-side.
5. **Never** delete on failure paths; prefer additional observations (diagnostics) to preserve auditability.

## Relation Vocabulary (canonical, directional)

* `Run EXECUTES Command`
* `Command EMITS Error|Warning`
* `Error CAUSED_BY Dependency`
* `Fix RESOLVES Error` / `Fix MITIGATES Warning`
* `Fix DERIVED_FROM Doc`
* `Doc REFERENCES Concept`
* `Error ABOUT Concept`
* `Run PERFORMED_BY Mode` / `Run USES Tool` / `Run TOUCHES File`

## Retry & Backoff (client policy)

* Assume **transient failures**; perform bounded retries with **exponential backoff + jitter**.
* Default: 3 attempts, base 250 ms, **full jitter**, cap 4 s. Abort on non-retryable errors (4xx schema/validation).
* Do **not** retry in multiple layers concurrently (avoid retry storms). Centralize retries in the memory hooks.

## Concurrency & Exactly-Once Equivalence

* Accept that execution is **at-least-once**; achieve **exactly-once equivalence** via stable keys + read-before-write.
* Prefer **open-then-create** patterns over fuzzy search for idempotency decisions.
* If two writers race, it’s acceptable for the second writer to **skip** creation after seeing the first writer’s result.

## Logging & Cost Discipline

* Use **structured JSON logs** with `level`, `event`, `key`, `durationMs`, `retries`.
* Sample non-error events; **always** keep `ERROR`/`WARN`.
* Never log secrets. Truncate payloads; hash or redact long identifiers.

## Validation Gates

* Before `create_entities`: ensure `name`/`type` present; envelope parses; `type` ∈ allowed set.
* Before `create_relations`: ensure `source`/`target` exist (open check) and `relationType` ∈ canonical list.
* Before `add_observations`: JSON parse check; envelope `type` is valid.

## Anti-Patterns (forbidden)

* Generating random names for deterministic entities.
* Append-only “error spam” nodes per attempt.
* Retrying non-idempotent operations without keys or guards.
* Writing full stdout/stderr blobs to observations by default.

```

**Why these rules (sources):**  
- Jittered backoff avoids thundering herds during retries and is an AWS-recommended pattern. :contentReference[oaicite:0]{index=0}  
- Idempotency keys and read-before-write upserts are standard for exactly-once **equivalence** in distributed systems (Stripe & general API design). :contentReference[oaicite:1]{index=1}  
- “At-least-once + idempotent processing ⇒ exactly-once effect” is a core distributed-systems approach. :contentReference[oaicite:2]{index=2}  
- Structured JSON logging and sampling keep signal high and cost/noise low. :contentReference[oaicite:3]{index=3}

If you want, I can generate companion files `20-evidence-and-citations.md` and `30-memory-reads.md` to complete the shared rule set.
::contentReference[oaicite:4]{index=4}
```
