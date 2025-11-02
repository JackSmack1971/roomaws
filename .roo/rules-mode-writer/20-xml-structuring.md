# .roo/rules-mode-writer/20-xml-structuring.md
> If a repo still uses XML rule files, keep structure predictable; prefer Markdown going forward.

- Use **semantic tags** (`<workflow>`, `<guidelines>`, `<tool_usage>`), consistent naming, and hierarchical nesting.
- Place examples inside **CDATA** when needed; keep indentation consistent.
- Prefer **attributes for metadata**, elements for content.
- Anti‑patterns: flat structures, inconsistent tags, generic names (“data”, “stuff”).
- Migration note: mirror XML sectioning when converting to Markdown rule files (same order and headings).
