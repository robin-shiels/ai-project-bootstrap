# Universal Project Bootstrap Standard

**Version:** 1.0.0  
**Scope:** product-neutral ChatGPT + Codex workflow bootstrap  
**Mode:** inventory-first, idempotent, conflict-aware

## Purpose

Bring new and existing projects to a consistent AI-assisted workflow without blindly replacing what already works. Product goals, domain rules, architecture, security/privacy and deployment constraints remain project-specific.

Every run follows:

**Inventory → Compare → Classify → Reconcile → Discover missing project specifics → Validate → Generate Codex handoff**

## Inventory first

Before changing rules or skills:

1. resolve the project's authoritative repository/default branch;
2. inspect authoritative instructions and workflow documentation;
3. inventory available skills/capabilities and their actual behavior where discoverable;
4. inventory Git/task/planning/research/audit/implementation conventions;
5. identify project-specific rules that must be preserved;
6. compare semantics with this standard.

A matching filename or skill name is not proof of equivalent behavior.

Classify each universal capability:

- **MISSING** — no equivalent exists;
- **EQUIVALENT** — current behavior satisfies the contract;
- **OUTDATED** — same intent exists but the universal contract is materially better/newer;
- **CONFLICT** — adopting one variant could change intentional project-specific behavior or authority.

Reconcile MISSING by adding it, EQUIVALENT by preserving it, and OUTDATED by upgrading it when project-specific intent and stricter constraints remain intact. Never resolve CONFLICT silently: show both behaviors, the practical consequence and the owner decision required.

## Universal vs project-specific

The target project should end with two coherent layers:

- **Universal workflow:** repository access, planning/research/audit behavior, owner boundary, Git handoff, parallel-work awareness, reporting and universal skill contracts.
- **Project-specific:** product/domain decisions, architecture, data rules, security/privacy, project quality gates, providers and deployment constraints.

Never remove legitimate project-specific rules because they are absent here. Never copy project-specific rules back into this standard.

## Repository access

Current repository evidence outranks old chat memory or historical planning text when repository state matters.

An empty/failed code search never proves that repository access is missing or a capability/file does not exist. Resolve the repository first. If code search is unavailable, unindexed or ambiguous, fall back automatically:

**repository → tree/contents → relevant paths → direct file reads**

Only report missing repository access after both repository resolution and direct content/file access fail.

For current-state/feature audits, inspect relevant specs, implementation, API/services, persistence/migrations, UI, tests and roadmap/task evidence before classifying capability status.

## Autonomous ChatGPT planning/research

For planning, research, audits and gap analysis, continue through obvious in-scope intermediate steps without ceremonial confirmation.

Do not stop merely to ask whether to inspect the repo, continue an audit, perform identified research, refine an in-scope plan or prepare an execution-ready order.

Stop when:
1. a genuine owner/product decision is required;
2. an unresolved architecture/product choice needs owner authority;
3. an external blocker prevents progress;
4. scope is complete; or
5. an execution-ready manual handoff is ready.

This grants no implicit implementation, merge, deployment or production authority.

## Normal planning endpoint

A planning/research chat normally returns control at one of two endpoints:

### Owner decision
Ask a real decision, with concise context, meaningful options and consequences. Do not manufacture confirmation questions.

### Execution-ready handoff
For substantial work, prefer a durable Git-tracked task/research/audit specification. Then provide only a short start prompt pointing the execution agent to it.

## Recommendation-only exception

A distinct **Handlungsempfehlung für den nächsten Chat / next-chat recommendation** is orientation, not execution authority. Do not automatically start that separate recommended follow-up.

The active task must still be completed to its own proper boundary first.

## Current-work overview

Immediately before every next-chat recommendation, show a compact evidence-based overview using only needed groups:

- **Läuft / Running**
- **Wartet / Waiting** — name the dependency
- **Relevant abgeschlossen / Relevant completed**
- **Status unklar / Status unclear**

Never guess task state. Exclude irrelevant history. Each entry is only name, type and short status/purpose.

Then recommend exactly one next planning/research/audit action or explicitly recommend no additional task. At most one similar alternative.

## Parallel work

Before proposing/preparing parallel work:

- identify active/waiting work;
- avoid duplicate scope and unnecessary component/file/contract overlap;
- identify dependencies;
- allow independent research/planning when non-interfering;
- recommend waiting when all useful parallel work is already in flight.

Parallel task count is not a goal.

Where parallel implementation is used, the executing environment should independently verify technical safety against current repository state. Use isolated Git state according to project conventions. Integration is separate from implementation; green checks against an old base do not authorize integration after main changes.

## Durable Git work orders

Substantial orders should define as applicable:

- goal/non-goals;
- authority/exclusions;
- current-state inspection;
- acceptance criteria;
- data/provenance/unknown semantics;
- tests/validation;
- parallel dependencies/integration conditions;
- Git/commit/push authority;
- completion report;
- recommendation behavior.

Stricter project task formats win.

## Completion/handoff

Execution reports should be compact and, where applicable, include status, branch, commit, remote verification, result files, validation, blockers, integration/deployment state and required owner action.

Branch completion never implies integration/deployment.

## Skills

Use [skills/SKILL_MANIFEST.md](skills/SKILL_MANIFEST.md) as the capability contract.

Distinguish desired capability, Markdown skill description, actually installed/available skill and project-specific skill. Compare semantics, not names.

Preserve EQUIVALENT skills. Upgrade OUTDATED skills when safe. Ask on CONFLICT. Do not install optional skills merely to maximize skill count.

## Project-specific discovery

If sufficient project-specific instructions exist, preserve them and ask only unresolved decisions.

If absent/materially incomplete, use the available brainstorming capability and [templates/PROJECT_DISCOVERY.md](templates/PROJECT_DISCOVERY.md) as coverage guidance. Discover only needed project-specific goals, scope, authority, architecture, data, security/privacy, quality, deployment, provider and domain rules.

Persist those decisions in the target project, never in this universal standard.

## Authoritative instructions

Integrate universal behavior into the target project's existing authoritative instruction structure, normally an existing `AGENTS.md` or equivalent. Do not create competing instruction files unnecessarily.

The final instructions must preserve universal workflow + project-specific rules + stricter local constraints.

A project may record:

`Universal Project Bootstrap: v1.0.0`

The marker is evidence only; future upgrades still inspect actual semantics.

## ChatGPT validation

Before ChatGPT bootstrap is complete verify:

- repository resolved;
- authoritative instructions identified;
- universal rules reconciled without duplication;
- project-specific rules preserved;
- conflicts resolved or explicitly blocked;
- required capabilities/skills assessed;
- durable Git handoff behavior established;
- recommendation/current-work behavior established;
- no product logic changed merely for bootstrap.

Then generate the Codex prompt using [templates/CODEX_BOOTSTRAP_PROMPT.md](templates/CODEX_BOOTSTRAP_PROMPT.md).

## Codex bootstrap

Codex independently inventories repository-local instructions, skills, task protocols, Git rules, quality gates and completion contracts and uses the same four classifications.

ChatGPT must not claim Codex is configured merely because ChatGPT is configured.

Codex preserves project-specific/stricter constraints, reconciles universal execution capabilities, stops for genuine conflicts, validates the result, follows explicit Git authority and reports final state.

## Re-running/upgrades

Bootstrap is intentionally idempotent and may be re-run on older projects.

Always inspect semantics; never trust only a stored version.

An upgrade must not erase project-specific additions. An older universal behavior is OUTDATED when the new standard improves it without changing local intent; if the old behavior is an intentional local choice, it is CONFLICT.

## Public-standard hygiene

Never add secrets, credentials, personal data, private infrastructure details, product-specific business rules, private repo names as defaults or one-project provider/account identifiers. Examples stay generic.

## Bootstrap completion report

Report briefly:

- authoritative instructions inspected/changed;
- bootstrap version;
- EQUIVALENT areas;
- OUTDATED areas upgraded;
- MISSING areas added;
- CONFLICT areas/owner decisions;
- skills/capabilities reconciled;
- project-specific discovery performed or not needed;
- files changed;
- branch/commit where applicable;
- confirmation that bootstrap changed no product logic;
- generated Codex bootstrap prompt when ChatGPT side is complete.
