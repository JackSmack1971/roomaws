# .roo/rules-docs-manager/20-documentation-patterns.md
> Templates and patterns for structuring **source material** and **verification** findings.

## User-Focused Template
# [Feature Name]

[Why it matters to a user.]

### Key Features
- [Benefit 1]
- [Benefit 2]
- [Benefit 3]

---

## Use Case
**Before**: [Old way / pain points]  
**With this feature**: [Outcome & improvements]

## How it Works
[Simple operation summary + where visuals help.]

## Configuration
1. **[Setting]**
   - **Key**: `[technical_name]`
   - **Default**: [value]
   - **Effect**: [user impact]

2. **[Setting]**
   - **Key**: `[technical_name]`
   - **Default**: [value]
   - **Effect**: [user impact]

## Troubleshooting
- **Symptom** → Causes → Fixes → Prevention

## FAQ
**“[User question]”** — [Answer]

---

## Comprehensive (internal) Outline
- Overview / Quick Start / Architecture / API / Config / User Guide / Developer Guide / Security / Performance / Troubleshooting / FAQ / Changelog / References

## Cross-references (patterns)
- Internal links: `[See Configuration](#configuration)`
- External links: `[Official Documentation](https://...)`
- Related features block; See-also block.

## Evidence & Memory
- For any claim: attach `doc.note` and link `Doc REFERENCES Concept`.
- When a fix changes behavior: add `fix.apply`, link `Fix DERIVED_FROM Doc`.
