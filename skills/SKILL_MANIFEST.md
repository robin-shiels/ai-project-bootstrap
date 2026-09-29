# Universal Skill & Capability Manifest

**Bootstrap standard:** v1.1.0

This manifest defines reusable capabilities, not assumptions that a named skill is installed. A Markdown file is not automatically an active skill. Bootstrap compares actual behavior and availability.

For each capability, record its trigger, available implementation/fallback, version/reference where discoverable, environment and evidence of actual behavior. Skill names are hints; a catalog entry, local file, active registration and historical use are distinct observations. Availability in one chat does not prove availability in Codex, CI or another worker. The manifest installs nothing.

## Authority for every capability

Applicable higher-priority platform/session instructions and current scoped authorization govern use; preserve authoritative local rules and stronger task restrictions. Generic skill stage or finish prompts neither revoke an explicit grant nor create missing authority. New material product/scope/security/cost/provider/architecture intent belongs to the Owner; ordinary authorized mechanics and discoverable facts do not require repetitive approval. A historical grant, another branch or a tool's capability supplies no authority.

For new v1.1.0 projects, use the [standard's publication policy](../UNIVERSAL_PROJECT_BOOTSTRAP.md#own-task-branch-publication-policy) only after prominent setup notice, opt-out/per-task choices and recorded effective policy. Preserve existing restrictive authority; a proposed incompatible grant is CONFLICT, not an automatic upgrade. Every capability operates within that policy and the current task, never implicit main/merge/release/deployment authority.

## ChatGPT-side capabilities

### Brainstorming / structured discovery — required when decisions are missing
- inspect existing context first;
- ask only questions that resolve genuine project/product choices;
- surface trade-offs and overlooked decisions;
- do not re-ask established decisions;
- distinguish owner choices from technical decisions;
- converge toward a sufficiently specified outcome.
For project bootstrap, discovery creates project-specific rules without adding them to the universal standard.

### Planning / executable work orders — required
- inspect current repository state;
- continue autonomously through non-decision intermediate steps;
- identify genuine owner decisions;
- store substantial orders and results in a canonical durable store, normally Git-tracked in Git projects;
- define scope, non-goals, acceptance, validation, authority and handoff;
- return a short execution start prompt after the durable order exists.

### Research / audit — required capability
- bind evidence to repository/default branch, relevant revisions/date and source classes;
- separate facts, inference, open Owner choices and historical material;
- inspect repository and external sources when relevant;
- state uncertainty;
- persist substantial reports;
- distinguish planned/branch-complete/integrated/deployed maturity; retain evidence limits rather than claiming long-term success from recent correlated audits;
- convert findings into planning inputs without automatically executing recommendation-only follow-ups.

### Skill authoring / maintenance — optional until needed
When reusable custom skills are created, keep them product-neutral unless explicitly project-specific. Version and reconcile them semantically.

This optional profile is separate from bootstrap inventory and requires its own authorized need; do not create or install a skill merely because a capability is described here.

## Codex-side capabilities

### Repository instruction discovery — required
Read applicable repository instructions before changes and respect nested/local instructions where the environment supports them. Resolve actual repository/default branch, task/base/working state and effective authority; use direct tree/file fallback when search is unindexed or empty. Preserve other tasks' work.

### Implementation planning — required for substantial work
Translate the durable order into an execution plan without reopening settled product decisions.

### Systematic debugging — required when diagnosing failures
Reproduce, isolate, identify root cause, add regression evidence, fix the root cause and revalidate.

### Testing / verification — required
Use task/risk-based checks appropriate to the repository. Reports need content/source/link/format/scope/privacy review; behavior changes need relevant meaningful tests and applicable gates; shared contracts/migrations/uncertainty need broader affected validation. Inspect actual commands/alias contents and exit statuses. Never invent product tests for audit-only work or treat a narrow green check as proof of unrelated behavior. Review the final diff for scope, secrets, generated/runtime material and documentation drift.

### Git isolation / parallel execution — required when parallel work is used
Planning identifies only a candidate; execution rechecks actual code/contracts/dependencies/migrations, shared resources, in-flight work and reconciliation cost. Use dedicated branches/worktrees or the project's equivalent isolation; concurrency count is not a goal. Before separately authorized integration, review textual/semantic current-main changes since base and rerun affected checks, broadening for shared contracts or uncertainty. Update shared status/docs from current canonical content and preserve unrelated transitions.

### Completion reporting — required
Keep complete results and consequential decisions durable. For authorized/applicable remote branch completion, verify checks, owned scoped commit, exact branch push, local/remote HEAD SHA equality and clean owned worktree. With opt-out, missing permission or access/failure, report actual local/intermediate state and blocker rather than remote DONE.

Return compact STATUS, BASE_COMMIT, BRANCH, COMMIT, REMOTE_COMMIT_VERIFIED, RESULT_FILES, VALIDATION, BLOCKERS, INTEGRATION_STATE and Owner action where applicable. Preserve the [standard's lifecycle meanings](../UNIVERSAL_PROJECT_BOOTSTRAP.md#completion-and-lifecycle): LOCAL_COMPLETE, BLOCKED, DONE_ON_BRANCH, INTEGRATION_READY, INTEGRATED, DEPLOYED / PRODUCTION_VERIFIED. Completion does not grant a later stage or start a recommended follow-up.

### Skill authoring — optional until needed
Reusable Codex skills should be created only when they improve recurring execution and should be versioned/reconciled rather than duplicated.

## Reconciliation

For each capability classify:
- MISSING
- EQUIVALENT
- OUTDATED
- CONFLICT

Names do not determine equivalence. OUTDATED capabilities should be upgraded when project-specific intent is preserved. CONFLICT requires owner resolution.

Do not install optional capabilities merely to maximize skill count.

Automation scheduling, READY, claims, slots, CAS, retries/recovery and cross-task automatic continuation need a separate optional profile; they are not manual-project capability requirements. Authorized manual agent methods may be used without adopting a Factory runtime.
