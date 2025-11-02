````markdown
# ROOMAWS — Roo Orchestrated Operations: Multi-Agent Workflow System

**Version 1 (Beta)**  
Deterministic multi-agent orchestration with persistent memory, reproducible handoffs, and rule-bound execution modes.

[![License](https://img.shields.io/badge/license-Not%20Specified-lightgrey)]()
[![Agents/Modes](https://img.shields.io/badge/agents%2Fmodes-15%2B-blue)]()
[![Memory](https://img.shields.io/badge/memory-MCP%20Enabled-green)]()
[![Determinism](https://img.shields.io/badge/flows-deterministic-orange)]()

---

## Overview

**ROOMAWS** is a **memory-first, multi-mode AI orchestration layer** for complex software development and operations. Specialized agents coordinate through a persistent knowledge graph and deterministic handoff protocols, enabling auditable workflows, repeatable outcomes, and incremental learning across runs.

**Why it exists**
- Codebases need repeatable, **policy-compliant** automation.
- Multi-agent systems drift without **structured memory** and **guardrails**.
- Teams need **explainable** decisions, not opaque suggestions.

**What you get**
- A set of **specialized modes** (builder, tester, auditor, designer, spec-writer, mode-writer, etc.).
- A **Knowledge-Graph Memory MCP** to retain observations, fixes, regressions, and decisions.
- **Deterministic orchestration**: reproducible steps, explicit contracts, and rule-scoped file access.

---

## Core Concepts

- **Modes (Agents):** Single-purpose executors with strict read/write/command/browser fences.
- **Deterministic Handoffs:** Structured outputs → validated inputs across the chain.
- **Memory MCP:** Graph entities/relations/observations form a durable context plane.
- **Rules as Code:** `.roomodes`, `.roo/*`, and optional Conftest/OPA policies gate unsafe actions.

---

## System Architecture

```mermaid
flowchart TB
    User([User / CI]) -->|task| Orchestrator

    subgraph Orchestrator["ROOMAWS Orchestrator"]
      Router[[Task Router]]
      Policy[[Policy Gates]]
      MemoryIO[[Memory MCP I/O]]
      Router --> Policy --> MemoryIO
    end

    Orchestrator -->|plan| Planner[Sequential / Graph Planner]
    Planner -->|handoff| Modes

    subgraph Modes["Specialized Modes (examples)"]
      Builder[🧱 Code Builder]
      Tester[🧪 Test Runner]
      SecAuditor[🔐 Security Auditor]
      Designer[🎨 Design Engineer]
      DocMgr[📚 Docs Manager]
      ModeWriter[✍️ Mode Writer]
      SpecWriter[📋 Spec Writer]
      IssueResolver[🔧 Issue Resolver]
      MergeResolver[🔀 Merge Resolver]
    end

    MemoryIO <--> KG[(Knowledge Graph)]
    Modes <--> FS[(Repo / Filesystem)]
    Modes <--> Shell[(Commands)]
    Modes <--> Web[(Browser)]
````

---

## Knowledge Graph Memory (MCP)

ROOMAWS integrates a **Memory MCP server** supporting a minimal, auditable command set:

* `create_entities` / `create_relations`
* `add_observations`
* `delete_*` (entities, relations, observations)
* `read_graph`, `search_nodes`, `open_nodes`

**Usage model**

* Modes **append observations** (e.g., failed command, error trace, fix, outcome).
* Orchestrator **queries graph** for prior patterns, known fixes, and decisions.
* Relations describe **causality** (“Patch X **fixes** Error Y”, “Mode Z **validated** Commit C”).

**Benefits**

* Durable memory across sessions
* Citable decisions and provenance
* Safer automation via historical priors

```mermaid
erDiagram
  ENTITY ||--o{ RELATION : creates
  ENTITY {
    string id
    string name
    string type
    string provenance
  }
  OBSERVATION {
    string ulid
    string content
    string timestamp
    string originMode
    string severity
  }
  ENTITY ||--o{ OBSERVATION : has
```

---

## Features

* ✅ **Deterministic orchestration** with explicit mode contracts
* ✅ **Memory-first execution** (Knowledge Graph as source of truth)
* ✅ **Guardrails**: file regex fences, read/edit/command/browser scopes
* ✅ **Evidence-based** decisions and traceable handoffs
* ✅ **Meritocratic planner** (sequential or DAG-style) with policy gates
* ✅ **Drop-in** repo usage via `.roomodes` and `.roo/` directory

---

## Quickstart

### 1) Prerequisites

* Node.js / Python toolchain as required by your modes (varies by repo)
* A project with `.roomodes`, `.roo/` (mode tools, rules, prompts)
* Memory MCP server configuration (local or remote)

### 2) Install / Layout

Place ROOMAWS config at the project root:

```
<your-project>/
├─ .roomodes
├─ .roo/
│  ├─ mode-tools/
│  ├─ rules-*/ 
│  └─ prompts/
├─ src/
└─ README.md
```

> Keep the canonical paths: **`.roomodes`** (top-level mode spec) and **`.roo/`** (tools, rules, prompts).
> You can customize subfolders, but **do not** rename `.roomodes` unless you’ve updated all references.

### 3) Minimal `.roomodes` (example excerpt)

```yaml
customModes:
  - slug: orchestrator
    name: 🧭 Orchestrator
    description: Deterministic planner and router for ROOMAWS.
    roleDefinition: |
      You plan, gate via policy, query memory, and hand off tasks to specialist modes.
      Prefer deterministic steps, explicit contracts, and evidence capture.
    groups:
      - read
      - command
      - browser
      - edit:
          fileRegex: "^(src|docs|tests|.roo|.roomodes|README\\.md)(/|$)"
```

> RULE: **Exactly one `edit` group** with a single `fileRegex` is supported.
> Add other modes similarly (tester, designer, mode-writer, spec-writer, etc.).

---

## Deterministic Handoff Pattern

```yaml
handoff_contract:
  input_schema:
    type: object
    required: [objective, scope, constraints, artifacts]
    properties:
      objective: { type: string }
      scope: { type: array, items: { type: string } }
      constraints: { type: array, items: { type: string } }
      artifacts: { type: array, items: { type: string } }
  output_schema:
    type: object
    required: [changes, tests, memory_observations]
    properties:
      changes: { type: array, items: { type: string } }
      tests: { type: array, items: { type: string } }
      memory_observations:
        type: array
        items:
          type: object
          required: [ulid, content, severity, originMode]
          properties:
            ulid: { type: string }
            content: { type: string }
            severity: { type: string, enum: [info, warn, error] }
            originMode: { type: string }
```

---

## Example Flows

### A) “Fix a failing test” (summarized)

1. **Orchestrator** queries memory for prior related failures.
2. **Tester** reproduces error; logs observation.
3. **Builder** proposes patch; returns diff + tests.
4. **Tester** validates; **SecAuditor** checks sensitive patterns.
5. **Orchestrator** commits and updates memory with outcome & relations.

### B) “Draft a spec and implement”

1. **SpecWriter** drafts spec (source-of-truth).
2. **ModeWriter** generates/updates mode configs aligned to spec.
3. **Builder → Tester → DocMgr** complete the loop with verified artifacts.
4. Memory links **spec → decisions → changes → validations**.

---

## Configuration Notes

* **Paths:** Keep `.roomodes` and `.roo/` at repo root.
* **Policies (optional):** Add Conftest/OPA under `.roo/policy/` to gate commands/edits.
* **Secrets:** Never commit secrets; use environment injection with allow-lists.
* **CLI/Tasks:** If you expose a CLI, prefer `roomaws <task>` wrappers that set deterministic flags.

---

## Troubleshooting

* **Edits rejected:** Ensure only **one** `edit` group exists with a **single regex**.
* **Memory not updating:** Validate MCP endpoint and that modes call `add_observations`.
* **Planner loops:** Add stricter contracts or policy gates to bound step counts.
* **Permissions:** Confirm file regex includes the intended targets (e.g., `README.md`, `src/`, `tests/`).

---

## FAQ

**Q: Do I need to rename `.roo/` to `.roomaws/`?**
A: No. `.roo/` is canonical in the ecosystem. Keep it unless you’ve updated every reference.

**Q: Can I run without Memory MCP?**
A: Yes, but you lose cross-run learning and provenance. Recommended for full capability.

**Q: How many modes are supported?**
A: Common setups use 10–20. Focus on **single-purpose** agents with tight scopes.

---

## Roadmap (High-level)

* Planner DAG mode with topological execution checks
* Built-in policy packs (security, licenses, PII)
* First-class CHANGELOG/ADR emitters from memory events

---

## License

Not specified. Add a license to clarify usage.

---

### Branding

* **Product:** **ROOMAWS**
* **Repo/Package/CLI:** `roomaws`
* **Expansion:** Roo Orchestrated Operations: Multi-Agent Workflow System
* **Tagline:** Deterministic multi-agent ops—memory-first.

```
```
