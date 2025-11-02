# .roo/rules-merge-resolver/40-complete-example.md
> Worked example (converted from XML).

**Scenario**: PR `#123` conflicts between a feature **refactor** and a **bugfix** branch.  
**Strategy**: keep async refactor **and** preserve listener cleanup (memory‑leak fix).  
**Flow**: view PR → checkout → fetch main → rebase → list `UU` → read files → blame → analyze intent → apply combined resolution → stage → continue rebase → validate → summarize.

(Example command/IO blocks mirror the XML: blame both sides, confirm commit messages, merge logic + cleanup, update tests, continue rebase, verify clean tree.) 
