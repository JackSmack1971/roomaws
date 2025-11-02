# .roo/rules-merge-resolver/30-tool-usage.md
> Tool priorities and exact commands (converted from XML).

## Tool Priorities
1) **execute_command** — all `git`/`gh` operations.  
2) **read_file** — inspect conflicted files and markers.  
3) **apply_diff** — precise conflict block replacement (escape markers).

## Common Commands
- Get PR info: `gh pr view [PR] --json title,body,headRefName,baseRefName`
- Checkout PR: `gh pr checkout [PR] --force`
- Fetch main: `git fetch origin main`
- Rebase non‑interactive: `GIT_EDITOR=true git rebase origin/main`
- Check conflicts: `git status --porcelain | grep "^UU"` or `git diff --name-only --diff-filter=U`
- Blame region: `git blame -L [start],[end] HEAD -- [file]`
- Commit message: `git log -1 --format="%s%n%n%b" [sha]`
- Stage file: `git add [file]`
- Continue rebase: `GIT_EDITOR=true git rebase --continue`

## apply_diff Tips
- Always **escape** conflict markers.
- Provide enough context and consider `:start_line:` for precision.
- Combine multiple blocks per file where safe.
