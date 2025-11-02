# .roo/rules-design-engineer/20-deprecation-handling.md
> Normalize how we detect, encode, and remediate UI-stack deprecations.

## Detection
- Parse build output for phrases like `deprecated`, `removed`, `renamed`, `requires`, `peer`, `mismatch`, `unsupported`.
- Extract **primary** line(s); derive `normalizedKey` (lowercase → strip hashes → collapse semver → squeeze spaces).

## Common Patterns (Tailwind v4 / shadcn-ui)
- **CSS-first pipeline**: replace `@tailwind base/components/utilities` with `@import "tailwindcss"`.
- **PostCSS changes**: migrate Tailwind plugin to `@tailwindcss/postcss`; remove standalone `autoprefixer` unless required.
- **Animation plugin**: replace `tailwindcss-animate` with `tw-animate-css` if flagged in components.
- **Colors**: migrate to OKLCH tokens; ensure accessible dark-mode contrasts.

## Memory Writes
- On detection: upsert `Error` or `Warning` node (`err#<key>` / `warn#<key>`) with `detector:"build/ui"` and details (tool, version, file).
- On remediation: upsert `Fix` with `{ strategy, changes[], result }`; link `DERIVED_FROM Doc` if an official guide was used.
- On dependency conflicts: create `Dependency` and link `Error CAUSED_BY Dependency`.

## Safe Remediation Order
1) Update tokens/config (backwards-compatible).
2) Swap deprecated plugins/utilities.
3) Adjust component imports/usages.
4) Re-generate shadcn components if CLI provides an overwrite flow (commit before overwrite).
5) Re-test interactive patterns (menus/dialogs) for keyboard and focus traps.

## Verification
- Build passes locally; no new warnings.
- Visual diffs approved (core screens).
- A11y checks pass (focus, contrast, target sizes).
