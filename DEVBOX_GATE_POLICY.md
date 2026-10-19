# Dev-box merge gate policy

**Standard:** Universal Project Bootstrap v2.0.0 · **Policy version:** 1

This is the binding, product-neutral contract for projects that adopt the
dev-box merge gate. The reference implementation is
[`templates/devbox_merge_gate.py`](templates/devbox_merge_gate.py) with the
strictly validated configuration schema in
[`templates/devbox_merge_gate.example.toml`](templates/devbox_merge_gate.example.toml).
Rule texts for project instructions are in
[`templates/AGENTS_DEVBOX_GATE.md`](templates/AGENTS_DEVBOX_GATE.md) and
[`templates/CLAUDE_DEVBOX_GATE.md`](templates/CLAUDE_DEVBOX_GATE.md); the rollout
steps are in
[`templates/DEVBOX_GATE_ROLLOUT_CHECKLIST.md`](templates/DEVBOX_GATE_ROLLOUT_CHECKLIST.md).

"Dev box" means the project's own deliberately operated development machine.
Nothing in this policy installs, registers or starts anything on it.

## 1. Decided rules

1. **Local gate is the binding merge and release check.** A PR is checked on
   its actual merge result: the gate builds the merge commit `M` with parents
   `B` (current integration ref) and `H` (exact PR head) in a fresh worktree,
   and runs every configured required step serially on `M` and its tree `T`.
   A release candidate is checked separately on exactly the current remote
   integration commit. A green PR run never replaces the release run.
2. **No automatic hosted CI.** GitHub-hosted workflows start at most through a
   deliberate `workflow_dispatch` for diagnosis, never on `push`,
   `pull_request`, `pull_request_target`, `merge_group`, `schedule`,
   `workflow_run` or any other automatic event. A diagnosis run is neither a
   merge nor a release condition. A red diagnosis run that executed steps is a
   stop signal for the change it diagnosed. A job that fails before its first
   step (for example blocked by billing or runner availability) is no test
   result, neither green nor red.
3. **Auto-merge of own task PRs.** After the gate contract is integrated on the
   integration branch, an own task PR that is explicitly marked mergeable and
   has no open decision may be integrated automatically by the gate after a
   complete green run. Stricter project rules, open owner questions,
   infrastructure/migration exclusions and branch rules take precedence.
4. **No automatic merge of anything else.** Foreign, unknown and fork PRs get
   no automatic merge authority. They are checked at most in a verifiably
   isolated environment and merged only after a separate owner decision.
5. **Deployment stays separate.** No project receives deployment authority
   from this policy, from a merge or from a green gate. A deployment needs its
   own project-specific authorization and its own gate run on the exact
   current integration commit.
6. **No self-authorization.** The first gate PR of a project (the bootstrap PR)
   and every later PR that changes the gate script or its configuration can
   never be merged by the gate. They need a concrete owner approval after a
   local gate run with the exact `B`/`H`/`T` evidence.

## 2. Authorization model

The gate distinguishes four authorities. None implies the next.

| Authority | Who decides | Scope |
| --- | --- | --- |
| Check own code (`check-only`) | operator starts it | own same-repository PRs whose branch matches the configured check patterns |
| Check untrusted code | owner provides an isolated environment | `check-only` only, inside that environment |
| Merge (`merge-ff`) | standing project rule + PR handoff | own task PR, explicit `MERGE_READY: yes`, `STATUS: DONE`, matching `COMMIT`, `BLOCKER: none`, no excluded path, contract on `B` |
| Release / deploy | separate project decision | never granted by this policy |

**Own task PR** means: same repository (no fork), author in the configured
trusted accounts, head branch matching the configured merge patterns, not
listed in `never_merge_heads`, not draft, and the operator repeats the PR
number with `--confirm-own-task-pr`.

**Project exception.** A project may name a specific existing own PR whose
branch does not match the merge patterns (for example an existing stacked
chain). Each exception names exactly one PR number, one exact branch name,
the author and the documented owner decision. It never acts as a wildcard,
never covers forks or other authors and never relaxes any other merge
condition. A wildcard-only branch pattern (`*`) is rejected by the schema.

**Handoff.** The PR body carries the last valid lines:

```text
STATUS: DONE
COMMIT: <head SHA, at least 7 hex characters>
BLOCKER: none
MERGE_READY: yes
```

The gate re-reads them immediately before the ref update; any change stops.

## 3. Gate contract

### 3.1 PR run (`check-only --pr N`, `merge-ff --pr N`)

1. Read PR metadata. Stop unless the PR is open, its base is the integration
   branch and its head is a full SHA; with `--expect-head`, it must match.
2. Fetch `B` and `refs/pull/N/head`; the fetched head must equal the PR head.
3. Origin check **before** any install, build or test step. Untrusted origin
   stops with `ISOLATION_REQUIRED` unless the instance runs in a verified
   isolated check-only environment (section 5).
4. For `merge-ff`: authorization (section 2), no changed path matching the
   configured merge exclusions, no change to the gate contract files, and the
   gate script and configuration in use are byte-identical to the versions on
   `B`.
5. Build `M = merge(B, H)` with `--no-ff` in a fresh worktree; verify parents
   `[B, H]` and tree `T`. A conflict stops; integration belongs in the task
   branch.
6. Classify the **merge-tree** diff `B...M`. Only a diff whose every path
   matches the documentation patterns and no "force full" pattern is
   `docs-only`. Empty, unknown and contract-touching diffs run the full plan.
7. Run setup steps, the plan's steps and teardown steps serially; teardown
   always runs. Steps are argument lists without a shell, with timeouts, a
   minimal environment without inherited credentials and optional resource
   scopes.
8. Every missing, red, timed-out or OOM-terminated required step stops.
   Steps that did not run are recorded as `SKIPPED_DOCS_ONLY` or
   `NOT_PRESENT` and are never reported as passed. There is no retry until
   green.

### 3.2 Application bootstrap state

A project whose integration branch does not yet contain its application
configures `application.markers` (for example the package manifest and the
test directory). If the checked tree contains **all** markers, application
steps are mandatory. If it contains **none**, application steps are reported
`NOT_PRESENT` and the summary lists them as not run; such a run must never be
called a passed application test. If it contains only some markers, the run
stops.

### 3.3 Release run (`check-only --main SHA`)

The SHA must be the full 40-character value of the current remote integration
ref, and the fetched ref must match it. The complete release plan runs on that
commit. A release or deployment additionally needs its own project
authorization; the gate never deploys.

### 3.4 Ref update (`merge-ff`)

1. Seal the log (section 4), push `M` to a temporary ref in the configured
   temporary namespace and publish the redacted summary with the log checksum.
2. Re-check immediately before the update: PR state, base, draft flag, head,
   unchanged handoff, remote integration ref still equal to `B`, unchanged log
   checksum and `M` topology.
3. Move the integration ref server-side with GitHub GraphQL `updateRefs`,
   `beforeOid = B`, `afterOid = M`, `force = false`. This compare-and-swap
   rejects a ref that moved — including the case where the ref moved to `H` or
   another ancestor of `M`, where a plain fast-forward push would still
   succeed.
4. Never fall back to a plain push, a force push, an admin bypass or the
   pull-request merge API. On rejection, an unclear answer or missing
   permission, read the actual remote ref and stop. If the ref already points
   to `M` after an ambiguous answer, report a blocker (`POST_VERIFY`) instead
   of claiming an unchanged state, and never attempt a second merge.
5. After the update verify the remote SHA, its tree and that the PR is
   reported merged; delete the temporary ref.

`check-only` never writes the integration ref. Every stop before the update
leaves it unchanged.

### 3.5 Probe

`probe-ref-cas` may verify compare-and-swap semantics and the token's
permission on a fresh ref inside the temporary namespace only, never on the
integration ref. It is optional and needs actual access.

## 4. Evidence and logs

- Each run writes a local run directory: `meta.json` (B, H, M, T, paths,
  classification, steps, authorization), step logs, `summary.md` and
  `SHA256SUMS`. The digest of `SHA256SUMS` is the log checksum.
- Before sealing, all files are scanned for secret patterns. A hit stops the
  run (`LOG_INTEGRITY`); nothing is published and nothing is merged.
- Only the redacted summary (identifiers, step names, states, durations,
  test-count lines, checksum) is published. Raw logs stay local. They belong
  to the same UID as the checks and are therefore not tamper-proof; the
  checksum makes later changes detectable.
- Results after sealing go to `completion.json` plus its checksum; the sealed
  log is never rewritten.
- A local simulation or a fake repository is never reported as a real merge.

Handoffs of gate tasks record: STATUS, BASE_COMMIT, BRANCH, COMMIT,
REMOTE_COMMIT_VERIFIED, gate `B`/`H`/`M`/`T`, steps with results and test
counts, log checksum, PR links, open approvals, integration state, BLOCKER and
NEXT_STEP.

## 5. Isolation

The gate runs project code under the UID that starts it. A scrubbed
environment only prevents accidental credential use; it is no process
isolation. Therefore:

- On a machine where that UID has project, deploy or provider access, code of
  untrusted origin stops with `ISOLATION_REQUIRED` before any install, build or
  test step.
- Untrusted code may be checked only by a separate gate instance in an
  environment provisioned for that purpose (own unprivileged user or VM,
  own checkout/state/lock/log area, no access to live data, tokens, SSH or
  GitHub credentials or user services). Its configuration sets
  `untrusted_code = "check-only-in-isolated-env"` with the UIDs it must not
  run as and credential paths it must not be able to read; the gate verifies
  both and the absence of credential-like environment variables before it
  runs anything. Such an instance never merges.
- The ref-update permission belongs to the orchestrating gate process only,
  never to the processes that run project checks.

## 6. Stop cases

| Code | Exit | Stop case |
| --- | --- | --- |
| `USAGE` | 2 | no mode, malformed SHA |
| `CONFIG` | 3 | configuration invalid (unknown key, wrong type, missing required value, shell string, unknown placeholder, credential-like variable) |
| `PRECONDITION` | 10 | PR not open, wrong base, incomplete application markers, missing git identity for the merge commit |
| `HEAD_MISMATCH` | 11 | head differs from expectation, fetched head, handoff or re-check |
| `BASE_MOVED` | 12 | integration ref moved; release SHA not current |
| `NOT_AUTHORIZED` | 13 | no own task PR, draft, missing handoff/merge-ready, blocker, contract not on `B`, self-authorizing gate PR, never-merge branch |
| `EXCLUDED_PATHS` | 14 | diff touches a merge-excluded path |
| `ISOLATION_REQUIRED` | 15 | untrusted origin without verified isolation |
| `RESOURCES` | 16 | lock held, too little memory/swap, other heavy checks running (the gate and its ancestors excluded) |
| `MERGE_TOPOLOGY` | 17 | conflict, wrong parents or tree |
| `GATE_FAILED` | 20 | missing, red, timed-out or OOM step; failed teardown; empty plan |
| `LOG_INTEGRITY` | 21 | secret pattern in the log, changed log before the update |
| `REF_UPDATE_REJECTED` | 30 | compare-and-swap rejected or unclear with the ref not at `M` |
| `POST_VERIFY` | 31 | ref at `M` after an ambiguous answer, or post-update check failed |
| `ERROR` | 40 | unexpected tool failure, including a failed merge without conflicting paths |

## 7. Branch rules, required checks and merge queue

Inspect, per project, the actual required checks, rulesets, branch protection
and merge queue on the account's real plan before adoption. If an API answer
is unavailable (for example on a plan without rulesets), record that; it
neither proves protection nor its absence. If a binding GitHub status rule
cannot be satisfied without a hosted check, the rollout for that project
stops and the conflict goes to the owner. The gate and its templates never
change protection rules, billing or runners. A merge queue is not combined
with the gate unless a separate design covers it; a queue's `merge_group`
event must not trigger hosted jobs automatically.

## 8. Diagnosis workflow

A project may keep or add one workflow whose only trigger is
`workflow_dispatch`. It is read-only (`permissions: contents: read`, checkout
without persisted credentials), uses no secrets, deploys nothing, starts no
agent and runs on hosted runners only. Third-party actions are pinned to
reviewed full commit SHAs. The template is
[`templates/github-actions-diagnose.example.yml`](templates/github-actions-diagnose.example.yml).
GitHub only offers manual runs for workflows on the default branch
([manually running a workflow](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)).

## 9. Relationship to other contracts

- This policy grants no deployment, release, provider activation or
  production access.
- Product contracts that require other evidence (for example an automation
  product that itself consumes hosted CI facts) keep those requirements; the
  repository gate never synthesizes such evidence.
- Branch publication rules of the
  [Universal Project Bootstrap](UNIVERSAL_PROJECT_BOOTSTRAP.md#own-task-branch-publication-policy)
  stay in force: own-branch push is not merge authority. Merge authority comes
  only from this separate contract once the project has adopted it.

## 10. Platforms

The contract above is the same on every platform; no platform gets a weaker
gate.

| Platform | Gate path | Notes |
| --- | --- | --- |
| Linux | native, reference implementation | `systemd_scope` and `watched_user_services` available where a user systemd instance runs |
| macOS | native | memory from `vm_stat` (free + inactive pages, a conservative estimate) and `sysctl vm.swapusage`, processes from `ps`; `systemd_scope = true` or non-empty `watched_user_services` stop with `PRECONDITION` instead of being ignored |
| Windows | inside WSL 2 only | the Linux path runs unchanged in the WSL distribution; the repository lives in the Linux file system; started natively on Windows the gate stops with `PRECONDITION` before reading the configuration's state directory |

A platform that cannot provide a configured protection is a named stop, never
a silent downgrade. Unit tests simulate the macOS and Windows host answers; a
simulation is not a test on that operating system.

GitHub references: [`updateRefs` and `RefUpdate`](https://docs.github.com/en/graphql/reference/git)
(`beforeOid`, `afterOid`, `force`).
