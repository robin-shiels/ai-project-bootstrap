# Bootstrap v1.1.0 disposable pilot — 2026-09-29

## Scope and evidence

This is a **local, self-run contract walkthrough**, not an independent user study or a verified ChatGPT/Codex runtime bootstrap. It tests the documented branching and authority decisions against two disposable Git repositories. No target project, provider, production service, release, or deployment was changed. The temporary fixtures were not published.

- Standard: `robin-shiels/ai-project-bootstrap`, `main@217b4b3ccd75557f707a627df87c2495e36cd35c` (v1.1.0).
- Inspected sources: `UNIVERSAL_PROJECT_BOOTSTRAP.md`, `README.md`, `templates/PROJECT_DISCOVERY.md`, `templates/CODEX_BOOTSTRAP_PROMPT.md`, and `skills/SKILL_MANIFEST.md` at that revision.
- Fixture A: fresh Markdown-only `Field Notes` repository, seed `0c3866ddb3d1db6924de7f59b4fb91a4943cfdbf`. Its README states the goal, no runtime/providers/deployment, documentation checks, and `docs/tasks` plus `docs/results` as canonical stores. No initial `AGENTS.md`.
- Fixture B: existing Markdown-only `Field Notes Legacy`, seed `5b46eada782f26fb5c0049612226723a69f2b8cc`. Its `AGENTS.md` permits local own-branch commits but requires explicit per-task permission before **any push**.

The fixture content was invented solely for this test. Its simulated Owner choices do not represent a real user's approval or modify the Bootstrap repository's authority. ChatGPT native project instructions and a separate Codex runtime were not configured or tested.

## Walkthrough and observed state

| Case | Performed | Observed Git and contract outcome |
| --- | --- | --- |
| A1: new project, disclosed default B | Created `pilot/new-default` from the seed, wrote a simulated setup response with the full prominent B notice and three choices, recorded `ALLOW_AFTER_CHECKS` with source/date/scope in `AGENTS.md`, and generated a project-specific Codex launcher carrying the policy source. Reviewed and committed only these three files. | Local fixture commit `ecf5d69ef90ea4c44dfa7328ab73948c9859642d`; own branch clean. No remote exists, so **LOCAL_COMPLETE**, never `DONE_ON_BRANCH`. The no-main/merge/release/deployment boundaries remain explicit. |
| A2: new project, opt-out | Created `pilot/new-optout` from the same seed. Wrote a simulated instruction stating that the Owner chose `DISABLED` before publication. Checked the untracked file directly and deliberately stopped before `git add`, commit, or push. | HEAD remains the seed `0c3866d`; `AGENTS.md` is untracked. A local result exists, publication is intentionally absent: **LOCAL_COMPLETE**, not `DONE_ON_BRANCH`. This is a simulated choice, not a real Owner decision. |
| B: existing per-task push rule | Read its existing `AGENTS.md` and compared its separate commit/push permissions to v1.1.0. No files or Git refs were changed. | Own-branch local commit permission remains; proposed automatic own-branch push is **CONFLICT** and requires an actual Owner decision. Silent B adoption would violate the existing rule. |

Commands used included `git init -b main`, fixture commits, `git switch -c`, `git diff --cached --check` before A1's commit, `git status --short --branch`, `git log -1 --oneline`, and `git rev-parse HEAD`. A direct read of A1's three committed files checked headings, publication choices, source reference, whitespace and simple credential patterns; it passed. A first naive credential substring scan falsely matched `sk-` inside ordinary `task-branch` text; a constrained pattern corrected it. In A2, `git diff --check` returned 0 but ignored the untracked `AGENTS.md`; a direct Python read then confirmed the `DISABLED` text, no trailing whitespace and a final newline. Final targeted checks exited 0. This is documentation/authority validation; no product runtime or product test suite exists in the fixtures.

## Findings

1. **No contract contradiction found in the three simulated cases.** The written standard distinguishes new-project default B, new-project opt-out, and existing restrictive authority. The Codex template explicitly requires independent verification of the recorded policy and does not infer main/integration rights.
2. **Publication cannot be proven from a local fixture.** The A1 branch has a verified local commit, but no remote SHA comparison. This is an intentional coverage limit, not a passing remote-completion test.
3. **The notice is only simulated.** A Markdown transcript cannot prove it appeared in a real ChatGPT setup response, that native project instructions were updated, or that the user saw/understood the choices. A later real-project pilot should retain a setup-response reference and inspect the authoritative target instructions.
4. **The Codex handoff is only inspected as text.** A separate executor has not attempted discovery, skill reconciliation, opt-out enforcement or remote publication. No claim of an end-to-end successful bootstrap follows.
5. **Status overview remains evidence-dependent.** A branch, fixture file or worktree does not establish that an agent is currently running. A live execution-status source is separate future Software Factory work ([Factory issue #1](https://github.com/robin-shiels/codex-software-factory/issues/1)).
6. **Opt-out files need direct checks.** `git diff --check` silently excludes an untracked local result. A checker must read untracked files explicitly (or stage intent to add without committing) before calling an unpublished result verified. The direct check was applied here; whether the standard needs an explicit example can wait for broader evidence.

## Recommendation and boundary

Keep v1.1.0 unchanged based on this limited walkthrough. When the two external contributions arrive, compare their rules against the existing six-audit evidence. A separate real pilot on a deliberately selected target project should then verify the actual ChatGPT notice, persisted effective policy, Codex execution, remote SHA and clean worktree. Do not treat this report as a grant to bootstrap another project, merge this research branch, publish a release, or deploy anything.
