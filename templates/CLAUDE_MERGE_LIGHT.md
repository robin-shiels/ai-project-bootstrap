# CLAUDE.md section: LIGHT merge and deployment

For projects that keep a separate `CLAUDE.md` next to `AGENTS.md`. Keep it a
short pointer; `AGENTS.md` (or the project's equivalent) stays authoritative.
Do not create a `CLAUDE.md` only for this section if Claude Code already reads
`AGENTS.md` (no `CLAUDE.md` present).

---

## Merge and deployment (LIGHT)

`AGENTS.md`, section "Merge and deployment (LIGHT)", is binding. In short:

- Merge only own task PRs without open decision, after `<check commands>`
  passed on the current head that contains `<default branch>`; rerun the
  checks if `<default branch>` moved. Bind the merge to the checked commit
  with `gh pr merge --match-head-commit <sha>`.
- Never merge foreign or fork PRs or PRs that change the merge rules or a
  gate. Never push to `<default branch>`, never force.
- Deploy only to `<deployment target>` with `<deploy command>` and check the
  result; production with real user data as recorded in `AGENTS.md`.
- Raise escalation signs with the Owner instead of switching the policy.
- Existing stricter rules and open owner questions win.
