# .roo/rules-issue-resolver/60-examples.md
> Example scaffolds. Adapt as starting points.

## Example: Silent Login Failure
- **Hypothesis**: Empty `catch` swallows errors in `handleLogin`.
- **What to read**: `src/auth/login.ts`; any global error middleware.
- **Disprove attempt**: search for alternate error handlers; check config flags.
- **Theoretical fix**: log/display error; surface user-visible feedback; add regression test.

## Example: Feature Flag Mismatch
- **Hypothesis**: Flag default differs between environments.
- **Read**: `config/*.ts`, feature checks, deployment manifest.
- **Disprove**: confirm env var overrides; CI vs dev parity.
- **Theoretical fix**: unify defaults; validate in tests.

## Example: Slow Search Endpoint
- **Hypothesis**: N+1 DB queries in aggregation.
- **Read**: repository layer; query builder; hot path handlers.
- **Disprove**: profile alternate path; inspect cache behavior.
- **Theoretical fix**: batch queries; add cache; tighten indexes.
