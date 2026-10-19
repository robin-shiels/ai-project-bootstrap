# Platform tests (manual)

Owner decision 2026-10-19: this repository carries exactly one active workflow,
[`.github/workflows/platform-tests.yml`](../.github/workflows/platform-tests.yml).
It checks the downloadable AI Bootstrap bundle on GitHub-hosted **macOS** and
**native Windows** runners, where no own device is available.

- Start only by hand (`workflow_dispatch`), never automatically. It is no merge
  or release condition and no substitute for the dev-box gate.
- No repository secrets, no third-party actions; the job token has
  `contents: read` only and is used to download the bundle from this private
  repository.
- It downloads `dist/` of the given commit, verifies `SHA256SUMS`, runs the
  bundled tests and the gate host probe, checks the native-Windows stop, and
  runs the documented Claude Code and Codex installers plus the Codex sandbox.
  No account sign-in happens, so a run proves no complete guided setup.
- WSL 2 is not expected to be available on the hosted Windows runner; the run
  records what `wsl --status` reports.
- Private repository: minutes count against the account's GitHub Actions
  quota (see GitHub's billing documentation).

Start: Actions → platform-tests → Run workflow (the commit is prefilled), or
`gh workflow run platform-tests.yml -f bundle_commit=<commit>` with a token
that has `actions: write`. Results: the run summary table and the step logs.
