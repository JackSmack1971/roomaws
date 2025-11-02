# .roo/rules-pr-fixer/30-memory-writes.md
> Persist CI parsing results, applied fixes, and evidence into the hive-mind.

## When to Write
- After CI parsing (even before fixing): record the normalized error/warning once.
- After applying a remediation: record the fix and any evidence.
- After successful re-run: record final outcome in the fix observation.

## Entities & Relations
- `Run` (this PR cycle) — `EXECUTES` → `Command` (e.g., `pnpm test`, `tsc`, `vite build`)
- `Command` — `EMITS` → `Error` or `Warning`
- `Error` — `CAUSED_BY` → `Dependency` (optional)
- `Fix` — `RESOLVES` → `Error`  |  `Fix` — `MITIGATES` → `Warning`
- `Fix` — `DERIVED_FROM` → `Doc`

## Observations
Complete envelope examples following hivemind contract:

**error.capture**:
```json
{
  "type": "error.capture",
  "ts": "2025-11-01T13:22:14.646Z",
  "mode": "merge-resolver@1.0",
  "repo": "owner/repo-name",
  "branch": "feature/new-component",
  "fingerprint": "3456789012abcdef...",
  "data": {
    "kind": "TypeScriptError",
    "message": "Cannot find module '@/utils/helpers' or its corresponding type declarations",
    "detector": "tsc",
    "normalizedKey": "typescript-module-not-found",
    "job": {
      "name": "CI / Build",
      "id": "123456789",
      "url": "https://github.com/owner/repo-name/actions/runs/123456789"
    },
    "step": "Type Check"
  }
}
```

**warning.capture**:
```json
{
  "type": "warning.capture",
  "ts": "2025-11-01T13:22:14.646Z",
  "mode": "merge-resolver@1.0",
  "repo": "owner/repo-name",
  "branch": "feature/new-component",
  "fingerprint": "4567890123abcdef...",
  "data": {
    "kind": "ESLintWarning",
    "message": "Unexpected any type, prefer explicit types",
    "detector": "eslint",
    "normalizedKey": "typescript-any-type-warning",
    "job": {
      "name": "CI / Lint",
      "id": "123456790",
      "url": "https://github.com/owner/repo-name/actions/runs/123456790"
    },
    "step": "Lint Code"
  }
}
```

**fix.apply**:
```json
{
  "type": "fix.apply",
  "ts": "2025-11-01T13:22:14.646Z",
  "mode": "merge-resolver@1.0",
  "repo": "owner/repo-name",
  "branch": "feature/new-component",
  "fingerprint": "5678901234abcdef...",
  "data": {
    "strategy": "Replaced absolute import with relative import to resolve module resolution conflict",
    "changes": [
      {
        "file": "src/components/NewButton.tsx",
        "op": "update",
        "path": "import statement line 1",
        "from": "import { formatDate } from '@/utils/helpers'",
        "to": "import { formatDate } from '../../utils/helpers'",
        "value": null
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
  "mode": "merge-resolver@1.0",
  "repo": "owner/repo-name",
  "branch": "feature/new-component",
  "fingerprint": "6789012345abcdef...",
  "data": {
    "url": "https://nextjs.org/docs/advanced-features/module-path-mapping",
    "title": "Next.js Module Path Mapping",
    "site": "nextjs.org",
    "author": "Vercel",
    "published_at": "2024-01-15",
    "accessed_at": "2025-11-01T13:22:14.646Z",
    "archive_url": "https://web.archive.org/web/20241101132214/https://nextjs.org/docs/advanced-features/module-path-mapping",
    "excerpt": "The @ alias points to the src directory, but in monorepos or complex project structures, relative imports may be more reliable for avoiding path resolution issues."
  }
}
```

## Idempotent Write Path
1) `open_nodes(names)` → compute missing.
2) `create_entities(missing)` → only missing.
3) `add_observations` → attach envelopes to existing nodes.
4) `create_relations([...])` → active voice, directional.
5) Re-run recordings: append to the same `Fix` observation with updated `result`.

## Hygiene & Privacy
- Truncate captured logs to ~8k head; never store full artifacts or secrets.
- Use stable names (`err#<normalizedKey>`, `fix#<issue>#<sha8>`, `doc#<sha256(url)>`).
- If failure was a **flake**, record a `warning.capture` with key `ci-flake-<tool>-<symptom>` and note mitigations (retries, timeouts, resource class).

## Done Criteria
- Required checks are **green**.
- Memory contains the **error key**, chosen **Fix**, and **Doc** evidence (if any).
- Subsequent occurrences of the same key recall this fix automatically.
