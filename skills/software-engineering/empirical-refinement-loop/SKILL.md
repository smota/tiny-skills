---
name: empirical-refinement-loop
description: Conduct bounded software refinement cycles with independent adversarial review, comparable measurements, fail-closed acceptance, and repository-backed continuity across conversations.
category: software-engineering
---

# Empirical Refinement Loop

## Purpose

Improve a scoped software behavior through reproducible experiments and independent review. Preserve the project's engineering approach and accumulated evidence so later conversations resume with a small context.

## Prerequisites

- Repository read access for discovery; write access for initialization and execution.
- The project's installed build, test, and measurement tools; discover their setup from project documentation. No language or benchmark package is mandatory.
- A harness capable of creating an independent subagent for reviewed execution, or a user-selected external reviewer CLI with its required account, credentials, and setup. Planning and initialization require neither.
- For external review, permission to send the selected context to that provider. Verify CLI usage locally; use bounded execution and capture output without secrets.
- Git only when the project uses it; identity and explicit delivery scope for commits, remote credentials and push authorization for publication.

## Commands

These are conversational entry points, not executable CLI flags. Equivalent prose works.

### `/empirical-refinement-loop init [path]`

- **Input:** Project path, optional known strategy documents and storage preference.
- **Action:** Discover existing engineering guidance, agree on missing document placement, and connect or establish the local approach using [state-and-output](references/state-and-output.md).
- **Output:** A compact `.empirical-refinement-loop/state.json` index and only the agreed missing documentation. Do not change application code.
- **Failure:** Report inaccessible or ambiguous sources. Distinguish not found from nonexistent; ask for a pointer before duplicating a possible authority.

### `/empirical-refinement-loop plan [scope]`

- **Input:** Objective and optional project path, rounds, reviewer, and execution budget.
- **Action:** Inspect pointers and relevant project evidence. Propose baseline measurements, acceptance criteria, review strategy, and bounded work. Read the references needed to make the proposal concrete.
- **Output:** A read-only proposal with document destinations, prerequisites, unknowns, and stopping conditions.
- **Failure:** Report missing evidence and unavailable commands; do not invent baseline results or create state files.

### `/empirical-refinement-loop run [scope] [rounds=N]`

- **Input:** Scoped objective; default to one round when no count is supplied. Reuse an agreed approach and reviewer preference.
- **Action:** Execute the workflow below within existing authorization. Resolve missing storage decisions through initialization before writing documentation.
- **Output:** Round evidence, accepted or rejected result, actionable backlog entries, and a resumable checkpoint.
- **Failure:** Stop with `blocked` or `inconclusive` when required review or evidence is unavailable. A failed gate never becomes accepted through backlog deferral.

### `/empirical-refinement-loop resume`

- **Input:** Existing project index and any new objective or constraints.
- **Action:** Revalidate the checkpoint against current code, environment, and criteria; resume the pending step rather than replaying completed rounds.
- **Output:** Continued execution or a precise explanation of the affected baseline that needs revalidation.
- **Failure:** Preserve unreadable, unsupported, or conflicting state. Report the mismatch and propose repair; do not overwrite it with a fresh run.

## Workflow

1. **Orient.** Read the compact index, referenced approach, and only relevant map/scorecard sections. Follow [state-and-output](references/state-and-output.md) for initial discovery, document placement, and freshness. Finish with an explicit scope, known sources, reviewer, and budget. By default allow one proposal revision and one corrective implementation attempt per round; use different bounded limits when agreed.
2. **Establish comparison.** Follow [benchmark-scorecard](references/benchmark-scorecard.md). Reuse native runners; add a minimal project-native measurement only when needed. Record baseline evidence and freeze the criteria used for comparison. Finish when required baseline observations are valid, or stop as inconclusive.
3. **Propose and challenge.** Use [the round template](assets/round-proposal.template.md) and [sparring-protocol](references/sparring-protocol.md). Obtain a real independent critique, respond with mitigation or evidence, and resolve blocking objections before implementation.
4. **Implement and evaluate.** Change only the scoped behavior and demonstrated test gaps. Use realistic E2E and isolated failure injection when the hypothesis requires them. Execute required project checks and scorecard measurements against the exact candidate. Required missing evidence closes the gate. Correct within the budget or stop; do not expand scope to force success.
5. **Checkpoint.** Persist the round result, evidence references, pending step, and last accepted result separately. A checkpoint is not a Git commit. Commit or push only when requested within delivery scope, staging task-owned changes explicitly.
6. **Close or continue.** Stop on objective achieved, budget exhausted, lack of progress, or an external impediment; N is a maximum, not a quota for unnecessary changes. Consolidate knowledge and backlog using [state-and-output](references/state-and-output.md). Continue another authorized round only when a useful hypothesis remains.

## Constraints

- Existing project documents remain authoritative; the hidden folder is an index by default. Internal documentation there is an explicit storage choice.
- Keep review provenance honest. Self-review is available only when requested and must be labeled as lacking independent review.
- Required invariants come from relevant contracts, not a universal metric quota. Preserve unresolved required failures even when they exceed the round's scope.
- Inject faults in isolated, owned resources. Record resource ownership before launch and clean only those resources. Preserve unrelated files, processes, and user changes; propose recovery when safe rollback cannot be proven.
- No automatic installation, production fault injection, provider switching, publication, or broad Git rollback follows from a refinement request.
- Evolve the method only from demonstrated shortcomings. Do not require additional tests, metrics, or application changes merely to complete a round.

## Examples

- `/empirical-refinement-loop init .` — connect existing engineering documentation and choose where missing guidance belongs.
- `/empirical-refinement-loop plan payment retries` — propose a reproducible reliability experiment without mutations.
- `/empirical-refinement-loop run worker shutdown rounds=2` — conduct up to two reviewed rounds, preserving evidence and stopping if blocked.
- `/empirical-refinement-loop resume` — inspect drift and continue the pending step with bounded context.

## Credits

Adapted from Samuel's Empirical Refinement Loop design and supplied Meshloop-derived engineering discussion, including the recovered session steps 125 and 141 and subsequent repository-integration decisions. These are design provenance, not runtime dependencies or proof of Meshloop results. Statistical guidance references the NIST Engineering Statistics Handbook in the scorecard reference.
