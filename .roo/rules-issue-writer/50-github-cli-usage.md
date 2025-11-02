# .roo/rules-issue-writer/50-github-cli-usage.md
> Deterministic commands for search, templates, and creation.

## Pre-Creation
- **Duplicates**: `gh issue list --repo $REPO_FULL_NAME --search "<keywords>" --state all --limit 20`
- **View related**: `gh issue view <num> --repo $REPO_FULL_NAME --comments`

## Template Handling
- Detect files under `.github/ISSUE_TEMPLATE/`; read YAML/MD; parse metadata.
- Prefer YAML forms; map to sections; respect labels/title.

## Create Issue
- Save body → `./github_issue_draft.md`.
- **Bug**: `gh issue create --repo $REPO_FULL_NAME --title "<title>" --body-file ./github_issue_draft.md --label bug`
- **Feature**: `… --label enhancement --label proposal`
- On failure: check `gh auth status`; consider `--web`.

## Post-Creation
- `gh issue comment` only if user asks to add follow-ups.
