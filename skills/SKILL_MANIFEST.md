# Universal Skill & Capability Manifest

**Bootstrap standard:** v1.0.0

This manifest defines reusable capabilities, not assumptions that a named skill is installed. A Markdown file is not automatically an active skill. Bootstrap compares actual behavior and availability.

## ChatGPT-side capabilities

### Brainstorming / structured discovery — required when decisions are missing
- inspect existing context first;
- ask only questions that resolve genuine project/product choices;
- surface trade-offs and overlooked decisions;
- do not re-ask established decisions;
- distinguish owner choices from technical decisions;
- converge toward a sufficiently specified outcome.
For project bootstrap, discovery creates project-specific rules without adding them to the universal standard.

### Planning / executable work orders — required
- inspect current repository state;
- continue autonomously through non-decision intermediate steps;
- identify genuine owner decisions;
- store substantial work orders durably in Git where appropriate;
- define scope, non-goals, acceptance, validation, authority and handoff;
- return a short execution start prompt after the durable order exists.

### Research / audit — required capability
- separate evidence from assumptions;
- inspect repository and external sources when relevant;
- state uncertainty;
- persist substantial reports;
- convert findings into planning inputs without automatically executing recommendation-only follow-ups.

### Skill authoring / maintenance — optional until needed
When reusable custom skills are created, keep them product-neutral unless explicitly project-specific. Version and reconcile them semantically.

## Codex-side capabilities

### Repository instruction discovery — required
Read applicable repository instructions before changes and respect nested/local instructions where the environment supports them.

### Implementation planning — required for substantial work
Translate the durable order into an execution plan without reopening settled product decisions.

### Systematic debugging — required when diagnosing failures
Reproduce, isolate, identify root cause, add regression evidence, fix the root cause and revalidate.

### Testing / verification — required
Use risk-based checks appropriate to the repository. Never treat a green narrow test as proof of unrelated system behavior.

### Git isolation / parallel execution — required when parallel work is used
Use dedicated branches/worktrees or the project's equivalent isolation. Revalidate against current main before integration.

### Completion reporting — required
Return compact status, branch/commit where applicable, validation, blockers, integration/deployment state and owner action.

### Skill authoring — optional until needed
Reusable Codex skills should be created only when they improve recurring execution and should be versioned/reconciled rather than duplicated.

## Reconciliation

For each capability classify:
- MISSING
- EQUIVALENT
- OUTDATED
- CONFLICT

Names do not determine equivalence. OUTDATED capabilities should be upgraded when project-specific intent is preserved. CONFLICT requires owner resolution.

Do not install optional capabilities merely to maximize skill count.
