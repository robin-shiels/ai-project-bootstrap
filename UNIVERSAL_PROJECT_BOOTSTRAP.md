# Universal Project Bootstrap Standard

**Version:** 1.1.0

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

Record the repository, default branch, inspected branch/revision, date and source class for material claims. Distinguish ChatGPT project instructions, authoritative repository rules, explicit owner decisions, inspected implementation/check evidence, runtime skill inventory and historical material. A repository file does not prove that native ChatGPT project instructions are configured; a planning audit's description of those instructions remains attributed evidence.

Keep facts, inference, open owner choices and historical/superseded material distinct. For maturity claims distinguish planned, branch-complete, integrated and deployed behavior; cite the revision and checks supporting the claimed stage. A matching filename, skill name or bootstrap version marker is not proof of equivalent behavior. Recent rules and correlated audits do not establish long-term success.

Current default-branch evidence is the baseline; also inspect any explicitly scoped task/feature branch. Historical documents can retain applicable constraints even when individual status/scope statements are superseded; do not promote or discard the entire document by title alone.

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

## Authority and Owner boundary

Applicable higher-priority platform/session instructions and the current scoped user authorization govern the work. Read authoritative local/project rules and the concrete task together; preserve stricter local constraints and task-specific prohibitions. This baseline fills workflow gaps; it does not silently weaken intentional restrictions. If applicable authority conflicts and cannot be resolved from current instructions, show the concrete consequence and ask the Owner.

Continue already-authorized work without asking again for discoverable facts, ordinary technical choices or natural intermediate steps. Material new product intent, scope, architecture, security, cost or provider choices belong to the Owner. A skill's generic stage or finishing prompt neither grants missing authority nor negates existing explicit authorization. A tool's capability, another branch's grant or historical approval is not current task authority.

Research/audit findings are evidence and planning inputs; their recommendations do not themselves authorize implementation. Planning, implementation, own-branch publication, integration, release and deployment are separate authority boundaries. Use an existing explicit grant within its exact scope; do not invent a grant for a later boundary.

## Own task-branch publication policy

**New projects bootstrapped to v1.1.0 use default B:** explicitly started tasks may commit and push only their dedicated task branch after the task's relevant verification. At setup, prominently deliver this notice in the ChatGPT setup response as well as the onboarding documentation, before relying on the default:

> Own task-branch commit/push is enabled by default for this new project. After an explicitly started task passes its required checks, the executor may commit and push only that task's dedicated branch. This does not authorize push to main/the default branch, another task's branch, merge, release/tag, deployment or production/provider activation, and does not start a recommended follow-up. You can opt out of commit/push or require explicit approval per task. Your effective choice will be recorded in the project's authoritative instructions; stricter project or task restrictions prevail.

Offer the concrete choices **ALLOW_AFTER_CHECKS** (default), **PER_TASK_APPROVAL**, or **DISABLED** for own task-branch commit/push. No affirmative selection is required to use B for a new project once the notice is delivered; an opt-out or per-task choice takes effect before publication. Record the effective policy, the notice delivery and any Owner choice in the target project's existing authoritative instruction structure. Ensure the Codex handoff carries that policy and its source. Do not hide the notice solely in an executor template or silently assume it was delivered.

**Existing projects:** inspect their active authority before reconciliation. Preserve an explicit restrictive commit/push rule until the Owner changes it. If the proposed upgrade would permit currently forbidden publication, classify it as **CONFLICT**, show the existing and proposed behaviors and ask about that concrete change; keep the restriction meanwhile. Existing own-branch permission that satisfies the contract is **EQUIVALENT** and needs no duplicate rule or repeated approval. If authority is absent or unclear, record the gap and obtain an explicit scoped grant before commit/push; silence is never retroactive consent from v1.1.0. Evaluate commit and push separately if the existing policy distinguishes them.

Every task rechecks its effective authority. A stronger task-specific prohibition wins over standing permission. With opt-out, stop before the prohibited commit/push, preserve the result locally and report actual evidence as LOCAL_COMPLETE or BLOCKED. Missing access or a failed push likewise cannot be reported as remote DONE. No policy authorizes mutation of another task's branch/worktree, main/default-branch push, integration, release or deployment merely because the task is complete.

## Autonomous ChatGPT planning/research

For planning, research, audits and gap analysis, continue through obvious in-scope intermediate steps without ceremonial confirmation.

Do not stop merely to ask whether to inspect the repo, continue an audit, perform identified research, refine an in-scope plan or prepare an execution-ready order.

Stop when:
1. a genuine owner/product decision is required;
2. an unresolved architecture/product choice needs owner authority;
3. an external blocker prevents progress;
4. scope is complete; or
5. an execution-ready manual handoff is ready.

Continuation stays within the authority above. The publication policy governs planning artifacts as well as implementation results when a repository task has explicitly started; it does not authorize product implementation from a planning-only task.

## Normal planning endpoint

A planning/research chat normally returns control at one of two endpoints:

### Owner decision
Ask a real decision, with concise context, meaningful options and consequences. Do not manufacture confirmation questions.

### Execution-ready handoff
For substantial work, persist the complete task/research/audit specification in the canonical store, normally a Git-tracked path in an ordinary Git project. Persist substantial results there too. An alternative durable, reviewable store requires explicit project selection. Chat supplies a short launcher pointing to the exact artifact and revision, or a compact closing handoff; it is not the sole carrier of substantial orders or results.

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

A task file, branch or worktree's existence alone does not prove live activity; use fresh canonical status evidence or report uncertainty.

Then recommend exactly one next planning/research/audit action or explicitly recommend no additional task. At most one similar alternative.

## Parallel work

Before proposing/preparing parallel work:

- identify active/waiting work;
- avoid duplicate scope and unnecessary component/file/contract overlap;
- identify dependencies;
- allow independent research/planning when non-interfering;
- recommend waiting when all useful parallel work is already in flight.

Parallel task count is not a goal.

Planning establishes only a parallel candidate. Before execution, independently inspect actual code, dependencies, contracts, migrations, in-flight work and shared resources against current repository state. Consider reconciliation/integration cost as well as technical independence; sequence work when concurrency is unlikely to save useful effort. Use isolated state according to project conventions and preserve other tasks' branches/worktrees.

When updating shared status or documentation, read current canonical content, apply only the owned change and preserve unrelated transitions. Do not overwrite it with a stale whole-file branch copy. Integration is separate from implementation and follows the revalidation contract below. Factory scheduling, READY, claims, slots, CAS, retries and recovery are outside this manual baseline; an optional automation profile needs separate design and authority.

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

Substantial results belong in the same durable canonical workflow: include evidence/provenance, limitations, findings or decisions, validation and blockers as applicable. Scope and task type determine the result; an audit does not manufacture an implementation follow-up. Do not add speculative future infrastructure outside the active order.

## Execution and verification

Read the current order and applicable instructions, inspect the actual base/worktree and keep changes within authorized scope. Choose checks by task type and risk:

- Reports/documentation: content, source, link, format, scope and privacy review; no invented product tests for an audit-only result.
- Behavior changes: meaningful relevant tests and the project's applicable quality gates; investigate failures and verify the actual behavior.
- Shared contracts, migrations or uncertain effects: broader affected validation rather than a convenient narrow check.

Record actual commands, exit statuses and material failures. Inspect what an alias/script really runs before calling it a complete gate. A narrow green test proves only its covered behavior. Review the final diff for unrelated changes, credentials, private data, generated/runtime material and documentation drift. Do not claim checks that were unavailable or never run.

## Completion and lifecycle

A remotely completed repository task requires, where authorized/applicable: complete durable result, required passing checks, reviewed scope/diff, a scoped commit on its own dedicated branch, push of that exact branch, exact local/remote HEAD SHA equality and a clean owned worktree. Without publication evidence, report the achieved intermediate state and missing authority/access, rather than remote DONE.

| State | Meaning / evidence |
| --- | --- |
| LOCAL_COMPLETE | In-scope local result and relevant checks complete; branch publication has not completed. State whether commit exists and why push/commit is prohibited or unavailable. |
| BLOCKED | A required part of the scope/checks or authorized action cannot proceed. Name actual failure, missing authority/decision/access and the preserved result. |
| DONE_ON_BRANCH | Durable verified result committed and pushed on its own branch, exact remote SHA verified, owned worktree clean. |
| INTEGRATION_READY | Branch completion plus current-target compatibility and impacted checks established; integration itself still needs scoped authority. |
| INTEGRATED | Result is actually present on the authoritative integration branch; cite its revision. |
| DEPLOYED / PRODUCTION_VERIFIED | Deployment and any claimed production verification actually occurred with evidence under separate authority; deployed alone does not prove production behavior. |

Target-project labels may differ; keep these meanings separate. Branch DONE does not imply integration readiness, integration or deployment.

Before any separately authorized integration, inspect current main/default branch since the task base for textual and semantic overlap. Reconcile affected work and rerun impacted gates. Focused checks suffice for clearly bounded changes; shared contracts, migrations or uncertain impact require broader validation. Protect shared status/docs by preserving unrelated canonical updates. Old green checks are not current integration proof, and current-main compatibility does not itself authorize a merge.

## Compact handoff

Execution reports should include, where applicable, STATUS, BASE_COMMIT, BRANCH, COMMIT, REMOTE_COMMIT_VERIFIED (exact remote SHA and equality), RESULT_FILES, VALIDATION (commands/results), BLOCKERS, INTEGRATION_STATE and any required Owner decision. State clean-worktree evidence and any publication restriction in the durable result or handoff. Keep substantial findings in the canonical artifact.

Branch completion never implies integration/deployment.

## Skills

Use [skills/SKILL_MANIFEST.md](skills/SKILL_MANIFEST.md) as the capability contract.

Distinguish desired capability, Markdown skill description, actually installed/available skill and project-specific skill. Compare semantics, not names. Check relevant triggers, version/reference where discoverable and actual behavior in the runtime that will execute the task. A skill available locally is not necessarily present in CI or another worker. Use an available capability fallback and report gaps rather than claiming automatic installation.

Preserve EQUIVALENT skills. Upgrade OUTDATED skills when safe. Ask on CONFLICT. Do not install optional skills merely to maximize skill count.

## Project-specific discovery

If sufficient project-specific instructions exist, preserve them and ask only unresolved decisions.

If absent/materially incomplete, use the available brainstorming capability and [templates/PROJECT_DISCOVERY.md](templates/PROJECT_DISCOVERY.md) as coverage guidance. Discover only needed project-specific goals, scope, authority, architecture, data, security/privacy, quality, deployment, provider and domain rules.

Persist those decisions in the target project, never in this universal standard.

## Authoritative instructions

Integrate universal behavior into the target project's existing authoritative instruction structure, normally an existing `AGENTS.md` or equivalent. Do not create competing instruction files unnecessarily.

The final instructions must preserve universal workflow + project-specific rules + stricter local constraints.

A project may record:

`Universal Project Bootstrap: v1.1.0`

The marker is evidence only; future upgrades still inspect actual semantics.

## ChatGPT validation

Before ChatGPT bootstrap is complete verify:

- repository resolved;
- authoritative instructions identified;
- universal rules reconciled without duplication;
- project-specific rules preserved;
- source classes/revisions and fact/inference/open/history distinctions recorded;
- new-project default B notice prominently delivered with opt-out/per-task choices and effective policy recorded, or existing authority preserved with gaps/conflicts explicit;
- conflicts resolved or explicitly blocked;
- required capabilities/skills assessed;
- durable order/result and short handoff behavior established;
- recommendation/current-work behavior established;
- no product logic changed merely for bootstrap.

Then generate the Codex prompt using [templates/CODEX_BOOTSTRAP_PROMPT.md](templates/CODEX_BOOTSTRAP_PROMPT.md).

## Codex bootstrap

Codex independently inventories repository-local instructions, skills, task protocols, Git rules, quality gates and completion contracts and uses the same four classifications.

ChatGPT must not claim Codex is configured merely because ChatGPT is configured.

Codex preserves project-specific/stricter constraints, reconciles universal execution capabilities, stops for genuine conflicts, validates the result, follows the recorded effective Git authority and reports the actual lifecycle state with evidence. It must verify the policy's source and setup notice rather than infer permission from a template or version marker.

## Re-running/upgrades

Bootstrap is intentionally idempotent and may be re-run on older projects.

Always inspect semantics; never trust only a stored version.

An upgrade must not erase project-specific additions. An older universal behavior is OUTDATED when the new standard improves it without changing local intent; if the old behavior is an intentional local choice, it is CONFLICT.

For v1.0.0 → v1.1.0, inventory each capability, strengthen evidence/results/lifecycle where intent is preserved, and retain existing publication authority. Do not apply new-project default B retrospectively. Show a restrictive-policy conflict before proposing an Owner change and leave the active restriction effective until that change is explicit. Update the version marker only to describe the actual reconciliation; unresolved areas remain listed, not hidden behind the marker.

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
- effective commit/push policy, prominent notice delivery for new projects, opt-out/per-task choice and existing restrictions preserved;
- skills/capabilities reconciled;
- project-specific discovery performed or not needed;
- files changed;
- base/branch/commit/remote equality and actual lifecycle state where applicable;
- confirmation that bootstrap changed no product logic;
- generated Codex bootstrap prompt when ChatGPT side is complete.
