# Codex Bootstrap Prompt Template

**Bootstrap standard:** v1.1.0

ChatGPT generates a target-project-specific prompt after its own bootstrap is complete. Fill the setup context from inspected evidence; unresolved decisions stay explicit. The new-project default B notice must already be prominent in the ChatGPT setup response, with opt-out/per-task choices; this template alone does not deliver that notice or grant authority.

## Setup context to carry into the generated prompt

- Repository/default branch and inspected revision(s), standard source/reference.
- Authoritative instruction path and canonical order/result store, normally Git-tracked.
- New or existing project; effective commit and push policy and its authoritative source/scope.
- For a new project: delivered B notice/date and Owner choice, or disclosed ALLOW_AFTER_CHECKS default. Alternatives: PER_TASK_APPROVAL or DISABLED (opt out of commit/push).
- Existing restrictive rules, task-specific prohibitions, unresolved conflicts/authority gaps.
- Exact task artifact/reference and authorized scope, branch convention, relevant checks, integration/deployment boundaries.

Do not invent missing context or claim Codex is configured because ChatGPT is configured.

## Prompt

Bootstrap the Codex execution side of this project against the Universal Project Bootstrap Standard used by this project.

First perform an independent inventory. Resolve the actual repository/default branch, current HEAD and working state, and inspect current main plus any explicitly scoped branch. Do not blindly install or overwrite rules or skills. Preserve other tasks' branches/worktrees and existing unowned changes.

Read:
1. the target project's authoritative instructions;
2. its recorded Universal Project Bootstrap version/reference;
3. the universal bootstrap standard and skill manifest made available by the project/bootstrap source;
4. existing Codex rules, skills, task protocols, Git rules, quality gates and completion contracts.

Bind material findings to source class, revision/date and actual evidence. Keep facts, inference, open Owner choices and history separate. Distinguish planned, branch-complete, integrated and deployed claims. Empty/unindexed code search is not evidence of missing access/capability: resolve repository → tree/contents → relevant paths → direct reads before reporting absence/access failure.

For every universal Codex capability classify the existing state as:
- MISSING
- EQUIVALENT
- OUTDATED
- CONFLICT

Then reconcile:
- add MISSING capabilities;
- preserve EQUIVALENT capabilities without duplication;
- upgrade OUTDATED universal behavior when project-specific intent and stricter constraints remain intact;
- do not resolve CONFLICT silently: present the concrete conflict and required owner decision.

Preserve all legitimate project-specific product, architecture, security, quality, deployment and authority rules.

Apply higher-priority platform/session instructions and current scoped authorization. Continue ordinary authorized steps without ceremonial approval; return material new product/scope/security/cost/provider/architecture choices to the Owner. Generic skill stage/finish prompts neither negate an explicit grant nor supply missing authority. Historical approval, another branch's policy and tool capability are not authorization.

Check the effective publication policy independently against active instructions:

- New project with documented notice and ALLOW_AFTER_CHECKS: explicitly started tasks may commit/push their own dedicated branch after required verification; no repeated routine approval is needed.
- New project with DISABLED or PER_TASK_APPROVAL: stop before any prohibited/unapproved commit or push. Preserve the local result and report actual state and missing authority.
- Existing project with restrictive policy: preserve it until explicit Owner change. An incompatible proposed B grant is CONFLICT; show the existing/proposed behaviors and consequence rather than overwriting the restriction.
- Existing equivalent permission: preserve it without duplicate rules or repeated approval. Missing/unclear authority is a gap, not retroactive consent; obtain a scoped grant before publication. Respect separate commit/push restrictions where present.
- Any stronger task prohibition prevails. No policy above authorizes main/default-branch push, another task's branch/worktree, merge, release/tag, deployment, production/provider activation or recommendation-only follow-up.

Ensure at minimum that Codex has coherent contracts for:
- reading repository instructions;
- executing durable canonical work orders and persisting substantial results (normally Git-tracked);
- systematic implementation/debugging;
- task/risk-appropriate validation and actual command/exit-status evidence;
- Git isolation for parallel work when used;
- independent execution preflight for parallel candidates, including code/contracts/dependencies/migrations/shared resources and integration cost;
- current-main impact review/revalidation before separately authorized integration;
- shared status/document reconciliation from current canonical content, preserving unrelated transitions;
- compact completion/blocker reporting;
- distinct local, branch, integration and deployment states;
- no automatic execution of recommendation-only follow-up work.

Inspect actual skill availability, triggers, version/reference where discoverable and semantics in this runtime; a name or Markdown description alone is not an installed capability, and local availability does not prove CI/worker availability. Keep optional skill creation/installation and automation profiles separate; do not install skills merely to complete this inventory.

Do not modify product logic merely to bootstrap workflow.

Before claiming completion:

1. Persist complete results, evidence, limitations, decisions and blockers in the selected canonical store. Findings from an audit do not start implementation; chat is a compact pointer/handoff.
2. Run relevant checks and inspect their actual contents/output/exit statuses. Reports need content/source/link/format/scope/privacy review; behavior changes need meaningful tests and applicable gates. Broaden checks for shared contracts/migrations/uncertain effects. Do not invent product tests for documentation work or treat a convenience alias as a full gate.
3. Review the final diff for scope, unrelated changes, credentials/private data, generated/runtime artifacts and documentation drift.
4. Where authorized/applicable, stage only owned task files, commit on the dedicated task branch, push that exact branch, verify exact local HEAD = remote branch HEAD SHA, and verify a clean owned worktree. Do not claim remote DONE when prohibited publication or technical failure leaves a local/intermediate result.
5. Report LOCAL_COMPLETE (verified local result, publication incomplete), BLOCKED (required work/action blocked), or DONE_ON_BRANCH (verified published result). INTEGRATION_READY additionally requires current-target compatibility and affected validation; INTEGRATED needs actual integration evidence; DEPLOYED / PRODUCTION_VERIFIED need separate action/verification evidence and authority. Exact project labels may differ; meanings remain distinct.

Before any separately authorized integration, inspect current main since the task base for textual and semantic overlap, reconcile affected work and rerun impacted gates. Focused checks suffice for clearly bounded impact; shared contracts/migrations/uncertainty require broader validation. Old green checks and branch DONE do not grant integration authority. No fixed concurrency or Factory scheduling/claims/slots/CAS/retry/recovery requirements belong in this manual setup.

When reconciliation is complete, validate the setup and report:
- authoritative files inspected/changed;
- standard version and actual source/revision evidence;
- EQUIVALENT / OUTDATED / MISSING / CONFLICT areas;
- capabilities/skills reconciled and actual availability gaps;
- effective publication policy and notice/Owner choice or preserved existing restrictions;
- unresolved owner decisions;
- confirmation that no product logic changed.

Return a compact handoff with STATUS, BASE_COMMIT, BRANCH, COMMIT, REMOTE_COMMIT_VERIFIED (exact remote SHA/equality), RESULT_FILES, VALIDATION, BLOCKERS, INTEGRATION_STATE and any genuine Owner decision. Record missing publication authority/access and clean-worktree evidence. A version marker or this generated prompt cannot override the effective policy.
