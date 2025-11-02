# .roo/rules-design-engineer/10-research-sop.md
> SOP for evidence-backed UI decisions and dependency usage.

## Research Triggers
- Adding/upgrading UI libs (shadcn/ui, Radix, Tailwind).
- Changing tokens, color scales, or motion primitives.
- Addressing deprecations or build warnings.

## Procedure
1) **Define question**: what behavior/design rule is disputed?  
2) **Locate primary sources**: official docs, release/upgrade guides, spec pages.  
3) **Capture evidence**: create `Doc` with `{url,title,site,author?,published_at?,accessed_at,archive_url?,excerpt}`.  
4) **Link**: `Fix DERIVED_FROM Doc`; optionally `Doc REFERENCES Concept` (e.g., “OKLCH contrast”, “Focus Visible”).  
5) **Summarize**: ≤200 tokens; extract the exact normative phrasing if relevant.

## Implementation Notes
- Prefer shadcn/ui components as **open code** copies; customize in-repo.
- Tailwind v4: favor CSS-first configuration (`@theme`) for tokens; keep `tailwind.config.js` only when necessary.
- Motion: use utility classes; prefer reduced-motion fallbacks.

## Acceptance Checklist (attach to PR)
- [ ] Evidence captured (Doc) for any new rule/workaround.  
- [ ] Tokens used (no magic colors/sizes).  
- [ ] A11y checks: focus visible, keyboard path, target sizes, labels.  
- [ ] CSP compliance (if in webview/embedded UI).  
- [ ] Memory updated: error/fix/doc recorded.
