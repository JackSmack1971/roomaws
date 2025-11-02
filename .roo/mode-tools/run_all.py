#!/usr/bin/env python3
"""
run_all.py — convenience entrypoint to validate `.roomodes` from /.roo/mode-tools.
- Auto-discovers project root.
- Runs: yamllint, spectral (if available), schema validator, security checks.
"""
import shutil, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VALIDATOR = HERE / "validate_roomodes.py"
ROOMODES = None

def find_project_root(start: Path) -> Path | None:
    cur = start.resolve()
    for p in [cur, *cur.parents]:
        if (p / ".roomodes").exists():
            return p
    return None

def main():
    root = find_project_root(Path.cwd())
    if root is None:
        print("Error: Could not find project root (no `.roomodes` found upward from CWD).", file=sys.stderr)
        sys.exit(1)
    target = root / ".roomodes"

    # yamllint
    yamllint = shutil.which("yamllint")
    if yamllint:
        print("-> yamllint")
        subprocess.check_call([yamllint, "-c", str(HERE / "yamllint.yaml"), str(target)])
    else:
        print("! yamllint not found; skipping. Install with: pip install yamllint")

    # spectral
    spectral = shutil.which("spectral")
    if spectral:
        print("-> spectral")
        subprocess.check_call([spectral, "lint", "-r", str(HERE / "spectral.yaml"), str(target)])
    else:
        print("! spectral not found; skipping. Install with: npm i -g @stoplight/spectral-cli")

    # schema and security validator
    print("-> schema and security validator")
    subprocess.check_call([sys.executable, str(VALIDATOR), str(target)])

    # conftest (policy as code)
    conftest = shutil.which("conftest")
    if conftest:
        print("-> conftest policy check")
        subprocess.check_call([conftest, "test", "-p", str(HERE / "conftest-policy.yaml"), str(target)])
    else:
        print("! conftest not found; skipping. Install with: go install github.com/open-policy-agent/conftest@latest")

    # opa (alternative policy engine)
    opa = shutil.which("opa")
    if opa:
        print("-> opa policy check")
        # Create temporary data file for OPA
        import json
        import yaml
        with open(target, 'r') as f:
            roomodes_data = yaml.safe_load(f)
        with open(HERE / "temp_roomodes.json", 'w') as f:
            json.dump({"roomodes": roomodes_data}, f)

        subprocess.check_call([
            opa, "eval",
            "--data", str(HERE / "security_policy.rego"),
            "--input", str(HERE / "temp_roomodes.json"),
            "data.security.deny"
        ])
        # Clean up temp file
        (HERE / "temp_roomodes.json").unlink(missing_ok=True)
    else:
        print("! opa not found; skipping. Install from: https://www.openpolicyagent.org/docs/latest/#running-opa")

    print("All checks passed.")

if __name__ == "__main__":
    main()