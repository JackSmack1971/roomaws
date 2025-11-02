# .roo/rules-docs-manager/30-analysis-techniques.md
> Checklists and heuristics to extract reliable, **user-visible** facts.

## UI/UX Techniques
- **Component discovery**: enumerate related components; container vs presentational; inputs/outputs; conditional rendering.
- **Style analysis**: design tokens & utilities; responsive behavior; visual states.
- **User flow mapping**: routes, validations, handlers, state changes, loading/error states.
- **User feedback**: errors, success, loading, tooltips, confirmations, progress indicators (triggers, severity, persistence, a11y).
- **Accessibility**: ARIA/roles, keyboard paths, SR compatibility, focus mgmt, contrast.
- **Responsive design**: breakpoints, mobile components, touch handlers, viewport.

## Code-Level Techniques
- Entry points & control flow; validation & preconditions.
- API extraction (REST/GraphQL): methods/paths/params/schemas/status codes.
- Dependency mapping: imports, packages, external APIs/SDKs, DB, queues, FS/network.
- Data models: TS types, DB schemas/migrations, validation schemas; relationships & constraints.
- Business logic: conditions, calculations, rules, state machines, invariants; why/when/what/edge cases/impact.
- Error handling: taxonomy, messages, retries/backoffs, fallbacks.
- Security: authn/authz, data protection, input validation.
- Performance: hotspots, N+1, caching, concurrency/async, batching, pooling, memory.

## Workflow & Integration
- User journey mapping: entry points → actions → decisions → data transforms → outcomes (deliver flow diagrams).
- Integration flows: protocols, auth, error handling, transforms, SLAs.

## Metadata Extraction
- Version compatibility table; deprecation tracking (date, removal target, migration, replacement).

## Quality Indicators
- Completeness checks for public APIs, examples, error scenarios, config impacts, security considerations.
- Code quality metrics: complexity, duplication, test coverage, docs coverage, known debt.

## Memory Lens
- Tag concepts (e.g., “rate-limit-errors”, “oauth-refresh”) so Docs & Fixes can reference them.
- For recurring doc issues, normalize keys and link **Fix ↔ Doc ↔ Concept** for downstream reuse.
