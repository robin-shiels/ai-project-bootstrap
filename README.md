# AI Project Bootstrap

A reusable, product-neutral standard for consistent ChatGPT planning and Codex execution workflows across new and existing projects.

**Current standard:** v1.1.0

> **New-project default: own task-branch commit/push is enabled.** After an explicitly started task passes its required checks, the executor may commit and push only that task's dedicated branch. This does not permit main/default-branch push, another task's branch, merge, release/tag, deployment or production/provider activation, and does not start a recommended follow-up. At setup you can choose **DISABLED** (opt out of commit/push) or **PER_TASK_APPROVAL** instead of **ALLOW_AFTER_CHECKS**. ChatGPT must prominently repeat this notice in its setup response and record the effective policy in your authoritative project instructions before relying on it. Existing projects keep their active restrictions; v1.1.0 does not grant permission retrospectively.

## Quick start

1. Make your project repository available to ChatGPT.
2. Give ChatGPT [`UNIVERSAL_PROJECT_BOOTSTRAP.md`](UNIVERSAL_PROJECT_BOOTSTRAP.md).
3. Say:

> Bootstrap this project according to `UNIVERSAL_PROJECT_BOOTSTRAP.md`. Inventory the current project first. Do not invent product-specific rules. Stop only for genuine conflicts or owner decisions.

4. ChatGPT resolves the actual repository/default branch and inventories existing rules, skills, workflows and commit/push authority with source/revision evidence.
5. For a new project it prominently explains the default above, offers opt-out/per-task approval and records the effective choice; default B does not require an affirmative selection after notice. For an existing project it preserves current authority, flags an incompatible restrictive policy as CONFLICT, and obtains any missing scoped authority before publication.
6. It preserves equivalent behavior, fills gaps, upgrades outdated universal behavior when safe, and asks you about genuine conflicts.
7. If project-specific instructions are missing, it uses structured brainstorming/discovery instead of inventing requirements.
8. When the ChatGPT side is ready, it outputs a **Codex bootstrap prompt** with the policy source and durable order.
9. Copy that prompt into Codex.
10. Codex independently inventories and reconciles its rules, skills, Git workflow, quality gates and completion contracts. It verifies and publishes only its own task branch when authorized, then returns a compact evidence-based handoff.

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
- durable canonical orders and results (normally Git-tracked) plus short execution prompts;
- visible own-branch publication policy with opt-out and existing-rule preservation;
- task-appropriate checks and distinct local, branch, integration and deployment states;
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

`Universal Project Bootstrap: v1.1.0`

That marker is useful but never replaces semantic inspection on a future upgrade.

When upgrading from v1.0.0, reconcile behavior rather than replacing local instructions. Preserve existing restrictive commit/push rules until an explicit Owner change; show the concrete conflict with a proposed default B policy. Already equivalent own-branch permission stays intact without re-approval. See [CHANGELOG.md](CHANGELOG.md) for migration details. Branch completion does not claim integration or deployment; recheck current main and affected gates before any separately authorized integration.

## Relationship to automation/software factories

This repository defines the workflow contract. A separate automation system or software factory may automate parts of that workflow and may therefore need different internal execution rules.

The bootstrap standard should not be coupled to one automation implementation.

The [six-audit synthesis](research/SIX_AUDIT_BOOTSTRAP_SYNTHESIS_2026-09-29.md) records the pinned evidence and Owner decision behind v1.1.0. Research reports remain source material, not independent execution grants.

## Contributing

Keep contributions product-neutral and broadly reusable. A rule belongs here when it solves a recurring cross-project workflow problem. Product-specific behavior belongs in the product repository.

## License

MIT.
