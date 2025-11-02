# mode-tools — `.roomodes` validation pack

Place this folder at `project_root/.roo/mode-tools/`. The tools auto-detect the **project root** by walking upward until they find `.roomodes`.

## Files
- `validate_roomodes.py` — folder-agnostic validator (tabs banned, fixed indentation = 2 spaces, JSON Schema validation).
- `run_all.py` — convenience script to run yamllint → spectral → schema validator.
- `roomodes.schema.json` — strict JSON Schema derived from your `.roomodes` structure.
- `yamllint.yaml` — formatting policy (spaces-only, 2-space indentation).
- `spectral.yaml` — additional YAML rules.
- `.editorconfig` — IDE/editor enforcement.

## Usage

From *any subfolder inside the project*:

```bash
cd project_root/.roo/mode-tools
python run_all.py
# or
python validate_roomodes.py          # auto-discovers project root
python validate_roomodes.py ../.roomodes  # or explicit path
```

## Dependencies
```bash
pip install jsonschema pyyaml yamllint
npm i -g @stoplight/spectral-cli
```

## Mode Orchestration (Validator → Writer)

1) Add the provided `mode-validator.snippet.yaml` entry into your `.roomodes` under `customModes:`.
2) From anywhere inside the project, run the validator flow:
   ```bash
   cd project_root/.roo/mode-tools
   python summarize_mode_validation.py
   ```
3) The summarizer writes:
   - JSON: `project_root/.roo/reports/mode_validation_summary.json`
   - Markdown: `project_root/.roo/reports/mode_validation_summary.md`
   - Handoff: `project_root/.roo/handoff/mode_validation_handoff.json`
4) Your `mode-writer` mode should read the handoff JSON, load the summary, and refactor `.roomodes` as needed.
