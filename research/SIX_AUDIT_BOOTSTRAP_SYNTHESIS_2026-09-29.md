# Six-Audit Bootstrap Synthesis — Decision Dossier

**Date:** 2026-09-29  
**Status:** research and proposed design; no rule adopted  
**Bootstrap base:** `main@b0d7338a8547203dfbb81f38002b0267877750a5` (v1.0.0)  
**Scope:** compare three ChatGPT Planning and three Codex/Repository extraction audits, then propose a product-neutral manual-project standard. This document is not a bootstrap instruction, an implementation grant, or an automation profile.

## 1. Inventory of the public bootstrap

At the pinned base the complete tracked tree has eight files: `README.md`, `UNIVERSAL_PROJECT_BOOTSTRAP.md`, `CHANGELOG.md`, `LICENSE`, `skills/SKILL_MANIFEST.md`, `templates/CODEX_BOOTSTRAP_PROMPT.md`, `templates/PROJECT_DISCOVERY.md`, and `research/PROPERTY_PILOT_WORKFLOW_RULE_EXTRACTION_V1.md`. There is no repository `AGENTS.md`, runtime, tests, CI, or installed skill package in this tree. The Markdown manifest describes capabilities, not installed skills. The older Property Pilot report is a preliminary, one-project input; it does not replace the newer six-report comparison.

v1.0 already has inventory-first semantic reconciliation, source-of-truth retrieval fallback, a planning endpoint, durable work orders, short Codex prompts, work-status context before a recommendation, parallel-work awareness, authority separation, skill semantics, and idempotent upgrades. Its completion paragraph is less operational than the recent audits. This report changes none of those files or version markers.

## 2. Source register and provenance

Each link below identifies a report at an immutable commit. The three Planning reports describe ChatGPT project instructions, explicit project rules, observed workflows and skills, with repository evidence as a separate source class. The three Codex reports inspect repository branches, instructions, code/tests and execution contracts. They are complementary views of only **three projects**, not six independent deployments.

| ID | Project / layer | Pinned evidence | Reading limit |
| --- | --- | --- | --- |
| P-P | Property Pilot / ChatGPT Planning | [Planning extraction](https://github.com/robin-shiels/property-pilot/blob/be8383fc5c6002cbf60f67eb7f826a8a8e469bef/docs/research/CHATGPT_PLANNING_WORKFLOW_EXTRACTION_V1.md) | Project instructions and chat conventions are reported by that audit; Git alone cannot independently prove their persistence. |
| P-C | Property Pilot / Codex/Repo | [Repository extraction](https://github.com/robin-shiels/property-pilot/blob/5a1ca844d1d8f83a995c9a277c1a61fb78d88b98/docs/research/UNIVERSAL_WORKFLOW_RULE_EXTRACTION_V1.md) | Snapshot `9d34e3f6`, with intervening planning report checked; newly integrated rules have limited longitudinal evidence. |
| K-P | KI-Sekretär / ChatGPT Planning | [Planning extraction](https://github.com/robin-shiels/ki-sekretaer/blob/1b30d51a3e29a4710b2011761e2d90fae1e05ee6/docs/research/CHATGPT_PLANNING_WORKFLOW_EXTRACTION_V1.md) | Some native Project Instructions are not independently inspectable from Git. |
| K-C | KI-Sekretär / Codex/Repo | [Repository extraction](https://github.com/robin-shiels/ki-sekretaer/blob/9f86a74ed4577d26aac1587aab010ef128efee0a/docs/research/UNIVERSAL_WORKFLOW_RULE_EXTRACTION_V1.md) | Recent repository and rules; CI/task examples prove specific runs, not long-term workflow success. |
| F-P | Software Factory / ChatGPT Planning | [Planning extraction](https://github.com/robin-shiels/codex-software-factory/blob/ced0b9eeeeb13543783d73c79d5bc3b2d32fcbe2/docs/research/CHATGPT_PLANNING_WORKFLOW_EXTRACTION_V1.md) | Its planning convention must be separated from Factory runtime policy. |
| F-C | Software Factory / Codex/Repo | [Repository extraction](https://github.com/robin-shiels/codex-software-factory/blob/c6345cda9dfed4bd2679e8c1afa842d85a373914/docs/research/UNIVERSAL_WORKFLOW_RULE_EXTRACTION_V1.md) | Authored against a Phase-3 branch and separately pinned then-current main; published later by explicit owner authorization. A policy branch described there was not integrated into either inspected base. |

The source reports and their detailed private project data remain in the source repositories. This public comparison records only workflow abstractions, stable source pointers and necessary authority differences. A private URL is a traceability pointer, not a public copy or proof that an anonymous reader can access it.

**Evidence hierarchy for this synthesis:** current scoped user authority and applicable platform contracts; pinned authoritative repository rules and explicit project decisions; inspected implementation and revision-bound test/CI evidence for actual behavior; planning-audit descriptions of non-Git project instructions; historical documents and memory as leads only. A report's candidate label is not a newly adopted rule. Confidence reflects both independent corroboration across projects and the maturity limits above.

## 3. Cross-project comparison

| Capability | Planning evidence | Codex/Repo evidence | Disposition for a future standard |
| --- | --- | --- | --- |
| Current-state discovery and search fallback | P-P, K-P, F-P | P-C U01–U02; K-C R01–R04; F-C U01 | **Retain v1.0**, clarify that branch, revision and actual implementation/status are distinct. A failed search is not negative evidence. |
| Provenance and decision state | All three distinguish instructions, workflow, skills and history | P-C U18/U22; K-C R05–R07; F-C U01/U05/U07 | **Strengthen** source class, date/revision, confidence, decided/hypothesis/open semantics without imposing one project's status labels. |
| Autonomous progress and Owner boundary | All three continue within active scope to a real decision, blocker, completion or executable handoff | P-C U03–U05; K-C R10/R11/R59; F-C U02–U04 | **Retain and clarify** existing authorization is used; a skill's generic routine gate cannot invent a new product decision or grant. Material new WHAT/security/cost/scope still returns to Owner. |
| Research/audit lifecycle | All three treat findings as evidence and follow-up as separate | P-C U11/U22; K-C R08/R12/R23; F-C U06/P04 | **Strengthen** durable result and task-appropriate completion; do not convert an audit into implementation authority. |
| Git specification and short launcher | All three describe substantial orders in Git and short manual Codex starts | P-C U11; K-C R08/R15; F-C P04/P06 | **Retain with a store parameter**. For a Git project, a versioned, reviewable repository path is normal; alternative canonical stores require explicit selection. |
| Task completion | All three demand evidence rather than self-reported DONE | P-C U12–U14; K-C R23/R24; F-C U06/U11/P14 | **Strengthen**, with distinct result, checks, diff/scope, local commit, remote publication and clean tree when authorized and applicable. A blocked intermediate result must be named honestly. |
| Commit/push authority | P-P/K-P report standing authority for own task branch; F-P does not establish it as universal | P-C and K-C have standing own-branch authority; F-C local branch required explicit grant, while another policy branch proposed standing authority | **Owner decision required** on default; preserve stricter project/session instructions and never infer permission from another branch or skill. |
| Integration and deployment | All three separate these from a planning or task result | P-C U12/U16; K-C R37–R39; F-C U09–U12/P13 | **Retain and strengthen** branch DONE, integration eligibility, integrated main and deployed/verified as different facts. Integration authorization may already exist in an exact task; do not ask for it again or infer it when absent. |
| Parallel work | All three reject artificial concurrency and stale status guesses | P-C U15–U17 with cost/impact; K-C R19/R20 and resource collision; F-C U08–U10 | **Conditional software-project guidance**: planning candidate, independent technical preflight, isolated state, reconciliation cost, main-movement impact and shared-document lost-update protection. Exact labels/resources are parameters. |
| Skill use | All three distinguish available skill from workflow mention | P-C/K-C/F-C inventory runtime availability and conflicts | **Retain**, verify trigger/version/actual environment; repository docs do not install skills. Skill methods are subordinate to current user/task/platform authority. |
| Next-work recommendation | All three use current work plus recommendation-only follow-up | P-C/K-C reinforce task boundary; F-C distinguishes derived status from canonical state | **Retain v1.0**; status needs fresh evidence, a recommendation does not start the next task. Exact wording/count may be configured. |
| Automation | All three exclude queue/worker rules from manual planning | P-C historical Factory, K-C product queues distinct, F-C runtime-specific READY/claims/CAS/recovery | **Keep outside manual baseline**. An optional profile needs separate design and authorization; no silent inclusion. |

## 4. Recommended product-neutral design, pending adoption

The best-supported shape is a **small manual-project core plus conditional execution modules**. It should be phrased as observable outcomes, not fixed tool commands or mandatory installed plugins.

1. **Evidence and authority envelope.** Resolve the project's current authoritative sources, their revision and scope. Record facts, inferences, open decisions and historically superseded instructions separately. A version marker or a file title is not behavioral equivalence. Do not make a prior approval or API permission portable to a new task or branch.
2. **Planning and research.** Continue the authorized task through natural read-only discovery, synthesis and drafting. Escalate only a material unresolved Owner decision, conflicting authority, external blocker or action beyond the existing grant. For substantial work, persist both the complete order and substantial audit/research result; a concise chat message points to the canonical artifact. Recommendation-only follow-up remains a new task boundary.
3. **Execution and verification.** Read applicable instructions and exact task, use isolated state when appropriate, keep scope narrow, investigate failures and verify relevant behavior. Choose gates by change type and risk: document review for a report; meaningful tests and quality checks for behavior changes; expanded checks where shared contracts or migrations are affected. Do not call a convenience command a full quality gate without verifying its contents. Preserve out-of-scope findings without opportunistic fixes.
4. **Publication and lifecycle.** Record base, branch, result paths, actual checks and failures, commit, remote equality, clean owned workspace and blockers, insofar as authorized and relevant. Distinguish local result, remotely published branch, integration-ready, integrated main and deployed/production-verified. Recheck current main and affected validation before an authorized integration; no blanket rerun merely because unrelated main files changed.
5. **Parallel coordination.** The planner checks dependencies, semantics and probable integration cost; the executor rechecks technical overlap and shared resources against current state. Shared status/docs are updated from current canonical content while preserving other tasks' changes. Concurrency count is never a goal.
6. **Skill/capability portability.** Specify needed behavior and trigger, verify availability in the environment that will execute it, and choose a supported fallback. Formal skill names, templates and agents are implementation choices. Do not require a Factory, scheduler, SDK, webhook, cryptographic journal, fixed model, or provider for ordinary projects.

This design would extend v1.0 in a later **new version**, following its semantic reconciliation rules. It is not an instruction to run bootstrap now. Keep public examples generic; per-project configuration owns repository identity, task paths, branch conventions, test commands, privacy/security constraints and integration/deployment policy.

## 5. Conflicts and decisions

**D1 — default own-branch commit/push policy (Owner decision: B, 2026-09-29).** For **new** manual projects, the proposed bootstrap default permits the executing agent to commit and push only the task's dedicated branch after the task's applicable checks. Bootstrap must **explicitly inform the owner at setup** that this default is active, explain its precise boundary, and provide a clear way to opt out or choose per-task authorization. The choice is recorded in the target project's authoritative instructions. Silence must never conceal the default.

For **existing** projects, inventory the effective rules first. A stricter existing commit/push restriction or task-specific prohibition remains in force unless the owner explicitly changes it; a rule on another branch or another project supplies no grant. The default does not grant push to `main`, merge, deployment, provider activation, mutation of other task branches, or any unrelated follow-up. If publication is disallowed or technically blocked, report the actual local/intermediate status instead of claiming remote DONE.

The compared alternatives were A (explicit selection before any default grant) and C (approval per task). The owner selected B after confirming that B differs from A in its starting state: B permits own-branch publication by default for a new project, with a prominent notice and opt-out.
Other differences can be resolved within the design without a new product choice: already granted authority outranks a generic skill's routine review prompt; genuinely new product intent still needs the owner. Review frequency, test commands, branch prefix, storage path and parallel labels remain project parameters. An optional automation profile should be a later independent proposal, not a condition for the manual standard.

## 6. Exclusions and evidence limits

Do not import financial/domain rules, product workflows, private operational details, provider/credential bindings, exact CI commands, model routing, Factory READY/claim/slot/CAS/recovery machinery, old Phase-3 approval, or task-status numbers. Do not conflate a product's own background queue with an engineering Factory. Formal skills were observed in particular sessions; their availability in a future ChatGPT chat, CI job or Codex worker is unproven. Recently written completion policies are clear but have limited duration of use. The six audits are correlated by shared owner and recent rule propagation; agreement alone is not a statistically independent validation.

## 7. Next executable boundary

With D1 decided, prepare a separate versioned implementation order to update `UNIVERSAL_PROJECT_BOOTSTRAP.md`, `skills/SKILL_MANIFEST.md`, both templates, `README.md`, and `CHANGELOG.md` consistently. The order should specify a version choice, exact semantic changes, migration/re-bootstrap behavior, conflict examples, a minimal acceptance matrix for a new project and an existing restrictive project, link/format/scope verification, and independent review. This decision and report do **not** authorize that implementation, a merge, or publication of a new bootstrap version.

**Research completion check:** six report paths pinned; three planning and three repository viewpoints compared; current v1.0 inventoried; material conflicts isolated; no rule, skill, template or version modified.
