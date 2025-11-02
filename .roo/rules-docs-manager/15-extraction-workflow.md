# .roo/rules-docs-manager/10-extraction-workflow.md
> Canonical workflow for **Source Material** and **Verification** paths.

## Mode Overview
- Choose one path:
  1) **Verification**: check provided documentation vs code/UX reality.
  2) **Source Material**: generate structured, user-oriented facts for writers.

Outputs emphasize **why**, constraints, troubleshooting, and visuals guidance. (No final docs.)

## Initialization
1) **Parse request** → identify feature/aspect; choose path; capture audience & depth (for source-material) or target docs (for verification).
2) **Discover feature** → locate relevant code/assets, entry points, and map the high-level user workflow.

## Analysis Focus (always consider)
- UI components & interactions; user workflows & decision points; configs affecting user behavior.
- Error states & recovery; benefits, limits, prerequisites, versions.
- “Cannot do” boundaries; troubleshooting playbooks; complex states that need visuals.

## Source-Material Path
1) **Scope & audience** → list primary user tasks.
2) **Extract user-facing facts**:
   - Benefits; when to use; how it works (simple).
   - Step-by-step workflows & UI interactions.
   - Config impacting users (name, default, effect).
   - Constraints & rationale; do/don’t; pitfalls.
   - Troubleshooting (symptoms → causes → fixes → prevention).
   - Prereqs, permissions, compatibility/version notes.
   - Mark complex states for visuals (what/why).
3) **Create report** → `EXTRACTION-[feature].md` with executive summary, use cases, how it works, config, constraints, troubleshooting, visuals, FAQ, version notes.

## Verification Path
1) **Analyze provided docs** → enumerate claims, workflows, configs, examples.
2) **Verify against code** → implementation, endpoints/params, defaults, snippets, workflows.
3) **Create report** → `VERIFICATION-[feature].md` with status, critical inaccuracies, corrections, missing info, troubleshooting gaps, visuals suggestions, clarity improvements.

## Memory I/O Hooks (when to write)
- On each command/tool run → `command.exec`.
- When citing sources → `doc.note` (+ archive_url).
- On contradictions/missing facts → `error.capture` with `normalizedKey`.
- On remediation (e.g., regenerate types) → `fix.apply` + `DERIVED_FROM Doc`.

## Done Criteria
- Audience/scope captured; accurate, minimal, user-impacting facts extracted.
- Verification outcomes clear; corrections listed with precise replacements.
- Memory updated for downstream reuse.
