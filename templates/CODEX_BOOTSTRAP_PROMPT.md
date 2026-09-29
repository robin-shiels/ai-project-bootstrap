# Codex Bootstrap Prompt Template

ChatGPT should generate a target-project-specific prompt following this contract after the ChatGPT-side bootstrap is complete.

## Prompt

Bootstrap the Codex execution side of this project against the Universal Project Bootstrap Standard used by this project.

First perform an inventory. Do not blindly install or overwrite rules or skills.

Read:
1. the target project's authoritative instructions;
2. its recorded Universal Project Bootstrap version/reference;
3. the universal bootstrap standard and skill manifest made available by the project/bootstrap source;
4. existing Codex rules, skills, task protocols, Git rules, quality gates and completion contracts.

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

Ensure at minimum that Codex has coherent contracts for:
- reading repository instructions;
- executing durable Git work orders;
- systematic implementation/debugging;
- risk-based validation;
- Git isolation for parallel work when used;
- current-main revalidation before integration;
- compact completion/blocker reporting;
- no implicit merge/deployment authority;
- no automatic execution of recommendation-only follow-up work.

Inspect actual skill semantics; a matching skill name alone is not equivalence.

Do not modify product logic merely to bootstrap workflow.

When reconciliation is complete, validate the setup and report:
- authoritative files inspected/changed;
- EQUIVALENT / OUTDATED / MISSING / CONFLICT areas;
- skills reconciled;
- unresolved owner decisions;
- branch and commit if changes were authorized and committed;
- confirmation that no product logic changed.

If repository rules require a dedicated branch/commit/push for instruction changes, follow them. Otherwise do not infer Git write authority.
