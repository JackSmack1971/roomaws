# .roo/rules-docs-manager/40-communication-guidelines.md
> Output formatting and comms standards for extraction/verification reports.

## Markdown Standards
- Headings: `#` title, then `##`, `###` only (no skips).
- Code blocks: specify language; include relevant file paths as comments.
- Tables: headers + aligned columns; brief cells.
- Lists: bullets for unordered; numbers for sequences.

## Cross-References
- Internal: `[Link text](#section-anchor)` using lowercase hyphen anchors.
- External: HTTPS to official sources.
- File refs: back-ticked workspace-relative paths.

## Special Sections
- Alerts: `> ⚠️ **Warning**:` for security/breaking/deprecations.
- Notes/Tips blocks for clarifications and best practices.
- Optional front-matter metadata (Feature/Version/Status).

## Communication Flow
- Progress updates at key milestones (start of analysis, extraction complete, unexpected complexity).
- Findings blocks for **security issues**, **deprecated code**, **missing docs**, **complex dependencies**.

## Completion Messages
- Summary of analysis; key findings; report path; next steps.
- Provide both **technical** and **non-technical** summaries where helpful.

## Quality Checks (before completion)
- No placeholders; correct code examples; working links; proper tables; version info; file naming convention.
