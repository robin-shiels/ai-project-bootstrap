# Property Pilot Workflow Rule Extraction — Bootstrap Candidate Audit

**Date:** 2026-09-29  
**Purpose:** extract mature cross-project workflow rules from Property Pilot before expanding the universal bootstrap.  
**Mode:** analysis only; this report does not itself change the bootstrap contract.

## Sources inspected

Primary current-main workflow sources:
- `AGENTS.md`
- `docs/CODEX_IMPLEMENTATION_PROTOCOL.md`
- `docs/CODEX_QUALITY_GATES.md`
- `docs/CODEX_SSOT_MAP.md`
- `docs/CODEX_WORKING_RULES.md`
- `docs/TASK_SPEC_V2.md`
- `docs/PRODUCT_EXECUTION.md`

The repository tree was also inspected for related architecture/orchestration material.

## Classification model

- **UNIVERSAL_CANDIDATE** — broadly reusable across normal Git/Codex projects.
- **UNIVERSAL_WITH_PARAMETERIZATION** — useful universally but concrete values/mechanisms must be project-selected.
- **PROJECT_SPECIFIC** — belongs only in Property Pilot or an equivalent product layer.
- **AUTOMATION_SPECIFIC** — belongs to an orchestrator/software-factory execution model, not the normal manual-project baseline.
- **HISTORICAL** — evidence/context, not a current universal rule.

## Strong universal candidates missing or weaker in bootstrap v1.0

### 1. Durable completion contract for every started repository task
**Classification:** UNIVERSAL_CANDIDATE

PP applies durable Git completion not only to implementation but also to planning, research, audits, gap analyses, specifications and documentation tasks.

Candidate universal contract:
- complete in-scope result must be durable in repository files or implementation;
- closing chat must not be the only carrier of substantive results;
- task-appropriate validation must pass;
- final diff must be checked for scope, secrets, generated/runtime artifacts and documentation drift;
- task finishes on its own branch;
- exact branch is pushed;
- remote commit is verified;
- worktree is clean;
- compact closing handoff is returned.

This is materially stronger than bootstrap v1.0's current generic completion paragraph.

### 2. Standing commit/push authority for the task's own branch
**Classification:** UNIVERSAL_WITH_PARAMETERIZATION

PP grants standing authority, once a repository task has explicitly started, to commit and push only that task's dedicated branch. This removes repeated permission prompts while preserving stronger boundaries:
- no push to main;
- no merge;
- no deployment;
- no mutation of another task branch/worktree;
- stricter task restrictions still win.

Universal bootstrap should support this as a selectable/default workflow policy for manual projects, but must not silently override a project whose owner deliberately requires per-commit approval.

### 3. DONE is branch completion, not integration
**Classification:** UNIVERSAL_CANDIDATE

A universal task lifecycle should distinguish at least:
- task implementation/result complete on branch;
- ready/eligible for integration;
- integrated into current main;
- deployed/production-verified where applicable.

Never collapse these states.

### 4. Current-main revalidation before integration
**Classification:** UNIVERSAL_CANDIDATE

Before integration:
- fetch current main;
- compare changes since task base for textual and semantic overlap;
- reconcile as appropriate;
- rerun affected validation;
- do not treat green checks against the old base as integration proof;
- stop when integration would require a new owner/product decision.

Bootstrap v1.0 mentions this, but PP has a stronger operational contract worth promoting.

### 5. Two-stage parallel-safety gate
**Classification:** UNIVERSAL_CANDIDATE

PP separates:
1. planning-level dependency/scope/semantic/migration overlap assessment;
2. independent execution-time technical preflight against current repository state.

The planner identifies only a parallel candidate. The executor has technical authority to classify actual safety within already-decided product contracts.

This prevents planning-time assumptions from becoming stale execution authority.

### 6. Integration/revalidation cost as part of parallelism
**Classification:** UNIVERSAL_CANDIDATE

Technical parallelism alone is not enough. PP also classifies expected reconciliation cost:
- LOW: normally parallelize;
- MEDIUM: parallelize when saved wall-clock time plausibly exceeds reconciliation;
- HIGH: normally sequence unless a documented reason justifies heavy reconciliation.

The exact labels are reusable and prevent artificial concurrency.

### 7. Impact-based revalidation
**Classification:** UNIVERSAL_CANDIDATE

When main changes during parallel work:
- derive revalidation from the actual intervening diff;
- use focused validation for clearly bounded impact;
- escalate to broad/full acceptance for shared contracts, domain chains, migrations or uncertain impact;
- do not rerun unrelated full suites merely because work occurred in parallel.

### 8. Shared coordination-state reconciliation
**Classification:** UNIVERSAL_WITH_PARAMETERIZATION

When a project has a shared execution/status board or equivalent coordination file:
- task branches must not publish stale whole-file state;
- read the current-main version before changing shared coordination state;
- apply only the task's own transition;
- preserve unrelated concurrent entries;
- reconcile conflicts instead of choosing the branch copy wholesale.

Not every project needs such a board, so the bootstrap should define the rule conditionally.

### 9. Compact standardized handoff
**Classification:** UNIVERSAL_CANDIDATE

PP's compact fields are useful as a universal baseline:
- STATUS
- BRANCH
- COMMIT
- REMOTE_COMMIT_VERIFIED
- RESULT_FILES / ERGEBNISDATEIEN
- CORE_RESULT / KERNERGEBNIS
- VALIDATION / PRÜFUNGEN
- BLOCKER
- NEXT_STEP

Base commit and integration conditions are added when relevant.

### 10. Stricter rule precedence
**Classification:** UNIVERSAL_CANDIDATE

A clear precedence contract should be universal:
- authoritative repository instructions;
- authoritative project documentation;
- concrete task order;
- stricter explicit restrictions;
- universal baseline only fills/reconciles workflow gaps and must not weaken stricter local constraints.

### 11. No speculative future scaffolding
**Classification:** UNIVERSAL_WITH_PARAMETERIZATION

PP's principle to avoid pre-creating future modules/tables/infrastructure is broadly useful as an anti-speculation rule:
- implement only the active scope;
- do not add future architecture solely because it might be useful later.

This should be framed generically, not tied to PP modules/database.

### 12. Block on unresolved authoritative conflict
**Classification:** UNIVERSAL_CANDIDATE

When implementation choice conflicts with authoritative project principles or requires a new product/architecture decision, stop and surface the conflict rather than silently choosing.

This complements autonomous continuation: autonomy applies inside settled authority, not across decision boundaries.

## Already represented well in bootstrap v1.0

- robust repository discovery and code-search fallback;
- current repository evidence over old chat memory;
- autonomous planning/research until a real decision or durable handoff;
- recommendation-only exception;
- current-work overview;
- avoid artificial parallelism;
- durable Git work orders;
- ChatGPT/Codex separation;
- semantic skill reconciliation;
- project-specific discovery;
- idempotent bootstrap upgrades.

These should be retained and may be tightened using the PP evidence above.

## Property-specific rules — do NOT universalize

Examples:
- Property Pilot repository identity and paths;
- FastAPI/Python/uv commands;
- Decimal financial rules;
- unknown/0 domain semantics as a mandatory rule for every project;
- Property/Listing/Rent/Renovation domain contracts;
- PP Roadmap current-state requirements;
- ImmoScout/GeoMap/KSK/provider rules;
- production infrastructure details;
- PP-specific status board filename;
- PP-specific issue title prefixes.

Some underlying principles (provenance, explicit unknowns, source authority) may inspire optional generic guidance, but the concrete rules are product-specific.

## Automation/software-factory-specific rules — do NOT put into normal manual baseline

The repository still contains extensive historical/current orchestration contracts:
- READY authorization;
- coordinator-only Git control;
- generation/state refs;
- automatic retries/self-repair;
- retained workspace recovery;
- task-spec-v2 machine contracts;
- model routing and model-capacity fallback;
- provider budgets;
- automated claims/workers/webhooks;
- technical resolution pipelines.

These are valuable inputs for a software factory but would constrain or confuse ordinary manual projects if made universal.

The bootstrap may define an optional **automation profile** later, but v1 manual-project baseline should not inherit these mechanics.

## Skill observations

PP repository evidence proves strong workflow contracts but does not by itself prove that named ChatGPT/Codex skills are installed in the runtime.

Therefore:
- continue to inventory actual skill availability separately;
- do not equate docs with installed skills;
- use mature PP workflow behavior to improve capability contracts even when no named skill exists.

## Recommended bootstrap changes

Before declaring v1.0 stable, revise the universal standard and skill manifest to incorporate candidates 1–10, and consider 11–12.

The update should preserve a profile distinction:
- **manual-project baseline** — normal ChatGPT planning + manually launched Codex tasks;
- **automation profile (future/optional)** — software-factory/orchestrator behavior.

Do not make the automation profile a prerequisite for ordinary projects.

## Next extraction source

After PP, perform the same rule/skill extraction against:
1. KI-Sekretär — identify reusable rules that PP lacks;
2. Software Factory — extract universal principles, but classify its automation mechanics separately.

Only after all three inventories should the bootstrap be promoted from the current foundation to a consolidated best-of baseline.
