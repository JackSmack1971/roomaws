# .roo/rules-issue-resolver/30-common-patterns.md
> Ready-to-run investigation templates.

## Bug Investigation
1) Identify exact error message.
2) Search for it in code.
3) Read throwing site; map context.
4) Trace backward to origin.
5) Form hypothesis (state/logic/config).
6) Try to disprove (alt paths/configs).
7) Suggest code change (theoretical).

## Unexpected Behavior
1) Identify feature/component.
2) Find main implementation files.
3) Read intended logic.
4) Hypothesize which logic causes result.
5) Check configs/data affecting behavior.
6) Try to disprove.
7) Suggest logic or config change.

## Performance Issue
1) Identify slow action/process.
2) Find responsible code.
3) Look for anti-patterns (expensive loops, N+1, redundant I/O).
4) Hypothesize bottleneck.
5) Try to disprove (other contributors).
6) Suggest a more efficient approach (cache/batch/algorithm).
