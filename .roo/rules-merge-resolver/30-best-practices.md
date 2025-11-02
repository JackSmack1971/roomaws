# .roo/rules-merge-resolver/20-best-practices.md
> Principles and heuristics (converted from XML).

## Principles
- **Intent‑Based Resolution**: prioritize the purpose of each change (bugfix, feature, refactor).  
- **Preserve Valuable Changes**: combine when feasible rather than discarding.
- **Consider Related Changes**: check tests/docs/dependents.  
- **Escape Conflict Markers** in diff tooling (`\<<<<<<<`, `\=======`, `\>>>>>>>`).

## Heuristics
- Bugfix vs Feature → **bugfix** first; reintegrate around it.
- Recent vs Old → prefer **recent**, unless older is a security/bug fix.
- Test Updates → prefer sides that **update tests**.  
- Formatting vs Logic → **logic wins**; formatting can be re‑applied.

## Pitfalls to Avoid
- Blindly choosing one side.  
- Ignoring PR description/intent.  
- Skipping validation after resolution.  
- Failing to escape markers in diffs.
