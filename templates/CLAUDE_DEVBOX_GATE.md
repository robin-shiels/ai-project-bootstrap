# CLAUDE.md section: dev-box merge gate

For projects that keep a separate `CLAUDE.md` next to `AGENTS.md`. Keep it a
short pointer; `AGENTS.md` (or the project's equivalent) stays authoritative.
Do not create a `CLAUDE.md` only for this section if the project's tools
already read `AGENTS.md`.

---

## Dev-box merge gate

`AGENTS.md`, section "Dev-box merge gate", is binding. In short:

- Never trigger hosted CI automatically and never add automatic workflow
  triggers. A manual `workflow_dispatch` diagnosis needs a concrete reason.
- Check PRs with `<gate script path> --config <gate config path> check-only
  --pr <N>` on the actual merge result; check releases with `check-only --main
  <full SHA>`.
- Auto-merge only own task PRs with `STATUS: DONE`, matching `COMMIT`,
  `BLOCKER: none` and `MERGE_READY: yes`, through `merge-ff
  --confirm-own-task-pr <N>`. Never `git push` to `<integration branch>`,
  never `gh pr merge`, never force.
- The gate bootstrap PR and every PR that changes the gate are presented to
  the owner with `B`/`H`/`T` evidence; they are never self-merged.
- Untrusted code only in the isolated environment; no deployment from a
  merge or a green gate.
- Existing stricter rules, open owner questions and branch rules win.
