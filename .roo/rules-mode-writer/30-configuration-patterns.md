# .roo/rules-mode-writer/30-configuration-patterns.md
> Canonical mode templates & permission presets.

## Specialist Mode
- Deep domain expertise; narrow `fileRegex`.
- `groups`: `read`, `- edit` (regex‑scoped), `command`, optional `mcp`/`browser`.

## Workflow Mode
- Guides multi‑step processes; heavy `ask_followup_question`.
- `groups`: `read`, `edit` (docs/templates), `command`.

## Analysis Mode
- Read‑heavy; limited or no edits; rich reporting.
- `groups`: `read`, `command`, optional narrow `- edit` for docs only.

## Creative Mode
- Broad file creation; templates and scaffolds.
- `groups`: `read`, `edit` (broad or component‑scoped), `command`, optionally `browser`, `mcp`.

### Permission Presets
- **documentation_only**: `\.(md|mdx|rst|txt)$`
- **test_focused**: `(__tests__/.*|__mocks__/.*|.*\.(test|spec)\.(ts|tsx|js|jsx)$)`
- **config_management**: `(.*\.config\.(js|ts|json)|.*rc\.json|.*\.(ya?ml)|\.env\.example)$`
- **full_stack**: unrestricted `edit` (use sparingly).
