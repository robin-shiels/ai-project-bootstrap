# Bootstrap v1.1.0 — Six-Audit Consolidation Implementation Order

**Status:** execution-ready order; not started  
**Prepared:** 2026-09-29  
**Repository:** `robin-shiels/ai-project-bootstrap`  
**Planning base:** `main@b0d7338a8547203dfbb81f38002b0267877750a5`  
**Decision source:** [Six-Audit Synthesis](../research/SIX_AUDIT_BOOTSTRAP_SYNTHESIS_2026-09-29.md), especially §5 D1 (Owner chose B, with prominent notice).  
**Target:** next standard version `1.1.0`, not an in-place silent reinterpretation of v1.0.0.

## Objective

Consolidate the six pinned extraction audits into a clear, product-neutral manual-project bootstrap. Preserve the working v1.0 foundation, strengthen evidence, task completion, authority, parallel execution and upgrade semantics, and implement the Owner's visible own-branch commit/push default for new projects. Do not copy one project's product or Factory runtime mechanics into the manual baseline.

This order is a **future execution task**. Merely reading it grants no implementation, merge or deployment authority. On explicit start, it authorizes the documentation changes below and publication on the task's own branch after the specified checks. It does not authorize main push, merge, release tag, target-project re-bootstrap, skill installation or deployment.

## Inspect first

1. Verify the current default branch, exact HEAD, working state, and applicable repository instructions. Read every tracked bootstrap file. The planning base above is evidence, not permission to ignore a newer main.
2. Read the linked synthesis and its six pinned reports. Treat ChatGPT-side project rules, repository rules, installed skills, and historical behavior as distinct source classes. Check whether any later owner decision or bootstrap change supersedes this order.
3. If main moved, compare the intervening diff semantically and adapt this order within the settled design. Stop only for a genuine conflict requiring Owner authority. Work on a dedicated task branch; preserve any other branches.

## Files and responsibilities

- `UNIVERSAL_PROJECT_BOOTSTRAP.md`: normative v1.1.0 contract and reconciliation behavior.
- `skills/SKILL_MANIFEST.md`: capability triggers, actual availability and authority precedence; no claim of automatic skill installation.
- `templates/CODEX_BOOTSTRAP_PROMPT.md`: executor inventory, conditional own-branch publication, verification and lifecycle handoff.
- `templates/PROJECT_DISCOVERY.md`: capture project-specific authority and opt-out, with existing-rule preservation.
- `README.md`: concise onboarding and prominent notice of the new-project publication default.
- `CHANGELOG.md`: v1.1.0 changes and migration from v1.0.0.
- Add at most one focused generic example or acceptance checklist under `templates/` if needed to show the notice/opt-out and restrictive-project conflict. Prefer a concise section in an existing file if that is sufficient.

Do not rewrite the source research report or erase v1.0.0 history. Keep `LICENSE` untouched.

## Required semantics

### 1. Inventory and source truth

Keep inventory-first MISSING / EQUIVALENT / OUTDATED / CONFLICT semantic reconciliation. Resolve the actual repository/default branch; bind claims to revisions and source class. Search misses are not evidence of absent access or capability. For maturity claims distinguish planned, branch-complete, integrated and deployed. Record facts, inference, open owner choices and historical material separately. A version marker does not establish behavioral equivalence.

### 2. Planning and Owner boundary

Continue already-authorized planning, research, audit and specification work through natural intermediate steps until a real decision, external blocker, completed scope or execution-ready handoff. No repetitive approval question for a discoverable fact or ordinary technical choice. Material new product, scope, security, cost, provider or architecture intent belongs to the Owner. A skill's generic stage or finish prompt neither grants a missing authority nor negates an existing explicit authorization. Preserve applicable higher-priority instructions and local stricter constraints.

Substantial task orders **and results** belong in a durable canonical location; in ordinary Git projects this is a Git-tracked path. Chat provides a short launcher or compact closing handoff. Research/audit findings do not automatically authorize their recommendations. The current-work overview remains evidence-based and the next-chat recommendation remains recommendation-only.

### 3. Own-branch commit/push default: selected B with visible notice

For a **new project** bootstrapped to v1.1.0, the proposed default is authorization to commit and push the dedicated task branch after the task's relevant verification. At setup, **prominently tell the Owner** this is the default, name the exact boundary, and provide an explicit opt-out/per-task-approval choice. Record the effective policy in the target project's authoritative instructions. The notice must not be buried solely in an implementation template or omitted from the ChatGPT setup response.

For an **existing project**, inspect its active rules before reconciliation. Preserve an explicit restrictive commit/push rule until the Owner changes it; classify an incompatible proposed upgrade as CONFLICT and ask with the concrete consequence. Never treat silence on an existing project's branch as retroactive consent from v1.1.0. Never derive authority from a different branch, historical grant, skill instruction or tool capability.

Neither the default nor the notice authorizes push to `main`, merge, release/deployment, production activation, another task's branch, or a recommendation-only follow-up. A task-specific stronger restriction prevails. When branch publication is prohibited or unavailable, report `LOCAL_COMPLETE`/`BLOCKED` with actual evidence and the missing authorization; do not claim remote DONE.

### 4. Execution, evidence and lifecycle

Apply task/risk-appropriate checks: reports need content, source, link, format, scope and privacy review; behavior changes need relevant tests and quality gates. Verify actual commands and exit statuses; do not infer a complete gate from a convenient alias. Check the final diff for unrelated changes, credentials, generated/runtime material and documentation drift.

A remotely completed repository task has a durable result, required checks, scoped own-branch commit, branch push, exact remote SHA equality and clean owned worktree where those operations are authorized/applicable. Distinguish `LOCAL_COMPLETE`, `DONE_ON_BRANCH`, `INTEGRATION_READY`, `INTEGRATED`, and `DEPLOYED/PRODUCTION_VERIFIED` in meaning; exact target-project labels may differ. Missing later stages are reported without turning branch DONE into a merge.

Before any separately authorized integration, inspect current main since task base for textual and semantic overlap and rerun impacted gates. Focused checks suffice for clearly bounded changes; shared contracts, migrations or uncertain effects require broader checks. Protect shared status/docs by reconciling current canonical state and preserving unrelated transitions.

### 5. Parallel work and skills

Planning may identify an independent parallel candidate; execution independently rechecks actual code, dependencies, migrations, shared resources and integration cost. Use isolated state according to target-project conventions. No fixed concurrency target. Keep Factory scheduling, READY, claims, slots, CAS, retries and recovery out of the manual baseline.

Treat skill names as hints to capabilities. Check current runtime availability, relevant trigger and actual behavior. Mentioned documentation is not an installed skill; a local skill is not necessarily available in CI or another worker. Keep optional skill creation and automation profiles separate.

## Execution slices

1. **Normative contract:** update the main standard with §§1–5 above, making each new requirement observable and avoiding duplicate/contradictory authority statements. Preserve v1.0's existing useful behavior.
2. **Onboarding and templates:** align README, discovery and Codex prompt. Show the B notice and opt-out in the onboarding path; make existing-project restrictions and task-specific prohibitions explicit.
3. **Manifest and release notes:** align capabilities/skill language and document v1.1.0 migration. No skill installation.
4. **Review:** independently inspect the whole diff against this order, the synthesis and the six pinned sources. Remove accidental project-specific or automation-only requirements and reconcile wording across every entry point.

## Acceptance examples

Check the resulting documents against these scenarios and record the outcome in the task's durable result or commit description:

- New project, no established policy: Owner sees a clear notice that own task-branch commit/push is enabled and can select opt-out/per-task approval; effective choice is recorded.
- New project with opt-out: executor stops before commit/push and reports the actual intermediate state.
- Existing project explicitly forbids push without per-task permission: bootstrap flags CONFLICT and preserves the restriction; no silent rewrite.
- Existing project already permits own-branch push: preserve EQUIVALENT behavior, do not duplicate rules or re-ask for routine approval.
- Branch work is verified and published: report exact remote SHA and branch DONE; do not report integrated or deployed.
- Main changed since base: integration eligibility depends on affected revalidation and separate authority, not an old green check.
- Audit report only: durable evidence and document checks, no manufactured product tests or implementation follow-up.
- Unindexed code search or historical Factory approval: use direct repository reads; do not infer missing capability or current authority.

## Verification and completion

Verify Markdown structure/links and semantic consistency across all changed files; verify every six-report source pointer; inspect diff and scope; check public hygiene (no secrets, personal data, private infrastructure detail or product-specific defaults). No runtime test/build suite exists at the planning base, so do not invent one for documentation-only work. If newer main introduces checks, apply those relevant to documentation.

Commit and push only the task's dedicated branch on explicit execution of this order. Verify branch HEAD equals remote HEAD. Return a compact handoff with `STATUS`, `BASE_COMMIT`, `BRANCH`, `COMMIT`, `REMOTE_COMMIT_VERIFIED`, `RESULT_FILES`, `VALIDATION`, `BLOCKERS`, `INTEGRATION_STATE` and any genuine Owner decision. Do not merge, tag or publish a release. A later integration decision must consider main movement and the acceptance examples above.
