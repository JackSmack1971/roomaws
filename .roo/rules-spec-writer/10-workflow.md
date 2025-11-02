# .roo/rules-spec-writer/10-workflow.md
> Canonical authoring workflow (mapped from system prompt).

## Intake & Intent
1) **Gather Requirements**: Parse user brief/problem statement, constraints, existing specs/ADRs/contracts/tests.
2) **Determine Scope**: Identify artifactType (ModelPolicy|CodeStyle|TestingRequirement|Interface|Runbook), appliesTo domains/architectures.
3) **Create TODO Ledger**: Break down into spec creation, clause writing, test file creation, validation.

## Design
4) **Draft Frontmatter**: Complete YAML frontmatter with artifactType, title, status, version, owners, governance, dependencies, metrics.
5) **Plan Clauses**: Identify atomic, testable requirements with unique IDs (e.g., sy73 for payment atomicity).
6) **Define Governance**: Specify publication rules, blocking checks, adjudication authority.

## Authoring
7) **Write Clauses**: For each clause, write Intent (normative), Rationale (non-normative), Definitions, Success Criteria, Precedent & Disambiguation, Traceability.
8) **Create Test Files**: Generate `tests/policy/<ID>.md` with challenging inputs and expected behavior (pass if all true).
9) **Link Tests**: Ensure every clause ID has corresponding test file with falsifiable prompts.

## Validation
10) **Ambiguity Lint**: Eliminate vague terms ("should," "robust," "fast") with specific thresholds/actors/timelines.
11) **Conflict Scan**: Verify dependencies compatible; block publication if conflicts exist without adjudication.
12) **Quality Gates**: Frontmatter complete, no unlabeled clauses, changelog updated.

## Publication
13) **Write Changelog**: Add deterministic entry describing change and why.
14) **Memory Integration**: Create/update entities/relations/observations for specs/clauses in Memory MCP.
15) **Spec Summary**: Append ≤120 word user-facing summary at end.

## Error Handling
- If ambiguity detected: Revise clause with specific, measurable criteria.
- If dependency conflict: Cite adjudication precedent or block publication with actionable notes.
- If test file missing: Create immediately with challenging prompts and success criteria.

## Delegation Points
- **New Task for Harnesses**: If downstream artifacts needed (BDD steps, contract checks), use `new_task` with concrete DoD.
- **Switch Modes**: Only when user approves different specialization (e.g., Architect for implementation).