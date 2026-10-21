# AI Project Bootstrap

A reusable, product-neutral standard for consistent AI planning and execution workflows across new and existing projects — ChatGPT with Codex and Claude with Claude Code, on macOS, Windows and Linux.

**Current standard:** v3.0.0 (single version source: [`VERSION`](VERSION))

> **New here? Start with the guided setup.** You need the ChatGPT or Claude desktop app and a subscription. Download `START_HIER.md`, give it to a new session in the app's code area (Codex or Claude Code) and write „Start“. It guides you in simple German, one current step at a time: connect GitHub, install the important skills, set up your working rules and the AI's permissions together, and try everything on your first project up to the merge. See [Guided personal setup](#guided-personal-setup).

> **New-project default: own task-branch commit/push is enabled.** After an explicitly started task passes its required checks, the executor may commit and push only that task's dedicated branch. This does not permit main/default-branch push, another task's branch, merge, release/tag, deployment or production/provider activation, and does not start a recommended follow-up. At setup you can choose **DISABLED** (opt out of commit/push) or **PER_TASK_APPROVAL** instead of **ALLOW_AFTER_CHECKS**. ChatGPT must prominently repeat this notice in its setup response and record the effective policy in your authoritative project instructions before relying on it. Existing projects keep their active restrictions; a standard version does not grant permission retrospectively.

> **v3.0.0: LIGHT merge and deployment by default for new projects.** The executor merges its own task PRs after the project's checks passed locally on the current head (rechecked if `main` moved, merge bound to the checked commit) and deploys to the project's recorded target; production with real user data needs one Owner decision per project. Foreign and fork PRs are never merged. If LIGHT proves too error-prone, the executor raises it and the Owner chooses **GATE** or **PER_CHANGE_APPROVAL**. Existing projects keep their rules. See [merge and deployment policy](UNIVERSAL_PROJECT_BOOTSTRAP.md#merge-and-deployment-policy).

> **v2.0.0: dev-box merge gate and no automatic hosted CI.** Projects check PRs on their actual merge result and releases on the exact current commit with a deliberately started local gate. GitHub-hosted CI starts at most through manual `workflow_dispatch` for diagnosis. Once a project's gate is integrated, its own explicitly mergeable task PRs without open decisions may be merged automatically by the gate; foreign PRs never are, and deployment always stays a separate project decision. See [`DEVBOX_GATE_POLICY.md`](DEVBOX_GATE_POLICY.md). Branch push authority above is still not merge authority.

## Quick start (personal setup already done)

1. Make your project repository available to ChatGPT (or to Claude / Claude Code; see [`plugins/ai-bootstrap/skills/einrichtung/references/claude-code.md`](plugins/ai-bootstrap/skills/einrichtung/references/claude-code.md) for the Claude Code specifics).
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

## Guided personal setup

The guided setup assumes the ChatGPT or Claude desktop app and a subscription. It only sets up and connects the essentials, once per computer, and is reused for every further project. It ships as the plugin [`plugins/ai-bootstrap`](plugins/ai-bootstrap/.claude-plugin/plugin.json) with three skills (German):

- [`einrichtung`](plugins/ai-bootstrap/skills/einrichtung/SKILL.md): seven steps – `start` (silent check), `github` (what and why, account, CLI login, commit identity), `skills` (Superpowers and ai-bootstrap), `arbeitsweise` (personal rules and the AI's permission profile, set up together), `projekt`, `probelauf` (the real project-rules PR, merged with the LIGHT mechanics after one explicit approval), `fertig`; `gate` only for projects that choose GATE. Provider and OS details are in its [`references/`](plugins/ai-bootstrap/skills/einrichtung/references/linux.md); Windows runs natively, WSL 2 only for the gate.
- [`projekt-start`](plugins/ai-bootstrap/skills/projekt-start/SKILL.md): new or existing project, creating a project in the ChatGPT or Claude app and connecting the repository, this standard with publication and merge/deployment policy, and a critical server/dev-box consultation (advice only).
- [`arbeitsweise`](plugins/ai-bootstrap/skills/arbeitsweise/SKILL.md): the always-on working rules – „Frage X von Y“ with options and a recommendation, explaining along the way, check before asking, and the merge/deployment procedure with escalation. A short marked block in `~/.claude/CLAUDE.md` or `~/.codex/AGENTS.md` keeps them active in every session.

- **Entry:** `START_HIER.md`, generated by `python3 scripts/build_bootstrap_bundle.py --output-dir <dir>` together with `AI-Bootstrap-<version>.zip` (offline copy including the plugin) and `SHA256SUMS`. It is short: it checks that the AI can run commands (otherwise a two-sentence hint to use the app's code area), fetches the skills from this public repository at the exact source commit and follows `einrichtung`.
- **Installation:** Claude Code installs the plugin from this repository's marketplace ([`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json)); Codex gets the same `SKILL.md` folders as personal skills in `~/.agents/skills`.
- **Resumable state:** a secret-free JSON file ([schema](plugins/ai-bootstrap/skills/einrichtung/references/STATE.schema.json), validated and migrated from version 1 by [`onboarding_state.py`](plugins/ai-bootstrap/skills/einrichtung/scripts/onboarding_state.py)); decisions are kept, access and installations are re-checked.
- **Acceptance:** [dialog and platform cases](https://github.com/robin-shiels/ai-project-bootstrap/blob/main/docs/GUIDED_SETUP_ACCEPTANCE.md). Dialog tests, package tests and real platform tests are reported separately; a simulation is no platform proof.

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
- a merge and deployment policy per project (LIGHT by default, the local dev-box gate as the stronger option), and hosted CI only by manual dispatch;
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

## Dev-box merge gate

The gate is the **GATE** choice of the merge and deployment policy, the stronger option next to the LIGHT default. [`DEVBOX_GATE_POLICY.md`](DEVBOX_GATE_POLICY.md) is the contract. It runs natively on Linux (reference) and macOS and inside WSL 2 on Windows ([platforms](DEVBOX_GATE_POLICY.md#10-platforms)). The reference CLI [`templates/devbox_merge_gate.py`](templates/devbox_merge_gate.py) (Python 3.12+, standard library, `git` and `gh`) is configured by a strictly validated TOML file ([example](templates/devbox_merge_gate.example.toml)); its tests run with `python3 -m unittest discover -s tests` against temporary repositories and fakes only (the same command also runs the setup-state and bundle tests). Adopt it per project with the [rollout checklist](templates/DEVBOX_GATE_ROLLOUT_CHECKLIST.md) and the [AGENTS.md](templates/AGENTS_DEVBOX_GATE.md) / [CLAUDE.md](templates/CLAUDE_DEVBOX_GATE.md) rule texts. An optional manual diagnosis workflow is in [`templates/github-actions-diagnose.example.yml`](templates/github-actions-diagnose.example.yml). This repository itself has no runner and one workflow: the manually started [platform test](https://github.com/robin-shiels/ai-project-bootstrap/blob/main/docs/PLATFORM_TESTS.md) for macOS and native Windows (owner decision 2026-10-19).

## Repository structure

```text
.
├── README.md
├── VERSION
├── UNIVERSAL_PROJECT_BOOTSTRAP.md
├── DEVBOX_GATE_POLICY.md
├── CHANGELOG.md
├── LICENSE
├── .claude-plugin/
│   └── marketplace.json        Claude Code marketplace for the plugin
├── plugins/ai-bootstrap/       guided setup as plugin (German)
│   ├── .claude-plugin/plugin.json
│   └── skills/
│       ├── einrichtung/        SKILL.md, references/ (providers, OSes, state schema), scripts/onboarding_state.py
│       ├── projekt-start/      SKILL.md
│       └── arbeitsweise/       SKILL.md
├── scripts/
│   ├── build_bootstrap_bundle.py
│   └── probe_gate_host.py
├── skills/
│   └── SKILL_MANIFEST.md
├── templates/
│   ├── CODEX_BOOTSTRAP_PROMPT.md
│   ├── PROJECT_DISCOVERY.md
│   ├── devbox_merge_gate.py
│   ├── devbox_merge_gate.example.toml
│   ├── AGENTS_MERGE_LIGHT.md / CLAUDE_MERGE_LIGHT.md
│   ├── AGENTS_DEVBOX_GATE.md
│   ├── CLAUDE_DEVBOX_GATE.md
│   ├── DEVBOX_GATE_ROLLOUT_CHECKLIST.md
│   └── github-actions-diagnose.example.yml
├── tests/
│   ├── test_devbox_merge_gate.py
│   ├── test_onboarding_state.py
│   ├── test_plugin.py
│   └── test_bootstrap_bundle.py
└── docs/                       design, research and result records (not part of the bundle)
```

The `.gitignore` only excludes Python bytecode of the reference CLI and its tests.

## Versioning

The standard uses semantic versions. A target project may record its last reconciled version, for example:

`Universal Project Bootstrap: v3.0.0`

That marker is useful but never replaces semantic inspection on a future upgrade.

When upgrading from v2.1.0 to v3.0.0, an existing project keeps its effective merge and deployment rules: a project with an integrated gate records GATE, one without merge grant records PER_CHANGE_APPROVAL, and switching to LIGHT is an Owner decision. When upgrading from v2.0.x to v2.1.0, nothing in an existing project's rules changes; the guided setup is new and optional for people who already have a working environment, and the gate gains macOS and WSL 2 support. When upgrading from v1.1.0 to v2.0.0, inventory workflows, branch rules and merge rules first and adopt the gate through a scoped project task; existing stricter merge rules stay CONFLICT until the owner changes them. When upgrading from v1.0.0, reconcile behavior rather than replacing local instructions. Preserve existing restrictive commit/push rules until an explicit Owner change; show the concrete conflict with a proposed default B policy. Already equivalent own-branch permission stays intact without re-approval. See [CHANGELOG.md](CHANGELOG.md) for migration details. Branch completion does not claim integration or deployment; recheck current main and affected gates before any separately authorized integration.

## Relationship to automation/software factories

This repository defines the workflow contract. A separate automation system or software factory may automate parts of that workflow and may therefore need different internal execution rules.

The bootstrap standard should not be coupled to one automation implementation.

The [six-audit synthesis](https://github.com/robin-shiels/ai-project-bootstrap/blob/main/research/SIX_AUDIT_BOOTSTRAP_SYNTHESIS_2026-09-29.md) records the pinned evidence and Owner decision behind v1.1.0. Research reports remain source material, not independent execution grants.

## Contributing

Keep contributions product-neutral and broadly reusable. A rule belongs here when it solves a recurring cross-project workflow problem. Product-specific behavior belongs in the product repository.

## License

MIT.
