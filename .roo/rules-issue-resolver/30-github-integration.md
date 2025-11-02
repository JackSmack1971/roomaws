# .roo/rules-issue-resolver/30-github-integration.md
> GitHub CLI patterns and integration workflows for issue resolution.

## URL Intake & Auth
- Require full issue URL: `https://github.com/<owner>/<repo>/issues/<number>`.
- Assume `gh` is installed and authenticated; if an auth error occurs, prompt the user to run `gh auth login`.

## Core Commands
- View issue JSON and comments: `gh issue view <number> --json title,body,comments,labels,assignees`
- Search code / list related PRs: `gh search prs --repo <owner>/<repo> --state open --label <relevant-label>`
- Inspect recent commits for affected files: `gh api repos/<owner>/<repo>/commits --jq '.[].sha' | head -5`
- Create PRs (with body file) and monitor checks: `gh pr create --base main --title "<title>" --body-file pr-body.md --maintainer-can-modify`

## PR Workflow Integration
### Preparation
- Commit all changes with conventional subject; push branch; extract owner/repo from the issue URL.

### Title Format
- **Bug**: `fix: <brief> (#<issue>)`
- **Feature**: `feat: <brief> (#<issue>)`

### PR Body (must include)
- Link to issue ("Fixes #…")
- What changed & why (concise)
- Tests performed + how to verify
- Acceptance-criteria checklist
- Screenshots/demos (UI)

### Creation
- Use `gh pr create --base main --title "<title>" --body-file pr-body.md --maintainer-can-modify`.

### After Creation
- Comment on the original issue with the PR number.
- Monitor PR checks; address failures before review.

## Testing Guidelines
- Run existing tests **before** changes (baseline).
- Add tests for new code; add **regression tests** for bug fixes.
- Exercise error paths and edge cases.
- Run full suite before finalization.
- For UI: test multiple themes; verify keyboard navigation and screen readers.
- Consider performance for large inputs/operations.

## Notes
- Prefer `--json` for structured data.
- Use `--maintainer-can-modify` on PRs.
