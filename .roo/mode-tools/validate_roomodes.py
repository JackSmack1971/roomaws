#!/usr/bin/env python3
"""
Folder-agnostic validator for Roo Code `.roomodes`.
Placement: project_root/.roo/mode-tools/validate_roomodes.py

Behavior:
- If a file path is provided, validate that file.
- If no path is provided, walk upward from CWD to find the *project root* that contains `.roomodes` and validate it.
- Enforces: (1) no tabs anywhere, (2) indentation is a multiple of configured spaces, (3) JSON Schema validity, (4) security patterns, (5) structural requirements.
"""
import sys, re, json, yaml
from pathlib import Path
from jsonschema import Draft202012Validator

# Indentation size for the reference file (auto-detected when the pack was generated)
INDENT = 2

def find_project_root(start: Path) -> Path | None:
    cur = start.resolve()
    for p in [cur, *cur.parents]:
        if (p / ".roomodes").exists():
            return p
    return None

def load_schema(script_dir: Path):
    schema_path = script_dir / "roomodes.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)

def read_text(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def validate_yaml_tabs_and_indent(raw: str, indent: int):
    if "\t" in raw:
        raise SystemExit("Error: Tabs detected in file. Only spaces are allowed.")

    for i, line in enumerate(raw.splitlines(), 1):
        if not line.strip():
            continue
        m = re.match(r"^( +)", line)
        if m:
            n = len(m.group(1))
            if n % indent != 0:
                raise SystemExit(f"Error: Indentation not a multiple of {indent} spaces at line {i} (got {n}).")

def validate_mode_structure(mode_config):
    """Validate mode follows single edit tuple pattern"""
    errors = []
    warnings = []

    for mode in mode_config['customModes']:
        slug = mode['slug']
        groups = mode.get('groups', [])

        # Count edit tuples
        edit_count = sum(1 for g in groups if isinstance(g, list) and g[0] == 'edit')

        if edit_count > 1:
            errors.append({
                'mode': slug,
                'issue': 'Multiple edit tuples detected',
                'severity': 'CRITICAL',
                'description': 'Mode has multiple edit entries which can cause parser bugs'
            })
        elif edit_count == 0 and 'edit' in [g for g in groups if isinstance(g, str)]:
            warnings.append({
                'mode': slug,
                'issue': 'Edit permission without fileRegex',
                'description': 'Edit group should be restricted with fileRegex'
            })

    return errors, warnings

def validate_memory_file_naming(script_dir: Path):
    """Validate memory file naming convention across all mode directories"""
    errors = []

    roo_dir = script_dir.parent
    rules_dir = roo_dir / "rules"

    if not rules_dir.exists():
        return errors, []

    # Find all mode directories (rules-* pattern)
    mode_dirs = [d for d in rules_dir.iterdir() if d.is_dir() and d.name.startswith("rules-")]

    for mode_dir in mode_dirs:
        mode_name = mode_dir.name
        memory_files = []

        # Find all files starting with "40-memory-"
        for file_path in mode_dir.glob("40-memory-*.md"):
            memory_files.append(file_path.name)

        # Check for violations
        if len(memory_files) != 1:
            if len(memory_files) == 0:
                errors.append({
                    'mode': mode_name,
                    'issue': 'Missing memory file - must have exactly one file named 40-memory-io.md',
                    'severity': 'ERROR'
                })
            else:
                errors.append({
                    'mode': mode_name,
                    'issue': f'Multiple memory files found: {", ".join(memory_files)} - must have exactly one file named 40-memory-io.md',
                    'severity': 'ERROR'
                })
        elif memory_files[0] != "40-memory-io.md":
            errors.append({
                'mode': mode_name,
                'issue': f'Incorrect memory file name: {memory_files[0]} - must be named 40-memory-io.md',
                'severity': 'ERROR'
            })

        # Check for forbidden naming patterns
        forbidden_names = ["40-memory-integration.md", "40-memory-reads.md"]
        for forbidden in forbidden_names:
            if (mode_dir / forbidden).exists():
                errors.append({
                    'mode': mode_name,
                    'issue': f'Forbidden memory file name: {forbidden} - must use 40-memory-io.md',
                    'severity': 'ERROR'
                })

    return errors, []

def validate_memory_protocol_compliance(mode_config, script_dir: Path):
    """Validate that all modes have proper memory protocol integration"""
    errors = []
    warnings = []

    roo_dir = script_dir.parent
    rules_dir = roo_dir / "rules"

    for mode in mode_config['customModes']:
        slug = mode['slug']
        custom_instructions = mode.get('customInstructions', '')

        # Check for mandatory memory protocol structure
        required_phrases = [
            'MANDATORY MEMORY PROTOCOL',
            'PRE-FLIGHT:',
            'POST-FLIGHT:',
            'memory:search_nodes',
            'Write: Observation envelope',
            'Link: Relations',
            'Confirm: List entity IDs'
        ]

        missing_phrases = []
        for phrase in required_phrases:
            if phrase not in custom_instructions:
                missing_phrases.append(phrase)

        if missing_phrases:
            errors.append({
                'mode': slug,
                'issue': f'Missing memory protocol elements: {", ".join(missing_phrases)}',
                'severity': 'CRITICAL',
                'description': 'Mode must have complete memory protocol checkpoints in customInstructions'
            })

        # Check for corresponding memory file
        mode_rules_dir = rules_dir / f"rules-{slug}"
        if mode_rules_dir.exists():
            memory_file = mode_rules_dir / "40-memory-io.md"
            if not memory_file.exists():
                errors.append({
                    'mode': slug,
                    'issue': 'Missing corresponding 40-memory-io.md file',
                    'severity': 'ERROR',
                    'description': f'Expected file: {memory_file}'
                })
        else:
            warnings.append({
                'mode': slug,
                'issue': f'Missing mode rules directory: {mode_rules_dir}',
                'description': 'Mode should have corresponding rules directory with workflow and memory files'
            })

        # Check for workflow file with memory integration
        if mode_rules_dir.exists():
            workflow_file = mode_rules_dir / "10-workflow.md"
            if workflow_file.exists():
                try:
                    with open(workflow_file, 'r', encoding='utf-8') as f:
                        workflow_content = f.read()
                        if 'Memory Consultation' not in workflow_content:
                            warnings.append({
                                'mode': slug,
                                'issue': 'Workflow file missing memory consultation phase',
                                'description': '10-workflow.md should include Phase 0: Memory Consultation'
                            })
                except Exception as e:
                    warnings.append({
                        'mode': slug,
                        'issue': f'Could not read workflow file: {e}',
                        'description': 'Ensure 10-workflow.md is readable'
                    })

    return errors, warnings

def validate_security_patterns(mode_config, baseline):
    """Check for overly permissive or insecure fileRegex patterns"""

    errors = []
    warnings = []

    ineffective_patterns = [
        (r'(?!.*\w+)', 'Negative lookahead - use positive allowlist'),
        (r'\.\*(?!\)|\$)', 'Unanchored wildcard - add ^ and $'),
    ]

    for mode in mode_config['customModes']:
        slug = mode['slug']

        for group in mode.get('groups', []):
            if isinstance(group, list) and group[0] == 'edit':
                regex = group[1].get('fileRegex', '')

                # Check for ineffective patterns
                for pattern, msg in ineffective_patterns:
                    if re.search(pattern, regex):
                        warnings.append(f"{slug}: {msg}")

                # Test against forbidden patterns
                forbidden = baseline['forbidden_patterns']
                for name, pattern in forbidden.items():
                    test_paths = [
                        f"src/{name.replace('_files', '')}/file.ts",
                        f"lib/{name.replace('_files', '')}-service.ts"
                    ]
                    for test_path in test_paths:
                        if re.match(regex, test_path):
                            errors.append({
                                'mode': slug,
                                'issue': f'Can access forbidden {name}',
                                'path': test_path,
                                'severity': 'HIGH'
                            })

    return errors, warnings

def main(argv):
    script_dir = Path(__file__).resolve().parent

    if len(argv) > 2:
        print("Usage: validate_roomodes.py [optional_path_to_roomodes]", file=sys.stderr)
        sys.exit(2)

    if len(argv) == 2:
        target = Path(argv[1]).resolve()
        if target.is_dir():
            target = target / ".roomodes"
    else:
        root = find_project_root(Path.cwd())
        if root is None:
            print("Error: Could not find project root containing `.roomodes` by walking upward from CWD.", file=sys.stderr)
            sys.exit(1)
        target = root / ".roomodes"

    if not target.exists():
        print(f"Error: `{target}` does not exist.", file=sys.stderr)
        sys.exit(1)

    raw = read_text(target)
    validate_yaml_tabs_and_indent(raw, INDENT)

    data = yaml.safe_load(raw)

    schema = load_schema(script_dir)
    v = Draft202012Validator(schema)
    errors = sorted(v.iter_errors(data), key=lambda e: (list(e.path), e.message))
    if errors:
        for e in errors:
            loc = "/".join(map(str, e.path)) or "(root)"
            print(f"Schema error at {loc}: {e.message}", file=sys.stderr)
        sys.exit(1)

    # Load security baseline
    baseline_path = script_dir / "security_baseline.json"
    with open(baseline_path, "r", encoding="utf-8") as f:
        baseline = json.load(f)

    # Run structural validation
    struct_errors, struct_warnings = validate_mode_structure(data)
    if struct_errors:
        print("Structural validation errors:", file=sys.stderr)
        for error in struct_errors:
            print(f"  {error['mode']}: {error['issue']} ({error['severity']})", file=sys.stderr)
        sys.exit(1)

    # Run memory file naming validation
    mem_errors, mem_warnings = validate_memory_file_naming(script_dir)
    if mem_errors:
        print("Memory file naming validation errors:", file=sys.stderr)
        for error in mem_errors:
            print(f"  {error['mode']}: {error['issue']} ({error['severity']})", file=sys.stderr)
        sys.exit(1)

    # Run memory protocol compliance validation
    mem_proto_errors, mem_proto_warnings = validate_memory_protocol_compliance(data, script_dir)
    if mem_proto_errors:
        print("Memory protocol compliance validation errors:", file=sys.stderr)
        for error in mem_proto_errors:
            print(f"  {error['mode']}: {error['issue']} ({error['severity']})", file=sys.stderr)
            if 'description' in error:
                print(f"    {error['description']}", file=sys.stderr)
        sys.exit(1)

    # Run security validation
    sec_errors, sec_warnings = validate_security_patterns(data, baseline)
    if sec_errors:
        print("Security validation errors:", file=sys.stderr)
        for error in sec_errors:
            print(f"  {error['mode']}: {error['issue']} - {error['path']} ({error['severity']})", file=sys.stderr)
        sys.exit(1)

    # Report warnings
    all_warnings = struct_warnings + sec_warnings + mem_warnings + mem_proto_warnings
    if all_warnings:
        print("Warnings:")
        for warning in all_warnings:
            if isinstance(warning, dict):
                print(f"  {warning['mode']}: {warning['issue']}")
                if 'description' in warning:
                    print(f"    {warning['description']}")
            else:
                print(f"  {warning}")

    print(f"OK: `{target}` formatting, schema, structural, security, and memory file naming validation passed.")

if __name__ == "__main__":
    main(sys.argv)