#!/usr/bin/env python3
"""
summarize_mode_validation.py
- Runs yamllint, spectral, and the schema validator against the project's `.roomodes`.
- Emits a structured JSON + Markdown summary under `project_root/.roo/reports/`.
- Writes a handoff payload under `project_root/.roo/handoff/` for consumption by Mode-Writer.

Placement (recommended):
  project_root/.roo/mode-tools/summarize_mode_validation.py
"""

import json, subprocess, shutil, sys, os, datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent

def which(cmd):
    return shutil.which(cmd)

def find_project_root(start: Path) -> Path | None:
    cur = start.resolve()
    for p in [cur, *cur.parents]:
        if (p / ".roomodes").exists():
            return p
    return None

def run_cmd(args, input_text=None):
    try:
        cp = subprocess.run(
            args,
            input=input_text.encode("utf-8") if input_text else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            text=True
        )
        return cp.returncode, cp.stdout, cp.stderr
    except FileNotFoundError as e:
        return 127, "", str(e)

def main():
    root = find_project_root(Path.cwd())
    if root is None:
        print("ERROR: Could not locate project root containing `.roomodes` from current path.", file=sys.stderr)
        sys.exit(1)

    reports_dir = root / ".roo" / "reports"
    handoff_dir = root / ".roo" / "handoff"
    reports_dir.mkdir(parents=True, exist_ok=True)
    handoff_dir.mkdir(parents=True, exist_ok=True)

    target = root / ".roomodes"
    yamllint_cfg = HERE / "yamllint.yaml"
    spectral_cfg = HERE / "spectral.yaml"
    validator = HERE / "validate_roomodes.py"

    result = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "project_root": str(root),
        "target": str(target),
        "tools": {},
        "summary": {
            "status": "unknown",
            "yamllint_errors": 0,
            "yamllint_warnings": 0,
            "spectral_issues": 0,
            "schema_valid": False,
        },
        "details": {
            "yamllint": [],
            "spectral": [],
            "schema": {
                "ok": False,
                "errors": []
            }
        }
    }

    # yamllint
    yamllint = which("yamllint")
    if yamllint:
        code, out, err = run_cmd([yamllint, "-c", str(yamllint_cfg), "-f", "parsable", str(target)])
        # parsable lines: file:line:col: level: message  (rule)
        lines = [ln for ln in out.splitlines() if ln.strip()]
        y_errs, y_warns = 0, 0
        y_items = []
        for ln in lines:
            # Attempt to parse
            # example: /path/.roomodes:12:5: [error] message  (rule-name)
            level = "info"
            message = ln
            rule = None
            try:
                head, rest = ln.split(":", 3)[0:3], ln.split(":", 3)[3]
            except Exception:
                head, rest = None, None

            # Split by " [level] " pattern if present
            if " [error] " in ln:
                level = "error"
            elif " [warning] " in ln:
                level = "warning"
            elif " [info] " in ln:
                level = "info"

            if "  (" in ln and ln.endswith(")"):
                try:
                    msg, rulep = ln.rsplit("  (", 1)
                    rule = rulep[:-1]
                    message = msg.split("]: ", 1)[-1]
                except Exception:
                    message = ln

            if level == "error":
                y_errs += 1
            elif level == "warning":
                y_warns += 1

            y_items.append({"level": level, "message": message, "raw": ln, "rule": rule})

        result["tools"]["yamllint"] = {"available": True, "returncode": code}
        result["summary"]["yamllint_errors"] = y_errs
        result["summary"]["yamllint_warnings"] = y_warns
        result["details"]["yamllint"] = y_items
    else:
        result["tools"]["yamllint"] = {"available": False}

    # spectral
    spectral = which("spectral")
    if spectral:
        code, out, err = run_cmd([spectral, "lint", "-r", str(spectral_cfg), str(target), "-f", "json"])
        issues = []
        try:
            issues = json.loads(out)
        except Exception:
            # fallback: treat as text
            issues = [{"raw": ln} for ln in out.splitlines() if ln.strip()]
        result["tools"]["spectral"] = {"available": True, "returncode": code}
        result["summary"]["spectral_issues"] = len(issues)
        result["details"]["spectral"] = issues
    else:
        result["tools"]["spectral"] = {"available": False}

    # schema validator
    code, out, err = run_cmd([sys.executable, str(validator), str(target)])
    schema_ok = code == 0
    result["details"]["schema"]["ok"] = schema_ok
    if not schema_ok:
        msgs = (out + "\n" + err).strip().splitlines()
        # Collect schema errors (stderr contains "Schema error at ...")
        result["details"]["schema"]["errors"] = [m for m in msgs if m.strip()]
    result["summary"]["schema_valid"] = schema_ok

    # Overall status
    if result["summary"]["schema_valid"] and result["summary"]["yamllint_errors"] == 0 and result["summary"]["spectral_issues"] == 0:
        result["summary"]["status"] = "pass"
    else:
        result["summary"]["status"] = "fail"

    # Write JSON + Markdown
    json_path = reports_dir / "mode_validation_summary.json"
    md_path = reports_dir / "mode_validation_summary.md"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    def md_escape(s): return s.replace("<", "\\<").replace(">", "\\>")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# Mode Validation Summary\n\n")
        f.write(f"- **Timestamp (UTC):** {result['timestamp']}\n")
        f.write(f"- **Target:** `{md_escape(str(target))}`\n")
        f.write(f"- **Status:** **{result['summary']['status'].upper()}**\n")
        f.write(f"- **Schema valid:** {result['summary']['schema_valid']}\n")
        if 'yamllint_errors' in result['summary']:
            f.write(f"- **yamllint:** {result['summary'].get('yamllint_errors',0)} errors, {result['summary'].get('yamllint_warnings',0)} warnings\n")
        if 'spectral_issues' in result['summary']:
            f.write(f"- **spectral issues:** {result['summary'].get('spectral_issues',0)}\n")
        f.write("\n---\n\n")
        if result["details"]["schema"]["errors"]:
            f.write("## Schema Errors\n\n")
            for e in result["details"]["schema"]["errors"]:
                f.write(f"- {md_escape(e)}\n")
            f.write("\n")
        if result["details"]["yamllint"]:
            f.write("## yamllint Findings\n\n")
            for item in result["details"]["yamllint"][:100]:
                level = item.get("level","info")
                msg = item.get("message","").strip()
                rule = item.get("rule","")
                rule_s = f" *(rule: {rule})*" if rule else ""
                f.write(f"- **{level}** — {md_escape(msg)}{rule_s}\n")
            if len(result["details"]["yamllint"]) > 100:
                f.write(f"\n(+{len(result['details']['yamllint'])-100} more)\n\n")
        if result["details"]["spectral"]:
            f.write("\n## Spectral Findings\n\n")
            for issue in result["details"]["spectral"][:100]:
                if isinstance(issue, dict):
                    msg = issue.get("message") or issue.get("raw") or str(issue)
                else:
                    msg = str(issue)
                f.write(f"- {md_escape(msg)}\n")
            if len(result["details"]["spectral"]) > 100:
                f.write(f"\n(+{len(result['details']['spectral'])-100} more)\n\n")

    # Handoff payload for Mode-Writer
    handoff = {
        "receiver_slug": "mode-writer",
        "handoff_type": "mode_validation_result",
        "summary_json": str(json_path.relative_to(root)),
        "summary_md": str(md_path.relative_to(root)),
        "status": result["summary"]["status"],
        "timestamp": result["timestamp"]
    }
    handoff_path = handoff_dir / "mode_validation_handoff.json"
    with open(handoff_path, "w", encoding="utf-8") as f:
        json.dump(handoff, f, indent=2, ensure_ascii=False)

    print(json.dumps({
        "ok": True,
        "summary_json": str(json_path),
        "summary_md": str(md_path),
        "handoff": str(handoff_path),
        "status": result["summary"]["status"]
    }))

if __name__ == "__main__":
    main()