# .roo/rules-design-engineer/40-memory-io.md
> Exact, efficient Memory MCP usage for Design Engineer (idempotent, shared across swarm).

## Read First
1) **Docs**: open `doc#<sha256(url|path)>` for prior design patterns, component standards, and accessibility guidelines.
2) **Command lens**: from `cmd#<canonical>#<fp8>` roll up past build/test failures and Storybook deployment issues.
3) **Error/Warning**: `err#warn#<normalizedKey>` for UI bugs, accessibility violations, and design inconsistencies.

## Write After
Complete envelope examples following hivemind contract:

**command.exec**:
```json
{
  "type": "command.exec",
  "ts": "2025-11-01T13:22:14.646Z",
  "mode": "design-engineer@1.0",
  "repo": "owner/repo-name",
  "branch": "feature/ui-redesign",
  "fingerprint": "e5f6789012345678...",
  "data": {
    "cmd": "npm run build",
    "cwd": "/path/to/project",
    "exitCode": 0,
    "durationMs": 12500,
    "stdoutHead": "✓ 123 modules transformed.\n✓ built in 12.50s",
    "stderrHead": null
  }
}
```

**warning.capture**:
```json
{
  "type": "warning.capture",
  "ts": "2025-11-01T13:22:14.646Z",
  "mode": "design-engineer@1.0",
  "repo": "owner/repo-name",
  "branch": "feature/ui-redesign",
  "fingerprint": "f678901234567890...",
  "data": {
    "normalizedKey": "button-missing-aria-label",
    "kind": "AccessibilityViolation",
    "message": "Button component missing aria-label attribute",
    "detector": "axe-core",
    "component": "Button",
    "issue": "WCAG 2.1 AA violation - buttons must have accessible names"
  }
}
```

**fix.apply**:
```json
{
  "type": "fix.apply",
  "ts": "2025-11-01T13:22:14.646Z",
  "mode": "design-engineer@1.0",
  "repo": "owner/repo-name",
  "branch": "feature/ui-redesign",
  "fingerprint": "7890123456789012...",
  "data": {
    "strategy": "Added aria-label prop to Button component with dynamic content",
    "changes": [
      {
        "file": "src/components/Button.tsx",
        "op": "update",
        "path": "Button component props",
        "from": "interface ButtonProps { children: ReactNode; onClick?: () => void; }",
        "to": "interface ButtonProps { children: ReactNode; onClick?: () => void; ariaLabel?: string; }"
      },
      {
        "file": "src/components/Button.tsx",
        "op": "update",
        "path": "Button render method",
        "from": "<button onClick={onClick}>{children}</button>",
        "to": "<button onClick={onClick} aria-label={ariaLabel}>{children}</button>"
      }
    ],
    "result": "applied"
  }
}
```

**doc.note**:
```json
{
  "type": "doc.note",
  "ts": "2025-11-01T13:22:14.646Z",
  "mode": "design-engineer@1.0",
  "repo": "owner/repo-name",
  "branch": "feature/ui-redesign",
  "fingerprint": "8901234567890123...",
  "data": {
    "url": "https://www.w3.org/WAI/WCAG21/quickref/#name-role-value",
    "title": "WCAG 2.1 Success Criterion 4.1.2 - Name, Role, Value",
    "site": "w3.org",
    "author": "W3C Web Accessibility Initiative",
    "published_at": "2018-06-05",
    "accessed_at": "2025-11-01T13:22:14.646Z",
    "archive_url": "https://web.archive.org/web/20241101132214/https://www.w3.org/WAI/WCAG21/quickref/#name-role-value",
    "excerpt": "For all user interface components, the name and role can be programmatically determined; states, properties, and values that can be set by the user can be programmatically set; and notification of changes to these items is available to user agents, including assistive technologies."
  }
}
```

## Stable Names
- Runs/Commands: `run#<iso>#<fp8>`, `cmd#<canonical>#<fp8>`
- Docs: `doc#<sha256(url|path)>`
- Issues/Warnings: `err#warn#<normalizedKey>`
- Components: `component#<name>@<version?>`
- Fixes: `fix#<component>#<sha8(JSON(changes))>`

## Normalized Key
- Lowercase → strip hashes/paths/timestamps → collapse semver → squeeze spaces.

## Safety
- **Open-then-create**; skip if exists. Never store secrets or entire component files.
