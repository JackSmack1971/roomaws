# .roo/rules-security-auditor/50-report-template.md
> Use this structure for PR comments or audit summaries

## Summary
- Scope: repo/PR, date
- Risk posture snapshot: **Critical(X)/High(Y)/Med(Z)/Low(W)**

## Key Findings (top N)
- [Rule/ID or CVE] — short description → **Proposed fix** (1–2 lines)
- Evidence: file@line, query/result id, package@version

## SBOM & Vuln
- SBOM artifact: `sbom.json` (CycloneDX/SPDX)
- Vulnerabilities summary: top ecosystems/images (link to JSON)

## Code & Config
- CodeQL: top rule hits (with links), FP notes
- Semgrep: policy gaps or framework-specific rules to add

## Supply Chain
- Dependabot posture; grouped updates recommended
- SLSA next steps (L2→L3) and signing/provenance recommendations

## Memory Links
- `err#…` / `warn#…` / `fix#…` / `doc#…` references recorded
