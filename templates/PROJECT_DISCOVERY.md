# Project Discovery Coverage Template

**Bootstrap standard:** v3.0.0

Use this only when project-specific instructions are missing or materially incomplete. It is a coverage guide, not a questionnaire to ask mechanically.

Establish, as needed:

- project/product goal;
- intended users;
- scope and explicit non-goals;
- Product Owner / owner authority boundaries;
- authoritative repository/default branch, inspected revisions and source classes;
- canonical store for substantial orders and results (normally Git-tracked), plus short launcher/handoff conventions;
- technology and architecture constraints;
- domain invariants;
- data quality, provenance and unknown-value rules;
- privacy, security and compliance requirements;
- external providers and permissions;
- test and quality expectations;
- effective commit and push authority, including existing restrictions, opt-out/per-task choice and stronger task prohibitions;
- Git/branch/integration expectations and evidence required for each lifecycle stage;
- merge and deployment policy (LIGHT by default for new projects), deployment target and command, and whether production serves real user data;
- operational constraints;
- project-specific skills or workflows.

Before asking, inspect existing repository documentation and prior established project context. Ask only unresolved genuine decisions.

## Publication policy at setup

For a **new project**, prominently put this notice in the ChatGPT setup response before relying on default B; it must not appear only in the Codex prompt:

> Own task-branch commit/push is enabled by default. After an explicitly started task passes its required checks, the executor may commit and push only that task's dedicated branch. This excludes main/default-branch push, another task's branch, merge, release/tag, deployment and production/provider activation, and does not start a recommended follow-up. You can opt out of commit/push or require approval per task. We will record the effective policy in your authoritative project instructions; stricter project/task rules prevail.

Offer **ALLOW_AFTER_CHECKS** (default B), **PER_TASK_APPROVAL**, and **DISABLED** (opt out of commit/push). B is active after notice for a new project without requiring affirmative selection; apply any Owner change before the affected action. Record:

- new or existing project classification and authoritative instruction path;
- effective commit/push policy, source/scope and restrictions;
- new-project notice delivery (date/setup response) and explicit Owner choice if given, otherwise the disclosed default;
- dedicated-branch convention and checks required before publication;
- separate integration/release/deployment authority and genuine unresolved decisions.

For an **existing project**, inspect and preserve effective authority first. A proposed grant incompatible with a restrictive rule is **CONFLICT**: explain, for example, “Existing rule requires per-task push approval; proposed B permits own-branch push after checks. Keep the existing restriction unless the Owner explicitly changes it.” Already equivalent permission stays **EQUIVALENT** without duplicate rules or repetitive approval. Missing/unclear authority is not retroactive consent; obtain a scoped grant before publication. Preserve separate commit/push restrictions if the project distinguishes them.

Keep the effective choice in the existing authoritative instructions rather than a competing file. With opt-out/per-task approval, the executor stops before any unapproved commit/push and reports LOCAL_COMPLETE or BLOCKED with actual local evidence. A branch DONE handoff requires exact remote SHA verification and a clean owned worktree; it does not establish integration/deployment.

## Merge and deployment policy at setup

For a **new project**, deliver the standard's LIGHT notice ([merge and deployment policy](../UNIVERSAL_PROJECT_BOOTSTRAP.md#merge-and-deployment-policy)) and offer **LIGHT** (default), **GATE** and **PER_CHANGE_APPROVAL**. Record the effective choice, the deployment target and command if one exists, and ask once whether a production deployment that serves real user data may run automatically. Without a deployment target, record "no deployment" and revisit it when one is added. For an **existing project**, preserve its effective merge and deployment rules; an incompatible LIGHT grant is CONFLICT.

## Merge gate at setup (GATE only)

Ask only what the repository does not answer: whether the project adopts the [dev-box merge gate](../DEVBOX_GATE_POLICY.md) now or later, its integration branch, the checks and runtime versions its gate must run, merge-excluded paths, which own branches count as task branches, whether an isolated environment for foreign code exists, and the separate deployment authority (none by default). Tell the Owner that hosted CI then runs only by manual dispatch and that own explicitly mergeable task PRs are merged automatically only after the gate's bootstrap PR is integrated.

Persist resulting decisions in the target project's authoritative project-specific instructions/specifications. Never add them to the universal bootstrap repository merely because one project needs them.
