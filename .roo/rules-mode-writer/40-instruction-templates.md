# .roo/rules-mode-writer/40-instruction-templates.md
> Standard rule pack structure & snippets.

**Files**
- `00-guardrails.md` · `10-workflow.md` · `20-best-practices.md` · `30-common-patterns.md` · `40-tool-usage.md` · `50-examples.md` · `60-memory-io.md`

**Tool‑combination patterns**
- *explore_then_modify*: `codebase_search → read_file → apply_diff`
- *verify_then_proceed*: `list_files → read_file → ask_followup_question → apply_diff`

**apply_diff example (escaped markers)**
```
<apply_diff>
<path>src/config.ts</path>
<diff>
<<<<<<< SEARCH
:start_line:10
-------
export const config = { a: 1 }
=======
export const config = { a: 1, retries: 3 }
>>>>>>> REPLACE
</diff>
</apply_diff>
```
