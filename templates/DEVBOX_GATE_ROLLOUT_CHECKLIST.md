# Dev-box merge gate rollout checklist

Copy into a project task and fill in real values. Keep private host details,
account data and production facts in the project, not in this public
template. Contract: [`DEVBOX_GATE_POLICY.md`](../DEVBOX_GATE_POLICY.md).

## 1. Inventory (read only)

- [ ] Repository, default/integration branch and full current SHA recorded.
- [ ] Authoritative instructions (`AGENTS.md`, `CLAUDE.md`, other rule files)
      read; existing merge, push, release and deployment rules quoted.
- [ ] Open PRs with base, head SHA, draft state, author, fork flag and
      dependency graph recorded; overlapping work identified.
- [ ] Every workflow file with its `on:` triggers, runner type and secrets use
      recorded; recent runs classified (executed steps vs. failed before the
      first step).
- [ ] Required checks, rulesets, branch protection and merge queue checked on
      the actual plan; unavailable API answers recorded as unknown.
- [ ] Conflicts with this policy listed as CONFLICT for the owner.

## 2. Local tooling and project checks

- [ ] Project's declared runtime versions available on the dev box (each
      supported version of a declared matrix, or a documented stop).
- [ ] Every check of the project's documented quality gates translated into
      argument lists with evidence-based timeouts; nothing silently dropped.
- [ ] Test data synthetic; services the checks need (databases, browsers)
      are disposable, per run, on non-colliding ports/names; no shared or
      production service.
- [ ] Resource preconditions and limits chosen so running services on the
      dev box are not displaced.
- [ ] Application bootstrap state handled with `application.markers` if the
      integration branch does not yet contain the application.

## 3. Configuration

- [ ] Config copied from the example; every placeholder replaced;
      `validate-config` passes.
- [ ] Trusted accounts, check/merge branch patterns, never-merge branches and
      named project exceptions (exact PR and branch, documented decision).
- [ ] Documentation-only, force-full and merge-excluded patterns reviewed:
      quality, gate, CI, security and operations documents, `.github/`,
      migrations, deployment and service files are never docs-only.
- [ ] State directory (lock, logs, worktrees) and temporary ref namespace are
      project-specific and not shared with another gate.

## 4. Isolation

- [ ] Whether the gate UID has project, deploy or provider access recorded.
- [ ] `untrusted_code = "refuse"` unless a separately provisioned isolated
      environment exists and is verified by its own instance.
- [ ] Ref-update permission held only by the orchestrating gate process.

## 5. Hosted CI

- [ ] Every workflow has only `workflow_dispatch` or is removed; no
      self-hosted runner; read-only permissions; no secrets; pinned actions.
- [ ] Documentation states that a diagnosis run is no merge or release
      condition and that a red executed run is a stop signal.

## 6. Bootstrap PR

- [ ] Own branch from current integration branch; planning file carried over.
- [ ] Gate tests (temporary bare repository, fake GitHub/host) pass locally.
- [ ] `check-only --pr <N>` run on the bootstrap PR's actual merge tree; B, H,
      M, T, steps and log checksum recorded in the PR.
- [ ] PR body says the PR must not be merged by the gate; owner asked for the
      one-time bootstrap approval with the exact B/H/T.
- [ ] Superseded PRs closed with a reason only after the successor PR exists.

## 7. After the owner integrated the bootstrap PR

- [ ] Integration branch SHA and the gate files on it verified.
- [ ] Optional `probe-ref-cas` on a temporary ref, only if access allows.
- [ ] First later own task PR integrated through `merge-ff`; remote SHA, tree
      and PR state verified.
- [ ] Deployment still unauthorized unless the project decides separately.
