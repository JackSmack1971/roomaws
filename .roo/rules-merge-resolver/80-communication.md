# .roo/rules-merge-resolver/50-communication.md
> Tone, progress updates, and completion templates (converted from XML).

## Tone & Style
- Direct, technical, rationale‑first. Avoid vague reassurances.

## Initial Response
- Acknowledge PR number, state PR fetch, indicate analysis start.

## Progress Updates
- Announce count of conflicted files, files in progress, strategy per file, and validation status.

## Conflict Explanations (per file)
- **HEAD** vs **Incoming** summaries; chosen resolution; brief why; reference SHAs when relevant.

## Completion Template
```
Successfully resolved merge conflicts for PR #[number] "[title]".

Resolution Summary:
- [file1]: [resolution & why]
- [file2]: [resolution & why]

All conflicts resolved and staged; rebase continued non‑interactively.
```
