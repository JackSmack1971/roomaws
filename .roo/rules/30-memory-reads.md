# 30-memory-reads.md
> Applies to all modes. Standardizes **how to read from the hive-mind graph** to maximize reuse of past fixes, minimize latency, and keep prompts lean.

## Goals
- **High recall, then precision:** find likely-relevant prior incidents fast, then rank and trim to a terse brief for the active task.  
- **Query for the answer you need:** shape reads around the decision (e.g., “which fixes resolved this error key?”), not around raw data scans. :contentReference[oaicite:0]{index=0}

---

## Read Order (must-follow)
1) **Exact keys first (cheap & precise).**  
   - If you have a **stable key** (e.g., `normalizedKey` or entity `name`), prefer `open_nodes(names)` or an exact-key search.  
   - Avoid broad scans when an exact handle exists. :contentReference[oaicite:1]{index=1}
2) **Selective graph traversals (left-to-right specificity).**  
   - Start from the most selective node and traverse only necessary hops; avoid Cartesian products/unconnected patterns. :contentReference[oaicite:2]{index=2}
3) **Limit early; return only what you need.**  
   - Cap K (e.g., top-3 fixes) and project only fields you will display/use. Early LIMIT reduces work dramatically. :contentReference[oaicite:3]{index=3}
4) **Use indexes-aware predicates when available.**  
   - Query by indexed label+property (e.g., `:Error{name}`, `:Fix{name}`) to let the planner pick or you hint the index. :contentReference[oaicite:4]{index=4}

---

## Canonical Retrieval Recipes
> Pseudocode describes the **logical traversal** your mode should request via MCP tools.

### A) Prior fixes for an error key
```

START   error = (:Error { name: "err#<normalizedKey>" })
FOLLOW  (:Fix)-[:RESOLVES]->(error)
OPTION  (:Fix)-[:DERIVED_FROM]->(:Doc)
RETURN  top K fixes with their doc metadata

```
- Rank fixes by most recent `fix.apply.ts` and by recurrence across distinct runs.  
- If `err#<key>` missing, **fallback** to text search on observations containing `normalizedKey`. :contentReference[oaicite:5]{index=5}

### B) What usually breaks this command?
```

START   cmd = (:Command { name: "cmd#<canonical>#<fp8>" }) OR search by cmd hash prefix
FOLLOW  cmd-[:EMITS]->(:Error|:Warning)
GROUP   by normalizedKey → COUNT occurrences
RETURN  top keys + representative Fix for each

```
- Useful to propose **preemptive mitigations**.

### C) Dependency-rooted reading (conflicts/deprecations)
```

START   dep = (:Dependency { name:"<pkg>", version:"<ver?>" })
FOLLOW  (:Error)-[:CAUSED_BY]->(dep)
FOLLOW  (:Fix)-[:RESOLVES]->(:Error)
RETURN  minimal Fix set that historically cleared these errors

```
- Prefer pin/constraint patterns surfaced most often.

### D) Evidence roll-up for an applied fix
```

START   fix = (:Fix { name:"fix#..." })
FOLLOW  fix-[:DERIVED_FROM]->(doc:Doc)
FOLLOW  optional doc-[:REFERENCES]->(concept:Concept)
RETURN  {doc metadata, concepts} for audit trail

```

---

## Ranking & Summarization Rules
- **Score** candidates by: recency (ts), success ratio (resolved > re-opened), and support (has `DERIVED_FROM Doc`).  
- **Trim** to top-3 items and **summarize** to ≤200 tokens for prompt hygiene (link names/IDs for deep drill).  
- **Prefer evidence-backed fixes** over anecdotal ones. (Fixes with `DERIVED_FROM Doc` rank first.)

---

## Performance Guidelines (planner-friendly)
- **Filter early.** Put the most selective predicates at the start node; avoid unbounded variable-length traversals. :contentReference[oaicite:6]{index=6}  
- **Avoid Cartesian products.** Do not match unconnected patterns; join via explicit relationships. :contentReference[oaicite:7]{index=7}  
- **Exploit indexes.** Query on properties that have indexes; the planner often picks them automatically, or use hints when needed. :contentReference[oaicite:8]{index=8}  
- **Return projections, not whole nodes.** Only the fields your mode will actually use (names, ts, key fields). :contentReference[oaicite:9]{index=9}  
- **LIMIT early.** Reduce intermediate cardinality; early LIMIT can cut DB hits by orders of magnitude. :contentReference[oaicite:10]{index=10}

---

## Fallback Strategy (no exact hit)
1) **Soft match**: search observations for the normalized key or its stem (strip versions/paths).
2) **Neighbor signal**: start from `:Command` or `:Dependency` context nearest to the current failure.
3) **Concept expansion**: if the error is tagged with `:Concept` (e.g., "ts-node loader"), traverse `(:Doc)-[:REFERENCES]->(:Concept)` to pull authoritative docs.

---

## Handling MCP Unavailability Gracefully

### Degraded Operation Guidelines

When Memory MCP is unavailable, modes should continue functioning with reduced capabilities while maintaining audit trails for later synchronization:

1. **Continue Core Functionality**: Don't block on memory operations - proceed with local context
2. **Structured Logging**: Use structured JSON logs with `level`, `event`, `key`, `durationMs`, `retries` for offline analysis
3. **Queue-and-Retry Patterns**: Buffer memory writes for later replay when MCP recovers
4. **Clear User Feedback**: Document degraded state in completion summaries

### Queue-and-Retry Patterns

#### Write Buffer Implementation
```javascript
class MemoryWriteQueue {
  constructor() {
    this.queue = [];
    this.maxRetries = 3;
    this.retryDelay = 250; // ms, exponential backoff
  }

  async enqueue(operation, data) {
    this.queue.push({
      operation,
      data,
      timestamp: new Date().toISOString(),
      retries: 0
    });
    await this.flush();
  }

  async flush() {
    if (this.queue.length === 0) return;

    const batch = this.queue.splice(0); // Take all pending
    for (const item of batch) {
      try {
        await this.attemptWrite(item);
      } catch (error) {
        if (item.retries < this.maxRetries) {
          item.retries++;
          this.queue.unshift(item); // Re-queue with backoff
          await this.delay(this.retryDelay * Math.pow(2, item.retries));
        } else {
          // Log permanent failure
          console.error(`Memory write failed permanently: ${item.operation}`, error);
        }
      }
    }
  }

  async attemptWrite(item) {
    // Attempt MCP call
    await use_mcp_tool({
      server_name: "memory",
      tool_name: item.operation,
      arguments: item.data
    });
  }

  delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```

#### Read Fallback Strategy
```javascript
async function readWithFallback(query, fallbackFn) {
  try {
    return await use_mcp_tool({
      server_name: "memory",
      tool_name: "search_nodes",
      arguments: { query }
    });
  } catch (error) {
    console.warn("Memory MCP unavailable, using fallback");
    return await fallbackFn(query);
  }
}
```

### Local Caching Approaches

For scenarios where MCP is down:
- **Cache key → top-K fix IDs** for the current session
- **Expire cache** at task boundary to prevent staleness
- **Use fallback strategies** for reads (soft match, neighbor signal, concept expansion)
- **Defer writes** until MCP recovers, don't block execution

### Recovery and Synchronization

When MCP becomes available again:
1. **Replay queued writes** in order with conflict resolution
2. **Validate cached reads** against fresh data
3. **Log recovery metrics** (items replayed, conflicts resolved)
4. **Clear local caches** to prevent divergence

See also: 40-memory-mcp-reference.md for comprehensive fallback strategies and degraded operation guidelines.

---

## Safety & Determinism
- **Never** mutate during read paths. Reads must not call delete/merge semantics.  
- If multiple results tie, order by deterministic keys (`name`, `ts`) for stable outputs across runs.  
- Cache **keys → top-K fix IDs** for the current session to avoid redundant reads; expire at task boundary.

---

## Example “Prompt-Ready” Output (mode should produce)
```

PRIOR_FIXES(err#ts-node-register-deprecated):

1. fix#... — Strategy: switch to ts-node/register/transpile-only — Evidence: doc#<sha> (title, accessed)
2. fix#... — Strategy: pin [ts-node@10.9.x](mailto:ts-node@10.9.x) — Evidence: doc#<sha>
3. fix#... — Strategy: update tsconfig moduleResolution

```

---