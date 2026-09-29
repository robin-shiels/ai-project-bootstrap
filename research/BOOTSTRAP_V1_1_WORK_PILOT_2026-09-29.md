# Work pilot of Bootstrap v1.1.0 — 2026-09-29

## Scope

The user requested autonomous testing in ChatGPT Work without creating real projects. One Work agent executed the planning/bootstrap workflow and a documentation task using separate fresh local clones and a local bare Git remote. No new GitHub repository or native ChatGPT project was created. This extends the earlier local walkthrough with actual task execution and Git publication. It is not an independent-agent or native ChatGPT-to-Codex integration test.

Pinned standard/base: `robin-shiels/ai-project-bootstrap@217b4b3ccd75557f707a627df87c2495e36cd35c`, v1.1.0. Read the standard, Codex handoff template and capability manifest directly. The actual Work commentary prominently disclosed default B and PER_TASK_APPROVAL/DISABLED alternatives before reliance. User scope grants execution of the temporary test; scenario opt-outs/restrictions are controlled test inputs, not claimed new real Owner decisions.

## Actual sequence and results

| Step | Actual action and evidence | Outcome |
| --- | --- | --- |
| Provision | Created a local bare remote and Markdown-only seed with explicit purpose/non-goals. Seed/main: `fec8368e9f831dc311cafac1a2bae2e71b250352`. | Default branch discovered from origin HEAD as main. Initial seed publication is test provisioning, separate from task authority. |
| Planning/bootstrap | Read target README; classified project scope/store as EQUIVALENT and workflow/authority instructions as MISSING. Wrote authoritative AGENTS.md, durable tasks, planning result and concrete handoff. Validated six Markdown files, then committed/pushed only pilot/bootstrap. | Local and remote SHA `30816a55bf7b3e51d40997e6abae7dfc2c854b2c`; clean planner checkout. |
| Fresh execution | Cloned origin anew; read the actual published task, handoff and instructions. Created pilot/handbook, added a lifecycle example plus durable result; validated eight Markdown files, content/authority and scoped diff; committed/pushed that branch. | Local/remote SHA `2331baf2b37219befd2eb87dece0cba2aba76b1d`; clean executor checkout. DONE_ON_BRANCH applies only to the local-Git-backend experiment. |
| Re-bootstrap | Manually re-inventoried the relevant contracts against the pinned standard, compared semantics rather than the marker, and found no further document change necessary. | HEAD stayed `2331baf`; AGENTS Git blob remained `c3aaf56f3c1c72aae63d7863bc6d22d234700a5b`; clean before/after. This is one agent's no-rewrite decision, not statistical proof of idempotence. |
| Stronger task prohibition | Fresh clone at bootstrap base; local-only task explicitly forbids stage/commit/push. Created and directly validated output/result, including untracked files. | HEAD stayed `30816a5`, index empty, two untracked results; no remote pilot/local-only branch. LOCAL_COMPLETE. |
| Full opt-out | Separate checkout at bootstrap base; controlled scenario selects DISABLED. Wrote local policy/result and validated seven Markdown files. | HEAD stayed `30816a5`; AGENTS modified and result untracked; no remote pilot/disabled branch, stage or task commit. LOCAL_COMPLETE. |
| Existing split authority | Separate fixture gives local commit permission but per-task push approval. Preserved that policy, classified automatic push adoption as CONFLICT, and recorded the decision requirement. Relevant checks then local report commit only. | Fixture policy base `97946f74681c6c4a428352c0440b01e2b0e4da5f`; local report commit `a1fd7f0e1ce7b8da316fe4cc1e3caa8e778fd50a`; no remote pilot/restricted branch. LOCAL_COMPLETE. |

Final local-remote refs remained exactly seed/main plus pilot/bootstrap and pilot/handbook. No task pushed main, merged, tagged or deployed. Restriction cases intentionally retain local results. Public research publication is a separate owned Bootstrap research branch; it does not publish the test branches to GitHub.

## Verification

Actual commands included git init --bare, clone, remote show origin, switch, status --porcelain, rev-parse, diff --cached --check, commit, push with exact branch refspec, ls-remote and for-each-ref. A temporary direct Markdown checker reads every Markdown file in the target, including untracked files, checking headings/newlines/whitespace/fences, local-link existence and basic credential patterns. Relevant commands completed with exit 0. Content, lifecycle distinctions, scope and privacy were additionally reviewed by this same agent. No product test suite exists or was manufactured.

Research-file validation initially scanned pre-existing reports and rejected their intentional Markdown hard-break whitespace. It was narrowed to the two owned new files. An optional Markdown parser was unavailable; no dependency was installed. Targeted checks instead ignore fenced snapshots when resolving real links and passed together with the staged diff check.

The [evidence packet](evidence/WORK_PILOT_V1_1_2026-09-29.md) retains actual target instructions, task/handoff, outputs, results and final Git state. Temporary checker limitations: it does not exhaustively validate Markdown anchors or detect every possible secret. There are no anchor links or real credentials in this controlled documentation fixture.

## Findings and limits

- Actual Git task completion, exact remote SHA verification, opt-out retention and split commit/push handling worked in this controlled local environment.
- The supplied handoff used a vague sibling-checkout description for the standard. The exact pinned source was available in this Work workspace, but the relative placement description was not accurate from every clone. A portable handoff should carry a directly resolvable source location plus the pin. This is an authored test-handoff defect; the current template already requires source/reference evidence.
- Re-bootstrap retained equivalent instructions without duplication in this one manual run. No autonomous reconciler, separate executor or repeated user cohort was evaluated.
- Instruction compliance here is agent behavior, not a technical Git access restriction. No claim that DISABLED is enforced by a server hook or permission system.
- The actual Work setup notice was delivered, but native ChatGPT project settings and a separate Codex session were not configured. A generated handoff and fresh clone cannot prove those product integrations or user comprehension.
- Local bare-remote push proves Git mechanics, not GitHub credentials, branch protections, cloud task visibility, CI, or provider execution. Those require separate environment evidence.

## Recommendation

Retain v1.1.0 unchanged and use this report as limited additional evidence when comparing the friends' contributions. No mandatory new rule is justified by this run. A future independent-agent/product-surface test may extend coverage if needed; no real project creation is necessary for the local tests completed here.
