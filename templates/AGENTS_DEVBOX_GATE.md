# AGENTS.md section: dev-box merge gate

Insert the section below into the target project's authoritative instructions
(normally `AGENTS.md`). Replace every `<...>` with inspected project facts.

**Before inserting:** read the project's current merge, push, release and
deployment rules. If an existing rule forbids merges or demands hosted CI,
do not overwrite it silently. Classify it as CONFLICT, show the existing and
the proposed behavior and keep the existing rule until the owner decides.
Stricter project rules, open owner questions, infrastructure/migration
exclusions and branch rules always take precedence over this section.

---

## Dev-box merge gate

Contract: Universal Project Bootstrap `DEVBOX_GATE_POLICY.md` (policy
version 1), adopted <date> by owner decision <reference>. Gate:
`<gate script path>` with `<gate config path>`.

### Hosted CI

- GitHub-hosted workflows start only through deliberate `workflow_dispatch`
  for diagnosis. No `push`, `pull_request`, `merge_group`, `schedule`,
  `workflow_run` or other automatic trigger; no self-hosted runner.
- Do not start a diagnosis run routinely. A red run that executed steps
  stops the change it diagnosed. A job that failed before its first step is no
  test result.

### Checks

- Before asking for review, run the project's focused checks locally.
- The binding merge check is `check-only --pr <N>` on the actual merge
  commit `M` of current `<integration branch>` and the exact PR head. The
  binding release check is `check-only --main <full SHA>` on the exact current
  remote commit. Never reuse an older green run after `B` or `H` moved.
- Record `B`, `H`, `M`, `T`, every step with its result, test counts and the
  log checksum in the handoff. Do not call a skipped or not-present step
  passed.

### Merge

- Own-branch commit/push follows the publication policy in this file; push
  authority is not merge authority.
- After the gate contract is on `<integration branch>`, an **own task PR**
  (this repository, author `<trusted account(s)>`, branch `<merge pattern(s)>`,
  not draft) whose handoff says `STATUS: DONE`, `COMMIT: <head>`,
  `BLOCKER: none` and `MERGE_READY: yes` may be integrated with
  `merge-ff --pr <N> --confirm-own-task-pr <N>` after a complete green run.
- Set `MERGE_READY: yes` only when the task order allows integration and no
  product, security, provider, cost or architecture question is open.
- Never merge: drafts, foreign or fork PRs, PRs with open decisions, PRs
  touching `<merge-excluded paths>`, PRs that change the gate script or its
  configuration, and the gate bootstrap PR. These need a separate owner
  decision with the exact `B`/`H`/`T` evidence.
- Only the gate moves `<integration branch>`, by compare-and-swap
  (`updateRefs`, `beforeOid=B`, `afterOid=M`, `force=false`). No plain push,
  force push, admin bypass or `gh pr merge` as a fallback. On an unclear
  answer read the actual remote ref and report a blocker.
- <Optional, only with a documented owner decision: named project exceptions,
  one PR number and exact branch each. Never a wildcard.>

### Untrusted code

- Code from foreign accounts, forks or unknown branches is never run under
  the UID that has project, deploy or provider access. Check it only in the
  isolated environment `<name or "not provisioned">`; never merge it without a
  separate owner decision.

### Deployment

- Deployment is not covered by this section. It needs the project's own
  deployment authorization <reference or "none granted"> and a fresh
  `check-only --main` run on the exact current commit.
