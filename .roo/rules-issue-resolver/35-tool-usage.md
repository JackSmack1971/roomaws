# .roo/rules-issue-resolver/50-tool-usage.md
> Tool priorities and usage.

## Priorities
1) `gh issue view … --json …` — get context first.
2) `codebase_search` — use iteratively; refine with identifiers.
3) `update_todo_list` — after each major step or plan change.

## Guidance
- `gh` (execute_command): prefer `--json` fields; wrap comment bodies in quotes; post only with explicit human approval.
- `codebase_search`: combine multiple keywords; iterate as you learn names and paths.
- `ask_followup_question`: only for “OK to post this comment?” confirmations.

## Combination Pattern: Investigate & Report
1) `gh issue view` → details.
2) `update_todo_list` → plan.
3) `codebase_search` → initial sweep.
4) Read files → analyze.
5) `codebase_search` → confirm/deny hypothesis.
6) `ask_followup_question` → approval to post.
7) `gh issue comment` → post (if approved).

# .roo/rules-issue-resolver/50-tool-usage.md
> Tool priorities and usage.

## Browser Usage
- **Allowed domains**: github.com (issues, discussions), stackoverflow.com, docs.github.com, developer.mozilla.org, react.dev, vuejs.org, angular.dev, nextjs.org, nuxtjs.org
- **Purpose**: Research similar issues, access documentation, check framework-specific guidance
- **Security measures**:
  - No JavaScript execution
  - 30-second timeout per request
  - 1MB content size limit
  - No credential/form submission
  - Read-only access only
- **Risk mitigation**: SSRF protection via domain allowlist; no external redirects followed; no credential leakage

## Priorities
1) `gh issue view … --json …` — get context first.
2) `codebase_search` — use iteratively; refine with identifiers.
3) `update_todo_list` — after each major step or plan change.

## Guidance
- `gh` (execute_command): prefer `--json` fields; wrap comment bodies in quotes; post only with explicit human approval.
- `codebase_search`: combine multiple keywords; iterate as you learn names and paths.
- `ask_followup_question`: only for "OK to post this comment?" confirmations.

## Combination Pattern: Investigate & Report
1) `gh issue view` → details.
2) `update_todo_list` → plan.
3) `codebase_search` → initial sweep.
4) Read files → analyze.
5) `codebase_search` → confirm/deny hypothesis.
6) `ask_followup_question` → approval to post.
7) `gh issue comment` → post (if approved).
