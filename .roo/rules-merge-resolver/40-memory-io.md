# .roo/rules-merge-resolver/40-memory-io.md
> Exact, efficient Memory MCP usage for Merge Resolver: general rules + mode-specific patterns for conflict tracking, resolutions, and pattern learning.

## Read First
1) **Exact key**: open `err#<normalizedKey>` → follow `(:Fix)-[:RESOLVES]->(:Error)` (+ `(:Fix)-[:DERIVED_FROM]->(:Doc)`).
2) **Command lens**: from `cmd#<canonical>#<fp8>` roll‑up prior rebase/merge failures to preempt.
3) **Dependency lens**: from `dep#<name>@<ver?>` inspect related errors/fixes.

## Write After (idempotent)
- `command.exec` on every `git`/`gh` run `{cmd,cwd?,exitCode,durationMs?,stdoutHead?,stderrHead?}` (~8k heads).
- `error.capture`/`warning.capture` for conflict classes (normalized keys per file/marker type).
- `fix.apply` for each file with `{strategy, changes[], result:"resolved"}`; link `Fix DERIVED_FROM Doc` when evidence used.
- `doc.note` for critical references (issue links, PR URLs, commit SHAs).

## Stable Names
- Runs/Commands: `run#<iso>#<fp8>`, `cmd#<canonical>#<fp8>`
- Issues: `err#warn#<normalizedKey>`
- Fixes/Docs/Deps: `fix#<issue>#<sha8>`, `doc#<sha256(url)>`, `dep#<name>@<ver?>`

## Normalized Key
- Lowercase; strip hashes/paths/timestamps; collapse semver; squeeze spaces (swarm‑wide dedup).

## Safety
- Open‑then‑create; skip if exists. Never store secrets or full logs.

## Mode-Specific Patterns

### Conflict Pattern Analysis
**When encountering new merge conflicts:**
```javascript
// Query for similar conflict patterns
const similarConflicts = await search_nodes({
  query: "merge conflict",
  filters: {
    fileType: affectedFileType,
    conflictType: identifiedConflictType,
    resolutionStrategy: potentialStrategies
  }
});

// Get successful resolution approaches
const resolutionHistory = await open_nodes({
  names: similarConflicts.map(c => c.resolutionId)
});
```

### Resolution Strategy Retrieval
**When planning conflict resolution:**
```javascript
// Find proven strategies for specific conflict types
const strategies = await search_nodes({
  query: "conflict resolution strategy",
  filters: {
    conflictType: currentConflictType,
    successRate: ">80%",
    complexity: "similar"
  }
});

// Retrieve strategy details and examples
const strategyDetails = await open_nodes({
  names: strategies.map(s => s.strategyDocId)
});
```

### Conflict Detection Logging
**When conflicts are first detected:**
```javascript
// Log merge conflict discovery
await create_entities({
  entities: [{
    name: `merge-conflict-${prNumber}-${timestamp}`,
    entityType: "MergeConflict",
    observations: [{
      type: "error.capture",
      ts: new Date().toISOString(),
      mode: "merge-resolver",
      data: {
        kind: "MergeConflict",
        message: `Merge conflict detected in ${conflictedFiles.length} files`,
        detector: "git-merge",
        normalizedKey: "merge-conflict-detected",
        context: {
          prNumber: prNumber,
          branch: headBranch,
          baseBranch: baseBranch,
          conflictedFiles: conflictedFiles,
          conflictCount: totalConflicts,
          complexity: conflictComplexity
        }
      }
    }]
  }]
});
```

### Resolution Outcome Documentation
**After successful resolution:**
```javascript
// Document successful merge resolution
await create_entities({
  entities: [{
    name: `merge-resolution-${prNumber}-${timestamp}`,
    entityType: "MergeResolution",
    observations: [{
      type: "fix.apply",
      ts: new Date().toISOString(),
      mode: "merge-resolver",
      data: {
        strategy: "intent-aware-merge",
        changes: resolutionChanges,
        result: "applied",
        context: {
          originalConflict: conflictId,
          resolutionTime: totalResolutionTime,
          filesResolved: resolvedFiles,
          strategiesUsed: uniqueStrategies,
          validationResults: postMergeTests
        }
      }
    }]
  }]
});
```

### Conflict Pattern Documentation
**When identifying new conflict patterns:**
```javascript
// Document recurring conflict pattern
await create_entities({
  entities: [{
    name: `conflict-pattern-${patternId}`,
    entityType: "ConflictPattern",
    observations: [{
      type: "doc.note",
      ts: new Date().toISOString(),
      mode: "merge-resolver",
      data: {
        url: `pattern://${patternId}`,
        title: patternTitle,
        site: "Merge Conflict Patterns",
        author: "Merge Resolver",
        accessed_at: new Date().toISOString(),
        excerpt: patternDescription,
        context: {
          patternType: conflictCategory,
          frequency: occurrenceCount,
          commonFiles: affectedFileTypes,
          resolutionStrategy: recommendedApproach,
          successRate: patternSuccessRate
        }
      }
    }]
  }]
});
```

### Finding Similar Conflicts
```javascript
// Query for conflicts in similar files
const similarFileConflicts = await search_nodes({
  query: "merge conflict",
  filters: {
    fileType: currentFileType,
    conflictType: currentConflictType,
    resolutionSuccess: true
  }
});

// Get resolution strategies ranked by success
const rankedStrategies = similarFileConflicts.reduce((strategies, conflict) => {
  const strategy = conflict.resolutionStrategy;
  strategies[strategy] = (strategies[strategy] || 0) + 1;
  return strategies;
}, {});
```

### Resolution Effectiveness Analysis
```javascript
// Analyze resolution success rates
const resolutionAnalysis = await search_nodes({
  query: "merge resolution",
  filters: {
    timeframe: "last-3-months",
    result: "applied"
  }
});

// Calculate strategy effectiveness
const effectiveness = resolutionAnalysis.reduce((stats, resolution) => {
  const strategy = resolution.strategy;
  if (!stats[strategy]) {
    stats[strategy] = { attempts: 0, successes: 0 };
  }
  stats[strategy].attempts++;
  if (resolution.outcome === "success") {
    stats[strategy].successes++;
  }
  return stats;
}, {});
```

This memory integration ensures that merge conflict resolution knowledge accumulates over time, enabling faster resolutions, better strategy selection, and continuous improvement of merge handling practices.

## Read Order
1) **Exact error node**: `open_nodes(["err#<normalizedKey>"])`.
2) **Traverse**: `(:Fix)-[:RESOLVES]->(:Error)`; optionally `(:Fix)-[:DERIVED_FROM]->(:Doc)`.
3) **Fallback search**: `search_nodes("type:Error normalizedKey:<key>")` → open and traverse.

## Ranking
- Prefer fixes that:
  - Resolved the same key **recently**.
  - Have **evidence** (`DERIVED_FROM Doc`).
  - Show **repeat success** across multiple runs.

## Summarization (prompt hygiene)
- Return **≤3** candidate fixes with:
  - `strategy` in ≤1 sentence.
  - Minimal change set (files/paths).
  - Evidence titles (if any) and node IDs for drill-down.

## Complete Envelope Examples for Reads

When retrieving prior fixes, the stored envelopes follow this hivemind contract structure:

**fix.apply** (retrieved from memory):
```json
{
  "type": "fix.apply",
  "ts": "2025-10-15T09:30:22.123Z",
  "mode": "merge-resolver@1.0",
  "repo": "owner/repo-name",
  "branch": "main",
  "fingerprint": "1234567890abcdef...",
  "data": {
    "strategy": "Updated import path to use relative path instead of absolute",
    "changes": [
      {
        "file": "src/components/Button.tsx",
        "op": "update",
        "path": "import statement",
        "from": "import { utils } from '@/utils/helpers'",
        "to": "import { utils } from '../../utils/helpers'"
      }
    ],
    "result": "applied"
  }
}
```

**doc.note** (evidence for fix):
```json
{
  "type": "doc.note",
  "ts": "2025-10-15T09:30:22.123Z",
  "mode": "merge-resolver@1.0",
  "repo": "owner/repo-name",
  "branch": "main",
  "fingerprint": "234567890abcdef1...",
  "data": {
    "url": "https://nextjs.org/docs/advanced-features/module-path-mapping",
    "title": "Next.js Module Path Mapping",
    "site": "nextjs.org",
    "author": "Vercel",
    "published_at": "2024-01-15",
    "accessed_at": "2025-10-15T09:30:22.123Z",
    "archive_url": "https://web.archive.org/web/20241015093022/https://nextjs.org/docs/advanced-features/module-path-mapping",
    "excerpt": "Next.js supports absolute imports using the @ alias for the src directory, but relative imports are more reliable in monorepos."
  }
}
```

## Preemptive Hints
- If historical data shows a **toolchain mismatch** pattern for this repo, surface a pre-check (Node version, package manager version, cache settings) before heavy edits.

## Determinism & Safety
- Reads never mutate. If ties, sort by `ts` then `name`.
- Cache (`normalizedKey` → fix IDs) for this PR to avoid redundant reads.