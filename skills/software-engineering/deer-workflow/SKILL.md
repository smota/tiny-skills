---
name: deer-workflow
description: Design, generate, validate, run, inspect, and resume Deer Workflow graphs from inside an agent session.
category: software-engineering
---

# Deer Workflow

Use this skill when a user wants graph-based orchestration with `@deerwork-ai/deer-workflow` without manually driving its CLI. Keep generated workflows reviewable, execution observable, and side effects explicit.

## Purpose

Translate an orchestration goal into TypeScript using Deer Workflow primitives, then operate it through the package API from the current agent session. Prefer `WorkflowRunner` and harness APIs over `deer-workflow create` subprocess calls.

## Inputs

- Natural-language workflow goal.
- Optional existing `.ts`/`.js` Workflow module.
- Optional harness: `pi`, `codex`, or `claude`.
- Optional run parameters: input, timeout, retries, checkpoint location.

## Outputs

- Design: node/edge plan and side-effect review.
- Create: source file containing a Workflow module.
- Validate: diagnostics and type-check result.
- Run: run ID, event summary, outputs, and checkpoint.
- Inspect: phase/node status, timings, logs, and errors.
- Resume: updated run ID and continuation result.

## Prerequisites

- Node.js or Bun.
- Project dependency `@deerwork-ai/deer-workflow` (v0.2.x or compatible).
- TypeScript execution or build path available in project.
- For Pi harness: Pi Coding Agent installed, authenticated as needed, and `pi --print` available. `PiAgent` uses ephemeral `pi --print` for text calls and `pi --mode json` for schema-backed calls.
- For Codex or Claude harnesses: corresponding executable installed and authenticated.
- Workspace permissions to read/write generated source and run checkpoints.
- Credentials and network access required by individual Workflow nodes.

## Commands

### `/deer-workflow:design <goal>`
- Input: orchestration goal and optional constraints.
- Action: propose phases, pipelines, parallel branches, agent nodes, retries, timeouts, inputs, outputs, and side effects. Do not execute.
- Output: concise graph plan plus unresolved questions and risk classification.
- Failure: ask for missing input contracts or report that goal cannot be represented safely.

### `/deer-workflow:create <goal>`
- Input: approved design. Ask for destination path when needed; never infer a conflicting existing path.
- Action: write a self-contained TypeScript Workflow using `workflow`, `phase`, `pipeline`, `parallel`, `agent`, and logging APIs as appropriate. Preserve user code; never overwrite an existing file without confirmation.
- Output: file path, source summary, and required dependencies.
- Failure: leave no partial file; report syntax/API uncertainty.

### `/deer-workflow:validate [file]`
- Input: Workflow module file (default: most recently created module).
- Action: inspect imports, graph structure, agent schemas, phase placement, retry/timeout settings, and run project type-check. Check that phase changes occur outside concurrent branches.
- Output: errors, warnings, and pass/fail status.
- Failure: report exact diagnostics and do not run invalid code.

### `/deer-workflow:run [file]`
- Input: validated Workflow file. Ask separately for input, harness, timeout, retry, and checkpoint settings.
- Action: import the module and execute through `WorkflowRunner`; subscribe to `WorkflowRunner.events`; stream compact progress to the session. Show side effects and request confirmation before execution when required.
- Output: run ID, status, outputs, event summary, timings, and checkpoint path.
- Failure: persist observed events, classify node/harness/timeout/credential errors, and provide resume guidance.

### `/deer-workflow:inspect <run-id>`
- Input: persisted run ID.
- Action: read run metadata and event history.
- Output: phase and node status, durations, logs, outputs, failures, and resume point.
- Failure: report missing or corrupt run state without guessing.

### `/deer-workflow:resume <run-id>`
- Input: interrupted or failed run ID.
- Action: verify checkpoint and explicit user approval, then continue from checkpoint with original graph and compatible options.
- Output: continuation run ID and final status/output.
- Failure: explain why checkpoint is incompatible or unavailable; never silently restart from beginning.

### `/deer-workflow:graph [file|run-id]`
- Input: Workflow file or run ID.
- Action: render static graph or runtime execution graph as text/ Mermaid.
- Output: nodes, edges, phases, parallel groups, and current status.
- Failure: report unresolved dynamic branches.

### `/deer-workflow:cancel <run-id>`
- Input: active run ID.
- Action: request cancellation, confirm before terminating side-effecting work, and record final events.
- Output: cancellation status.
- Failure: report if runner cannot cancel safely.

## Operating rules

1. Treat generated source as a reviewable artifact; never execute immediately after create.
2. Use direct package imports and `WorkflowRunner`; CLI `deer-workflow create` is fallback only for scaffolding when API generation is unavailable.
3. Select harness explicitly. `PiAgent` is preferred for a Pi session unless user chooses another.
4. Keep `phase()` transitions outside `parallel()` and `pipeline()` branches when shared context could race.
5. Set bounded timeouts and retries. Do not retry non-idempotent side effects without confirmation.
6. Normalize events into run ID, phase, node, start/end, status, output, and error fields.
7. Persist checkpoints and event history under a project-local, user-approved directory. Do not persist secrets or raw credentials.
8. Redact secrets from logs and summaries.
9. Before run, list filesystem, process, network, deployment, and credential side effects. Require confirmation for destructive or external mutations.
10. On failure, preserve partial state and exact error text; offer inspect/resume rather than blind rerun.

## Reference API

```ts
import {
  agent, log, parallel, phase, pipeline, workflow,
  WorkflowRunner, WorkflowEventEmitter,
} from "@deerwork-ai/deer-workflow";
```

The package also exports focused subpaths (`./agents`, `./events`, `./flow`). Consult installed package typings and `docs/api.md` for exact signatures; do not invent options.

## Safe failure behavior

Never execute unvalidated generated code, bypass confirmation, expose secrets, or claim completion when a harness subprocess fails. If package or executable is missing, provide install/version/login checks. If structured agent output fails schema validation, retain raw event metadata but do not treat text as valid output.

## Credits

- `@deerwork-ai/deer-workflow` project and API documentation: https://github.com/deerwork-ai/deer-workflow
- Pi integration behavior based on Deer Workflow's documented `PiAgent` harness (`pi --print` and `pi --mode json`).
