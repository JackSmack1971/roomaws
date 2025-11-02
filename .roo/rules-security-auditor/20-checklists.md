# .roo/rules-security-auditor/20-checklists.md
> Field checklists mapped to standards

## App Code
- Input validation, output encoding, authz boundaries, crypto usage, secrets handling → map to **ASVS v5** sections.
- Common pitfalls: injection, authz bypass, insecure deserialization, SSRF, XXE → **OWASP Top 10** categories.

## Dependencies
- Generate SBOM (CycloneDX/SPDX). Ensure lockfiles present; pin indirects where feasible.
- Automate: Dependabot security updates, grouped by ecosystem.

## Containers & IaC
- Minimal base, rootless where possible; known-good registry.
- Scan images & IaC in CI; break-glass only with documented justification.

## Build & Provenance
- Reproducible builds; signed provenance; aim SLSA Build L2→L3 in CI roadmap.
