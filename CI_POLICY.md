# Cost-aware GitHub Actions CI policy

This policy is product-neutral. Reconcile it with each repository's actual
language, checks, release contract and GitHub plan before copying a workflow.
The [rollout checklist](templates/GITHUB_ACTIONS_CI_CHECKLIST.md) and
[Python example](templates/github-actions-python-ci.yml) are starting points,
not a claim that every project has Python, uv or an enforceable ruleset.

## Audit before changes

Record the default and integration branches, existing workflows and events,
recent runs with **job-level** durations, runner operating systems and matrix
sizes, cancellations, cache usage, PR topology, required check names, branch
rules/rulesets and merge queue availability. Inspect the exact current base
and repository instructions. Separate observed billing from estimates; GitHub
rounds billable time per job. Public and private repository allowances differ,
and an account may block job starts when billing or limits need attention.

## Default trigger and gate contract

1. Prefer `main` as the durable integration branch for new projects; preserve
   an existing branch choice until its owner authorizes migration. Run full,
   read-only CI for every code PR and for the final integration commit on
   that branch. Use `pull_request` for feature work and
   `push` only on the default branch; avoid running the same feature commit
   from both events. Add other events only for a documented need.
2. Keep a stable, always-created check on every PR. Avoid workflow-level
   `paths` / `paths-ignore` filters when the workflow or its jobs may be
   required; a skipped workflow can leave the check Pending. For pure
   documentation, classify paths **inside** a job and visibly report skipped
   application tests. Treat unknown paths, empty/failed diffs, CI scripts,
   workflow files, dependencies, tests and mixed changes as full CI. Validate
   rename/deletion behavior and the actual PR merge tree. Never call a
   deliberately skipped test a passing test. If documentation-only skips cost
   more extra jobs on code PRs than they save, keep classification within
   existing jobs or run the full suite.
3. Set `concurrency.group` with workflow identity, event type and PR number
   (or ref). Set `cancel-in-progress` for PRs, so new commits cancel only older
   runs of the same PR. Do not cancel default-branch or unrelated workflow
   runs through a shared group.
4. Use the smallest supported test matrix that still covers the project's
   declared runtime contract. Reduce a dimension only with evidence and
   owner approval for any lost support. Choose timeouts from observed job
   lengths with headroom; a timeout is a failure, not a green shortcut.
5. Use `permissions: contents: read` or less by default, checkout without
   persisted credentials and pin third-party actions to reviewed commit SHAs.
   Do not expose production secrets to PR code. CI should never deploy unless
   deployment is a separately authorized, protected workflow.
6. Add caches only when measured time saved exceeds cache/storage cost and
   keys follow the lockfile and tool version. Do not cache secrets, mutable
   production data or unbounded reports. Retain only short-lived failure
   artifacts needed for diagnosis.
7. Run focused tests locally before pushing, then the project's broader
   affected gates before asking for review. This avoids avoidable failed CI
   runs; it does not replace a green CI result on the **exact PR head**.

## Merge protection and queue

Inspect the plan's actual ruleset support and check names. If enforceable
required checks are available, require the stable gate on the protected
integration branch and block direct bypass. If not, the reviewer must verify
the exact-head checks manually; documentation must not imply protection that
is unavailable. For a merge queue, add the `merge_group` event and check the
combined queued candidate before enabling it. Keep the default-branch push
check for the final commit and any release/deployment gate that requires it.
Do not merge a red, missing or cancelled applicable check.

## Review and measurement

Make CI-only changes on a dedicated branch and PR. Record the audit window,
baseline job-minutes, proposed workload scenarios, local validation, remaining
risks and the exact check statuses. After integration, compare a similar mix
of runs; report actual minutes saved separately from scenarios. Refresh
assumptions when GitHub billing, plan, branch rules or project stack changes.
