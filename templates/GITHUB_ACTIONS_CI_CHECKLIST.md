# CI rollout checklist

Copy this into a project task and fill in the real values. Keep account costs,
private repository names and production details in the project, not in this
public template.

- [ ] Repository, default branch, integration branches and current revision verified.
- [ ] Workflows, events, last comparable runs, job durations, runner OS and matrix recorded.
- [ ] Required checks, branch protection, rulesets and merge queue support checked on the actual plan.
- [ ] Full tests listed for code PRs and the final default-branch commit.
- [ ] Feature pushes do not duplicate PR CI; other triggers have a specific purpose.
- [ ] PR concurrency isolates workflow/event/PR; default-branch runs are not cancelled.
- [ ] Documentation handling keeps the required check created, fails closed on unknown paths and reports skipped tests honestly.
- [ ] Test matrix matches supported runtimes; timeout has evidence-based headroom.
- [ ] Permissions are least privilege; action SHAs pinned; checkout credentials are not persisted.
- [ ] Cache and artifact retention justified by measured runtime and storage use.
- [ ] Local pre-push commands documented; CI checks the exact PR head before merge.
- [ ] If a merge queue is enabled, `merge_group` runs on its combined candidate.
- [ ] Workflow syntax and scope tests pass locally; PR diff contains only intended CI/docs changes.
- [ ] PR documents baseline, **scenario** saving, actual validation, risks and merge conditions.

For a uv-based Python project with an existing `uv.lock`, start from
[`github-actions-python-ci.yml`](github-actions-python-ci.yml). Adapt the
matrix, commands and timeout to the project; do not copy it into a repository
whose tests, dependency layout or protected checks differ.
