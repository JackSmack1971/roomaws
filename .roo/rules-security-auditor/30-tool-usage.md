# .roo/rules-security-auditor/30-tool-usage.md
> Deterministic commands & outputs (store heads only)

## SBOM
- Syft: `syft packages dir:. -o cyclonedx-json > sbom.json` (or `docker sbom <image> -o cyclonedx-json`).

## Vulnerabilities
- Grype (file/dir/image): `grype . -o json > grype.json` (air-gapped DB options available).
- Trivy (repo/image): `trivy repo . -f json > trivy.json` or `trivy image <img> -f json > trivy.json`.

## Static Analysis
- CodeQL: default or security-extended suites; export SARIF.
- Semgrep: `semgrep --config=p/owasp-top-ten --json > semgrep.json` (add custom rules).

## Dependency Hygiene
- Dependabot config & grouping: see `dependabot.yml` options.

# .roo/rules-security-auditor/30-tool-usage.md
> Deterministic commands & outputs (store heads only)

## Browser Usage
- **Allowed domains**: cve.mitre.org, nvd.nist.gov, owasp.org, github.com (security advisories), docs.github.com (security docs)
- **Purpose**: Access live CVE databases, security advisories, and vulnerability documentation
- **Security measures**:
  - No JavaScript execution
  - 30-second timeout per request
  - 1MB content size limit
  - No credential/form submission
  - Read-only access only
- **Risk mitigation**: SSRF protection via domain allowlist; no external redirects followed

## SBOM
- Syft: `syft packages dir:. -o cyclonedx-json > sbom.json` (or `docker sbom <image> -o cyclonedx-json`).

## Vulnerabilities
- Grype (file/dir/image): `grype . -o json > grype.json` (air-gapped DB options available).
- Trivy (repo/image): `trivy repo . -f json > trivy.json` or `trivy image <img> -f json > trivy.json`.

## Static Analysis
- CodeQL: default or security-extended suites; export SARIF.
- Semgrep: `semgrep --config=p/owasp-top-ten --json > semgrep.json` (add custom rules).

## Dependency Hygiene
- Dependabot config & grouping: see `dependabot.yml` options.
