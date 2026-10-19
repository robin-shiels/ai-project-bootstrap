# Platform tests (manual)

Owner decision 2026-10-19: this repository carries exactly one active workflow,
[`.github/workflows/platform-tests.yml`](../.github/workflows/platform-tests.yml).
It checks the downloadable AI Bootstrap bundle on GitHub-hosted **macOS** and
**native Windows** runners, where no own device is available.

- Start only by hand (`workflow_dispatch`), never automatically. It is no merge
  or release condition and no substitute for the dev-box gate.
- No repository secrets, no third-party actions; the job token has
  `contents: read` only and is used to download the bundle through the
  contents API (works for public and private visibility).
- It downloads `dist/` of the given commit, verifies `SHA256SUMS`, runs the
  bundled tests and the gate host probe, checks the native-Windows stop, and
  runs the documented Claude Code and Codex installers plus the Codex sandbox.
  No account sign-in happens, so a run proves no complete guided setup.
- On Windows the run finally tries to install Ubuntu 24.04 in WSL 2 and to
  run the gate tests there; each step has a timeout. Whether WSL 2 works on
  a hosted runner is recorded, not assumed.
- The default input is the branch `claude/guided-bootstrap-v1`; the run prints
  the bundle's source commit from `BUNDLE_MANIFEST.json`.
- Standard hosted runners are free for public repositories; while the
  repository is private, minutes count against the account's Actions quota
  (GitHub billing documentation).

Start: Actions → platform-tests → Run workflow (the branch is prefilled), or
`gh workflow run platform-tests.yml -f bundle_commit=<commit or branch>` with a token
that has `actions: write`. Results: the run summary table and the step logs.
