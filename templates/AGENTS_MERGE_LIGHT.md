# AGENTS.md section: LIGHT merge and deployment

Insert the section below into the target project's authoritative instructions
(normally `AGENTS.md`). Replace every `<...>` with inspected project facts or
the Owner's answers.

**Before inserting:** read the project's current merge, push, release and
deployment rules. If an existing rule forbids merges or deployments or the
project has an integrated dev-box gate, do not overwrite it silently. Classify
the difference as CONFLICT, show the existing and the proposed behavior and
keep the existing rule until the Owner decides.

---

## Merge and deployment (LIGHT)

Contract: Universal Project Bootstrap `UNIVERSAL_PROJECT_BOOTSTRAP.md`,
section "Merge and deployment policy", policy LIGHT, recorded <date> (notice
delivered <date/setup response>; Owner choice: <default LIGHT | explicit>).

### Merge

The executor may merge its own task PR without asking when all of these hold:

1. It is its own task PR in this repository; never a foreign, unknown or fork
   PR.
2. No open decision, requested review or explicit hold is recorded.
3. Immediately before the merge the PR head contains the current
   `<default branch>`. If `<default branch>` moved since the last check,
   update the branch, rerun the checks, then continue.
4. These checks passed locally on exactly that head commit: `<check commands>`.
   Skipped, red or timed-out checks are not passed.
5. The merge is bound to the checked commit:
   `gh pr merge <N> --<merge method> --match-head-commit <sha>`.
6. The PR does not change this section, the project's authority rules or a
   gate configuration; such PRs need explicit Owner integration.

Never push directly to `<default branch>`, never force-push, never use an
admin bypass.

### Deployment

- Target: `<deployment target | none>`. Command: `<deploy command | none>`.
- After a merge, deploy from the merged `<default branch>` commit with the
  command above and check the result: `<result check>`. A failed check is a
  stop; report it and follow `<rollback procedure>`.
- Production with real user data: `<automatic | ask before each deployment>`
  (Owner decision <date>).
- Without a recorded target there is no deployment.

### Escalation

If `<default branch>` is broken after a merge, a deployment had to be rolled
back, the same defect recurs, or several tasks run in parallel on overlapping
files, raise it with the Owner and evaluate GATE (dev-box merge gate) and
PER_CHANGE_APPROVAL together. Never switch the policy silently.
