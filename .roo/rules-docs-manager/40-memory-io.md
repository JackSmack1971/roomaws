# .roo/rules-docs-manager/20-memory-integration.md
> What to persist to the Memory MCP during documentation tasks, failures, and updates.

## Observation Envelopes
Stringify and attach to nodes as observations following the hivemind contract:

### Complete Envelope Examples

**command.exec**:
```json
{
  "type": "command.exec",
  "ts": "2025-11-01T13:22:14.646Z",
  "mode": "docs-manager@1.0",
  "repo": "owner/repo-name",
  "branch": "main",
  "fingerprint": "a1b2c3d4e5f67890...",
  "data": {
    "cmd": "npx typedoc --out docs/api src/",
    "cwd": "/path/to/project",
    "exitCode": 0,
    "durationMs": 2450,
    "stdoutHead": "Documentation generated at docs/api/index.html",
    "stderrHead": null
  }
}
```

**error.capture**:
```json
{
  "type": "error.capture",
  "ts": "2025-11-01T13:22:14.646Z",
  "mode": "docs-manager@1.0",
  "repo": "owner/repo-name",
  "branch": "main",
  "fingerprint": "b2c3d4e5f6789012...",
  "data": {
    "kind": "DocFailure",
    "message": "TypeDoc failed to parse JSDoc comments in src/utils.ts",
    "detector": "extractor",
    "normalizedKey": "typedoc-jsdoc-parse-failure"
  }
}
```

**fix.apply**:
```json
{
  "type": "fix.apply",
  "ts": "2025-11-01T13:22:14.646Z",
  "mode": "docs-manager@1.0",
  "repo": "owner/repo-name",
  "branch": "main",
  "fingerprint": "c3d4e5f678901234...",
  "data": {
    "strategy": "Updated JSDoc syntax to TypeDoc-compatible format",
    "changes": [
      {
        "file": "src/utils.ts",
        "op": "update",
        "path": "line 15",
        "from": "@param {string} input",
        "to": "@param input - The input string to process"
      }
    ],
    "result": "applied"
  }
}
```

**doc.note**:
```json
{
  "type": "doc.note",
  "ts": "2025-11-01T13:22:14.646Z",
  "mode": "docs-manager@1.0",
  "repo": "owner/repo-name",
  "branch": "main",
  "fingerprint": "d4e5f67890123456...",
  "data": {
    "url": "https://typedoc.org/guides/doccomments/",
    "title": "TypeDoc Documentation Comments Guide",
    "site": "typedoc.org",
    "author": "TypeDoc Team",
    "published_at": "2024-03-15",
    "accessed_at": "2025-11-01T13:22:14.646Z",
    "archive_url": "https://web.archive.org/web/20241101132214/https://typedoc.org/guides/doccomments/",
    "excerpt": "TypeDoc supports most JSDoc tags but has specific syntax requirements for parameter documentation."
  }
}
```

> Use stable names/keys and **read-before-write** per `10-idempotency-policy.md`.

## When to Write
1) **After every documentation command** (extract, verify):
   - Create/upsert `Run`, `Command`, optional `Tool` (`extractor@<ver>`), and `Mode`.
   - Link: `Run EXECUTES Command`; `Run PERFORMED_BY Mode`; `Run USES Tool`.
2) **On documentation failures**:
   - Derive `normalizedKey` from the primary issue (e.g., "api-doc-outdated").
   - Upsert `Error` as `err#<normalizedKey>` and attach `error.capture` (`detector: "extractor"`).
   - Optional dependency edges if failure cites a package (`Error CAUSED_BY Dependency`).
3) **On successful updates**:
   - Upsert `Fix` with `fix.apply { strategy, changes[], result }`.
   - If research informed the update, upsert `Doc` and link `Fix DERIVED_FROM Doc` (and `Doc REFERENCES Concept` as needed).
4) **Touched files**:
   - For edits made to documentation, add `Run TOUCHES File` for each changed path (path-stable node naming).

## Minimal Write Sequence (per event)
1. `open_nodes(names)` → compute missing entities.
2. `create_entities(missing)` → only for missing.
3. `add_observations(...)` → envelopes on existing nodes.
4. `create_relations([...])` → active-voice, directional.

## Data Hygiene
- Truncate `stdoutHead`/`stderrHead` (~8k each).
- Never include secrets or full artifacts; link a file path instead.
- Prefer **small, typed** JSON over raw blob text.

## Ground Rules (Documentation specifics)
- Confirm documentation tools are available; otherwise record a `error.capture` for missing tools.
- Encourage accurate and up-to-date documentation.