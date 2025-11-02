import json
import re
import yaml

# Load security baseline
with open('.roo/mode-tools/security_baseline.json', 'r') as f:
    baseline = json.load(f)

# Load roomodes
with open('.roomodes', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

print('Testing fileRegex patterns against security baseline...')
print('=' * 60)

forbidden_patterns = baseline['forbidden_patterns']
test_paths = [
    'src/auth/login.ts',
    'src/authentication/utils.ts',
    'src/payment/processor.ts',
    'src/billing/invoice.ts',
    'src/security/encryption.ts',
    'src/admin/dashboard.ts',
    'src/config/credentials.ts',
    '.env.production',
    'src/secrets/keys.ts'
]

violations = []

for mode in config['customModes']:
    slug = mode['slug']
    groups = mode.get('groups', [])

    for group in groups:
        if isinstance(group, list) and group[0] == 'edit':
            regex_str = group[1].get('fileRegex', '')
            if regex_str:
                try:
                    regex = re.compile(regex_str)
                    for test_path in test_paths:
                        if regex.match(test_path):
                            # Check which forbidden pattern it matches
                            for forbidden_name, forbidden_pattern in forbidden_patterns.items():
                                if re.search(forbidden_pattern, test_path):
                                    violations.append({
                                        'mode': slug,
                                        'pattern': regex_str,
                                        'forbidden_path': test_path,
                                        'forbidden_type': forbidden_name
                                    })
                                    break
                except re.error as e:
                    violations.append({
                        'mode': slug,
                        'pattern': regex_str,
                        'error': str(e)
                    })

if violations:
    print(f'X FOUND {len(violations)} SECURITY VIOLATIONS:')
    print()
    for v in violations:
        if 'error' in v:
            print(f'  {v["mode"]}: REGEX ERROR - {v["error"]}')
            print(f'    Pattern: {v["pattern"]}')
        else:
            print(f'  {v["mode"]}: Allows access to {v["forbidden_type"]}')
            print(f'    Forbidden path: {v["forbidden_path"]}')
            print(f'    Pattern: {v["pattern"]}')
        print()
else:
    print('OK: No security violations found')