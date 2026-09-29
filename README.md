# AI Project Bootstrap

A reusable, product-neutral standard for consistent ChatGPT planning and Codex execution workflows across new and existing projects.

**Current standard:** v1.0.0

## Quick start

1. Make your project repository available to ChatGPT.
2. Give ChatGPT [`UNIVERSAL_PROJECT_BOOTSTRAP.md`](UNIVERSAL_PROJECT_BOOTSTRAP.md).
3. Say:

> Bootstrap this project according to `UNIVERSAL_PROJECT_BOOTSTRAP.md`. Inventory the current project first. Do not invent product-specific rules. Stop only for genuine conflicts or owner decisions.

4. ChatGPT first inventories existing rules, skills and workflows.
5. It preserves equivalent behavior, fills gaps, upgrades outdated universal behavior when safe, and asks you about genuine conflicts.
6. If project-specific instructions are missing, it uses structured brainstorming/discovery instead of inventing requirements.
7. When the ChatGPT side is ready, it outputs a **Codex bootstrap prompt**.
8. Copy that prompt into Codex.
9. Codex independently inventories and reconciles its rules, skills, Git workflow, quality gates and completion contracts.

The same process works for an existing project and can be re-run after the standard is updated.

## Reconciliation model

Every relevant capability is classified as:

- **MISSING** — add it;
- **EQUIVALENT** — preserve it, do not duplicate;
- **OUTDATED** — upgrade to the newer universal contract when project-specific intent remains intact;
- **CONFLICT** — do not choose silently; ask the owner.

A matching filename, rule title or skill name is not enough. Bootstrap compares actual behavior.

## What is universal?

The standard covers reusable workflow behavior such as:

- robust repository discovery and code-search fallback;
- current repository evidence before old chat assumptions;
- autonomous planning/research until a real owner decision or execution-ready handoff;
- durable Git-tracked work orders plus short execution prompts;
- recommendation-only next-chat guidance;
- compact current-work status before recommendations;
- parallel-work awareness;
- ChatGPT ↔ Codex handoff;
- universal skill/capability contracts;
- safe re-bootstrap and version upgrades.

It intentionally does **not** define your product, domain model, architecture, security policy or deployment environment.

## Universal vs project-specific

```text
Universal Project Bootstrap
        │
        ├── universal workflow rules
        ├── universal skill contracts
        ├── ChatGPT planning/research workflow
        └── Codex execution/handoff workflow
                     +
Target project
        ├── product/domain rules
        ├── architecture
        ├── security/privacy
        ├── project quality gates
        └── deployment/provider constraints
```

Project-specific rules are preserved and never copied back into this public standard just because one project needs them.

## Skills

See [`skills/SKILL_MANIFEST.md`](skills/SKILL_MANIFEST.md).

The manifest defines capabilities and expected behavior. It does **not** assume that a Markdown file is an installed skill or that two skills with the same name are equivalent.

## Project discovery

For a new or underspecified project, [`templates/PROJECT_DISCOVERY.md`](templates/PROJECT_DISCOVERY.md) provides coverage for structured brainstorming. Existing repository context is inspected first, so the owner should only be asked genuine unresolved questions.

## Codex bootstrap

ChatGPT uses [`templates/CODEX_BOOTSTRAP_PROMPT.md`](templates/CODEX_BOOTSTRAP_PROMPT.md) to produce the final project-specific prompt that you copy into Codex.

ChatGPT and Codex remain separate layers: configuring one does not falsely imply that the other is configured.

## Repository structure

```text
.
├── README.md
├── UNIVERSAL_PROJECT_BOOTSTRAP.md
├── CHANGELOG.md
├── LICENSE
├── skills/
│   └── SKILL_MANIFEST.md
└── templates/
    ├── CODEX_BOOTSTRAP_PROMPT.md
    └── PROJECT_DISCOVERY.md
```

No technology-specific `.gitignore` is included yet because this repository currently contains only portable documentation/templates and assumes no runtime stack.

## Versioning

The standard uses semantic versions. A target project may record its last reconciled version, for example:

`Universal Project Bootstrap: v1.0.0`

That marker is useful but never replaces semantic inspection on a future upgrade.

## Relationship to automation/software factories

This repository defines the workflow contract. A separate automation system or software factory may automate parts of that workflow and may therefore need different internal execution rules.

The bootstrap standard should not be coupled to one automation implementation.

## Contributing

Keep contributions product-neutral and broadly reusable. A rule belongs here when it solves a recurring cross-project workflow problem. Product-specific behavior belongs in the product repository.

## License

MIT.
