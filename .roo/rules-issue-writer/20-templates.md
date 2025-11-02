# .roo/rules-issue-writer/20-templates.md
> Repository templates over hardcoded ones; YAML forms preferred.

## Detection Order
1) `.github/ISSUE_TEMPLATE/*.yml` / `*.yaml` (Issue Forms)
2) `.github/ISSUE_TEMPLATE/*.md`
3) `.github/issue_template.md`
4) `.github/ISSUE_TEMPLATE.md`

## YAML Forms (map → sections)
- Read: `name`, `description`, `title`, `labels`, `assignees`, `body[*]`.
- Convert `markdown`, `input`, `textarea`, `dropdown`, `checkboxes` into markdown sections, preserving **required** indicators and helper text.

## Markdown Templates
- Parse front-matter (`name`, `about`, `title`, `labels`, `assignees`).
- Keep structure (## headers, checklists); replace placeholders; never leave blanks.

## No Templates → Minimal Generators
- **Bug**: Description · Steps · Expected vs Actual · Context (versions/env) · Code Investigation.
- **Feature**: Problem · Current Behavior · Proposed Solution · Impact · Technical Context.

## Labels & Ordering
- Apply labels from template metadata; keep filename-ordering stable.
