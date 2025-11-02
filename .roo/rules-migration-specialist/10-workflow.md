# Migration Workflow (Migration Specialist mode)

1) On migration step completion: emit `command.exec` with stdoutHead/stderrHead (first ~8k chars), exitCode, durationMs.
2) If migration failure (e.g., build break, test failure):
   - Derive `normalizedKey` from the primary error (e.g., "react-18-migration-build-error").
   - Persist `error.capture {kind: "MigrationFailure", message, detector: "codemod", normalizedKey}`.
   - Query: search_nodes("type:Error normalizedKey:<key>") → follow (:Fix)-[:RESOLVES]->(:Error) and (:Fix)-[:DERIVED_FROM]->(:Doc).
   - Summarize top 3 prior Fix patterns; apply the safest minimal-change fix first.
3) After successful phase: persist `fix.apply {strategy, changes[], result}` and any `doc.note {url,title,excerpt}`; link Fix DERIVED_FROM Doc.