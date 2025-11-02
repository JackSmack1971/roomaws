# 20-evidence-and-citations.md
> Applies to all modes. Encodes how to **research, verify, cite, and archive** sources used to create or justify fixes, decisions, and documentation.

## Goals
- Ensure every material claim or remediation is **evidence-backed**, **verifiable later**, and **resilient to link rot**.  
- Standardize how modes **capture source metadata** into the memory graph (`Doc` nodes + `DERIVED_FROM` relations).  
- Prefer **primary, persistent identifiers** (e.g., DOI) and **archived snapshots** alongside live URLs. :contentReference[oaicite:0]{index=0}

---

## Evidence Hierarchy (use strongest available)
1) **Primary sources**: official docs/specs, release notes, RFCs/standards, upstream repository code/commits, vendor advisories.  
2) **Secondary**: reputable tech orgs, standards bodies, high-quality trade press performing original analysis.  
3) **Tertiary**: forums, random blogs, AI outputs — use only when 1/2 are unavailable, and flag as low-confidence.  
4) **Scholarly**: if citing research, **prefer DOI** and display it as `https://doi.org/<DOI>` (not `doi:` or `dx.doi.org`). :contentReference[oaicite:1]{index=1}

---

## Required Metadata (for each `Doc` node)
Capture and store as the observation payload `doc.note`:
```json
{
  "url": "<canonical URL or DOI URL>",
  "title": "<page or paper title>",
  "site": "<publisher/org>",
  "author": "<org or person if available>",
  "published_at": "<ISO8601 or YYYY-MM-DD if known>",
  "accessed_at": "<ISO8601>",
  "archive_url": "<Wayback or Perma.cc snapshot if available>",
  "excerpt": "<<=500 chars, verbatim>"
}
````

* **Always include an “Accessed” date** for web sources (web pages change). ([otis.libguides.com][1])
* For papers/articles with DOIs, **use the DOI URL** as the canonical link. ([www.crossref.org][2])

---

## Archival & Link-Rot Mitigation

* On first use of any web source, attempt to **save a snapshot** and record its URL:

  * **Wayback Machine → Save Page Now** for a point-in-time capture. ([archivesupport.zendesk.com][3])
  * **Perma.cc** when available for durable legal/academic preservation. ([Harvard Law Review][4])
* Why archive? Studies show **~70% of law-journal URLs and ~50% in U.S. Supreme Court opinions** fail over time; large scholarly crawls also find widespread **reference rot (content drift)**. ([Harvard Law Review][4])
* Prefer **stable identifiers** (e.g., **DOI**). W3C guidance: design links to be persistent — **cool URIs don’t change**. ([W3C][5])
* Optional user tip: Google now surfaces Wayback links in result menus, easing snapshot discovery. ([The Verge][6])

---

## Verification Procedure (every claim/fix)

1. **Locate** the strongest source per hierarchy; if only tertiary exists, mark `[Low-confidence]`.
2. **Confirm** the claim text vs. source; prefer **exact release notes/spec text** for technical behaviors.
3. **Archive** the page; add `archive_url`. (Wayback “Save Page Now”.) ([archivesupport.zendesk.com][3])
4. **Record** `doc.note` with metadata + short **verbatim excerpt** (≤ 500 chars).
5. **Link** evidence: `(:Fix)-[:DERIVED_FROM]->(:Doc)` and `(:Doc)-[:REFERENCES]->(:Concept)`.
6. **Re-check** for DOI: if present, store the **DOI URL** as canonical. ([www.crossref.org][2])

---

## Citing in Commits / PR Descriptions

Use compact, durable citations:

```
Refs: <Title> — <Site/Publisher> — <DOI URL or canonical URL>
Archived: <Wayback/Perma URL>
Accessed: <YYYY-MM-DD>
Key excerpt: "<<=200 chars verbatim>"
```

* For long rationales, place a short **Evidence** section at the end of the PR.

---

## Quotation & Paraphrase Rules

* **Prefer paraphrase** + link; use **short, exact quotes** only where wording is normative (e.g., spec text).
* Limit quotes to what’s essential; include **page/section anchors** when available.
* Always attribute to the **original publisher** and include **Accessed** + **Archive** links for web sources. ([otis.libguides.com][1])

---

## What NOT to do (anti-patterns)

* Citing **random gists, screenshots, or unauthenticated mirrors** as primary evidence.
* Linking to **dx.doi.org** or `doi:` instead of `https://doi.org/…`. ([www.crossref.org][2])
* Omitting **Accessed** dates and archive links for mutable web pages. ([otis.libguides.com][1])
* Treating moving blog posts as stable without an archive snapshot. **Reference rot** is real. ([Harvard Law Review][4])

---

## Notes for Site Builders (for internal docs)

If you control the documentation site, adopt persistent URL design: avoid content-bearing paths and extensions; keep status/access out of the path; ensure redirects maintain a **stable canonical**. (“Cool URIs don’t change.”) ([W3C][5])

---