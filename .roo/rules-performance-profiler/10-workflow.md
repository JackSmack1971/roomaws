# Performance Profiling Workflow (Performance Profiler mode)

1) On profiling run completion: emit `command.exec` with stdoutHead/stderrHead (first ~8k chars), exitCode, durationMs.
2) If regression detected (e.g., LCP > 2.5s, throughput drop >10%):
   - Derive `normalizedKey` from the primary metric (e.g., "lcp-regression", "memory-leak").
   - Persist `warning.capture {kind: "PerformanceRegression", message, detector: "lighthouse", normalizedKey}`.
   - Query: search_nodes("type:Warning normalizedKey:<key>") → follow (:Fix)-[:MITIGATES]->(:Warning) and (:Fix)-[:DERIVED_FROM]->(:Doc).
   - Summarize top 3 prior Fix patterns; apply the safest minimal-change fix first.
3) After optimization: persist `fix.apply {strategy, changes[], result}` and any `doc.note {url,title,excerpt}`; link Fix DERIVED_FROM Doc.