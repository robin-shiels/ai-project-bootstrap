# Changelog

## 2.1.0 — Guided personal setup — 2026-10-19

Compatible addition. No existing project rule, publication policy or gate stop condition changes.

- Added the guided personal setup in German ([`onboarding/`](onboarding/ENTRY.md)): shared dialog control (only the current step, check before asking, „Frage X von Y“ with options and a recommendation, short confirmation on success, concrete diagnosis only for actual problems, questions in the same chat with return to the same step), a step catalog with evidence types, and equal paths for ChatGPT/Codex and Claude/Claude Code on macOS, Windows (WSL 2) and Linux. Own computer by default; dev box optional.
- Added a versioned, secret-free setup state ([schema](onboarding/STATE.schema.json), [example](onboarding/STATE.example.json)) with an actual validator ([`scripts/onboarding_state.py`](scripts/onboarding_state.py)); saved before GitHub exists, re-read in a new chat with decisions kept and access/installations re-checked.
- Added the deterministic bundle build ([`scripts/build_bootstrap_bundle.py`](scripts/build_bootstrap_bundle.py)): `START_HIER.md`, `AI-Bootstrap-<version>.zip` with `BUNDLE_MANIFEST.json` (version, full source commit, file hashes) and `SHA256SUMS`, built from a Git commit without network access.
- Gate platforms ([policy §10](DEVBOX_GATE_POLICY.md#10-platforms)): native macOS through a small host adapter (memory from `vm_stat`/`sysctl`, processes from `ps`), with `systemd_scope = true` or watched user services stopping as `PRECONDITION` instead of being ignored; native Windows stops with `PRECONDITION` naming WSL 2, where the Linux reference runs unchanged. Linux behavior is unchanged. This changes the gate script, so adopting projects integrate it through a separately approved gate PR.
- Single version source [`VERSION`](VERSION); standard, policy, manifest and templates now name v2.1.0. The v2.0.1 entry below stays the gate hardening release; v2.0.0 remains the policy baseline.
- Mapped the manifest capabilities to verified candidate implementations for both providers and stated the Claude Code equivalence of the Codex roles.

### Migration from v2.0.x

Nothing to change in an adopted project. A project that copied the gate script may adopt the v2.1.0 script through its usual gate PR with owner approval; until then its v2.0.1 copy keeps working on Linux. Update the project's bootstrap marker only after confirming its rules still reconcile.

## 2.0.1 — Gate template hardening — 2026-10-19

Compatible fixes from the first real gate runs in adopting projects; the policy is unchanged.

- The resource check skips the gate process and **all** its ancestors (previously only itself and its parent). A shell that started the gate and merely mentions a heavy-check pattern such as `pytest` in its command line no longer blocks the run.
- The reference CLI and its tests satisfy the stricter default rule set of current Ruff (parenthesized implicit string concatenations, explicit `check=` in tests, executable script with shebang), so adopting projects can copy them byte-identically without lint exceptions.

## 2.0.0 — Dev-box merge gate — 2026-10-18

**Incompatible change.** Owner decision of 2026-10-18: GitHub-hosted CI starts in every project at most through deliberate `workflow_dispatch` for diagnosis, never automatically; the binding merge and release check is a deliberately started local gate; own explicitly mergeable task PRs may be merged automatically once a project's gate is integrated. Earlier versions required separate authority for every merge.

- Added [`DEVBOX_GATE_POLICY.md`](DEVBOX_GATE_POLICY.md): merge-tree gate (`B`+`H`=`M`, tree `T`) and separate exact-commit release gate, authorization model with narrowly named project exceptions, isolation of untrusted code, evidence/log rules, stop codes, compare-and-swap ref update via `updateRefs` (`beforeOid`, `afterOid`, `force=false`) without fallback, separate deployment contract, branch-rule and merge-queue handling, manual diagnosis workflow.
- Added the reference CLI [`templates/devbox_merge_gate.py`](templates/devbox_merge_gate.py) (`check-only --pr`, `check-only --main`, `merge-ff --confirm-own-task-pr`, `probe-ref-cas`, `validate-config`; no action without an explicit mode; never deploys) with a strictly validated TOML schema and a placeholder-only example.
- Added tests ([`tests/test_devbox_merge_gate.py`](tests/test_devbox_merge_gate.py)) against a temporary bare repository and fake GitHub/host: positive runs plus every stop case, including a stale base where a fast-forward push would still succeed, an ambiguous answer after the update, untrusted origin without isolation, excluded paths, gate self-merge, a missing/red/timed-out step and an unpublishable log.
- Added rule texts for `AGENTS.md`/`CLAUDE.md`, a rollout checklist and a dispatch-only diagnosis workflow example.
- Reconciled the standard, README, discovery template, Codex prompt and skill manifest: own-branch publication still excludes merge; merge authority is the separate gate contract, adopted by new projects only after their gate bootstrap and treated as CONFLICT where an existing project keeps a stricter rule.
- Adopted general points from the superseded cost-aware CI proposal where they still apply to a manual diagnosis workflow: least-privilege permissions, checkout without persisted credentials, pinned actions, no secrets for PR code, fail-closed documentation classification, skipped tests never reported as passed, timeouts as failures, matrix following the declared runtime contract, and checking rules on the actual plan instead of assuming protection. Its automatic `pull_request`/`push` workflow template is not adopted.

### Migration from v1.1.0

Inventory workflows, required checks/rulesets/merge queue, open PRs and merge rules. Adopt the gate in one scoped project task following the rollout checklist: configure the gate from inspected facts, move workflows to `workflow_dispatch` only, check the bootstrap PR on its actual merge tree and obtain a one-time Owner approval for it. Keep stricter merge, release and deployment rules as CONFLICT until the Owner changes them. Deployment is never granted by the migration.

## 1.1.0 — Six-audit consolidation — 2026-09-29

- Strengthened inventory with actual repository/default branch, revision-bound source classes, facts/inference/open/history separation and explicit maturity stages.
- Clarified autonomous progress within current authority and genuine Owner boundaries; generic skill gates neither revoke an explicit grant nor supply a missing one.
- Made substantial orders **and results** durable in a canonical store, normally Git-tracked; chat carries short launchers and closing handoffs.
- Adopted Owner decision B for **new projects**: own dedicated task-branch commit/push after relevant checks, prominently disclosed at setup with opt-out/per-task-approval choices and recorded effective policy.
- Preserved existing restrictive publication rules and stronger task prohibitions; separated branch publication from main, merge, release, deployment, production/provider activation and recommended follow-ups.
- Added task-appropriate verification, exact remote SHA equality, clean owned worktree and distinct LOCAL_COMPLETE / BLOCKED / DONE_ON_BRANCH / INTEGRATION_READY / INTEGRATED / DEPLOYED / PRODUCTION_VERIFIED meanings.
- Strengthened two-stage parallel assessment, integration cost, impact-based current-main revalidation and preservation of unrelated shared-document transitions.
- Aligned README, discovery, Codex prompt and capability manifest; verified runtime skill availability remains separate from documentation, optional skill authoring and automation profiles. No skills installed.

### Migration from v1.0.0

Inventory the target project's active rules first, then classify each capability MISSING / EQUIVALENT / OUTDATED / CONFLICT by behavior. Preserve product-specific intent and stricter constraints; improve evidence, durable results and completion where compatible. The version marker alone is not conformity or publication authority.

For an existing project, do not apply B retrospectively: preserve an explicit per-task approval or no-push rule, classify an incompatible proposed grant as CONFLICT and show its practical consequence before an Owner change. Preserve already equivalent own-branch authority without duplicate rules or repeated approval. If authority is absent/unclear, obtain an explicit scoped grant before commit/push. Evaluate existing commit and push restrictions separately.

For a new project, prominently show the B notice in onboarding and the ChatGPT setup response, offer ALLOW_AFTER_CHECKS / PER_TASK_APPROVAL / DISABLED, and record notice delivery and effective policy in authoritative instructions before relying on it. Default B requires no affirmative selection once disclosed; apply any opt-out before publication. A stronger task restriction still prevails.

Update the project's marker after actual reconciliation and list unresolved areas. This standard update does not re-bootstrap target projects, merge its task branch, tag/publish a release or deploy anything. Any later integration requires separate authority and current-main impact review/revalidation.

## 1.0.0 — Foundation

- Established inventory-first, idempotent bootstrap model.
- Added MISSING / EQUIVALENT / OUTDATED / CONFLICT reconciliation.
- Separated universal workflow from project-specific rules.
- Defined robust repository-access fallback.
- Defined autonomous planning to owner-decision or execution-ready handoff.
- Added recommendation-only exception and current-work overview.
- Added parallel-work and durable Git work-order contracts.
- Added ChatGPT/Codex separation and Codex bootstrap handoff.
- Added universal skill/capability manifest and project discovery template.
