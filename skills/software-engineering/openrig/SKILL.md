---
name: openrig
description: "Operate and orchestrate OpenRig agent fleets via direct CLI commands and slash commands: audit fleet health (/openrig-fleet), dispatch durable queue tasks (/openrig-dispatch), unblock stalled seats (/openrig-unblock), apply watchdog alignment (/openrig-watchdog-align), or execute seat handovers (/openrig-handover)."
category: software-engineering
---

# OpenRig

## Purpose

Operate, inspect, and coordinate OpenRig agent topologies, seats, and daemon infrastructure. Provide a comprehensive reference for native `rig` CLI commands alongside high-level composite workflows that supervise tasks, resolve interactive blockers, conduct fleet health audits, ensure watchdog alignment, and execute safe seat handovers.

This skill functions as an outside-in fleet supervision and control plane. It operates cleanly alongside internal seat-level skills (such as `queue-handoff`, `mission-slice-sop`, and `openrig-user`) by providing external observability, intervention, and dispatch without dictating internal in-seat task implementation.

## Prerequisites

- OpenRig CLI installed and accessible in `$PATH` (`rig` executable, version >= 0.6.0). Run `rig --version` to verify.
- Running OpenRig local daemon (`rig daemon status` or `rig daemon start`).
- Standard Linux/macOS host with `tmux`, `node` (>= 22), and SQLite3 CLI tools.
- Read/write access to OpenRig local workspace and daemon state directories (typically `~/.openrig`).
- Active agent authentication profiles configured for target runtimes (e.g. Claude Code, Codex, Pi).

## Credits

- Built for and based on the OpenRig local control plane CLI (`rig`), developed by [mvschwarz/openrig](https://github.com/mvschwarz/openrig).
- Incorporates and formalizes operational patterns from canonical OpenRig in-seat skills:
  - `openrig-user` (CLI command surface, flag semantics, and safety defaults).
  - `queue-handoff` (L3 durable task custody and handoff chains).
  - `refocusing` and `watchdog` (the 3-level intervention doctrine: wake, refocus, and alignment checkpoint).
  - `seat-continuity-and-handover` and `rig-lifecycle` (successor handover procedures and the restore-honesty rule).

## Commands

The high-level slash commands compose multiple low-level `rig` primitives into safe, transactional, and observable operational workflows.

### `/openrig-fleet [rig-id]`

- **Input:** Optional `rig-id` to filter a specific topology, or omit to audit the entire local host fleet.
- **Action:**
  1. Inspect daemon connectivity via `rig daemon status` and run-directory database integrity (`PRAGMA integrity_check`).
  2. Execute `rig doctor` non-destructively to verify system readiness, port bindings, and provider credentials.
  3. Query active topologies and nodes via `rig ps --full --json`.
  4. Identify stopped or attention-owed seats using `rig parked`.
  5. Check pending and in-flight work queues using `rig queue list -a`.
- **Output:** Structured diagnostic summary outlining daemon status, active rigs, node health matrix (alive/idle/held/attn), stuck queue counts, and any recommended remediation steps.
- **Failure:** If the daemon is unreachable, runs `rig crash-cart` to output the recovery verdict as JSON without mutating state.

### `/openrig-dispatch <seat@rig> <task-file-or-text>`

- **Input:** Target seat reference `<seat@rig>` and the task description string or path to a markdown/text task specification file.
- **Action:**
  1. Verify target seat exists and is running/idle using `rig ps --nodes --rig <rig>`.
  2. Create a durable task record in the L3 coordination queue via `rig queue create --destination <seat@rig> --body-file <file>` (or inline text).
  3. Extract the created queue task ID.
  4. Notify the target seat inside tmux by sending `rig send <seat@rig> "task <task-id> is yours"`.
  5. Capture the initial seat screen output via `rig capture <seat@rig>` to confirm receipt and verify the seat does not crash or stall at an interactive prompt.
- **Output:** Confirmation containing task ID, target seat verification, initial screen capture snippet, and instructions on how to track progress.
- **Failure:** If the seat is not in `running` state or is already claiming uncompleted work, reports the conflict and refuses dispatch without explicit operator override.

### `/openrig-unblock <seat@rig>`

- **Input:** Target seat reference `<seat@rig>` that is stalled, parked, or marked with `ATTN > 0`.
- **Action:**
  1. Capture the current terminal buffer using `rig capture <seat@rig>`.
  2. Classify the blocking condition into one of:
     - **Interactive Menu / Selection:** Seat waiting for numeric/arrow key choice.
     - **Confirmation Prompt:** Seat waiting for `y/n` or confirmation phrase.
     - **Runner / Runtime Error:** e.g. `MALFORMED_FUNCTION_CALL`, missing thought signatures, or tool schema failure.
     - **Authentication / Quota Refusal:** Expired token, login required, or provider rate limit.
     - **Deadlock / Stale Idle:** Process exited or hanging without active tool execution.
  3. Formulate the required input sequence (e.g. Escape, Enter, specific option key, or confirmation text) and transmit using `rig send <seat@rig> "<key/text>"`.
  4. Capture terminal buffer again to confirm resolution.
- **Output:** Classification of the blockage, input sent, and before/after screen verification. If the issue is an environmental or credential failure, escalates to the operator with actionable diagnostic details.
- **Failure:** Does not kill or abort tmux sessions automatically. If unblock attempts fail after 2 captures, flags the seat for manual operator inspection.

### `/openrig-watchdog-align <seat@rig> [wake|refocus|checkpoint]`

- **Input:** Target seat reference `<seat@rig>` and desired intervention level (`wake`, `refocus`, or `checkpoint`). Defaults to `wake` if idle, or `refocus` if drifting.
- **Action:**
  1. Inspect seat activity telemetry and recent queue state via `rig telemetry` and `rig queue list --destination <seat@rig>`.
  2. Apply the OpenRig 3-level intervention stack rules:
     - **`wake` (Liveness Nudge):** Prompts the seat to resume motion without altering its current workstream context.
     - **`refocus` (Alignment Nudge):** Instructs the seat to "finish current action first", reiterates role boundaries and current approved goals, and reminds of stop conditions.
     - **`checkpoint` (Alignment Checkpoint):** Requests a deliberate pause at a milestone or phase seam to reconstruct the shared state before proceeding.
  3. Deliver the formatted intervention message via `rig send <seat@rig> "<message>"`.
  4. Monitor with `rig capture <seat@rig>` to ensure the seat does not treat the refocus text as a new contradictory goal.
- **Output:** Level of intervention applied, dispatched message, and observed seat acknowledgment.
- **Failure:** Refuses intervention if the seat is actively writing code or generating output (prevents cadence pollution and bureaucracy theater).

### `/openrig-handover <source-seat@rig> <target-seat@rig>`

- **Input:** Current owner seat `<source-seat@rig>` and the successor seat `<target-seat@rig>`.
- **Action:**
  1. Snapshot durable state and verify working tree clean status on the source seat.
  2. Reassign pending and owned L3 tasks in `rig queue` from the source seat to the target seat.
  3. Deliver accumulated context and latest handoff summary to the target seat.
  4. Verify continuity and startup compliance on the target seat using `rig whoami` and `rig startup-proof`.
  5. Gracefully unbind or unclaim the source seat session using `rig unclaim` without destroying tmux history.
- **Output:** Handover manifest listing reassigned task IDs, context packet verification, and the verified status of the successor seat.
- **Failure:** Stops and halts handover if the target seat fails startup-proof verification or rejects the context packet.

---

## Direct Command Reference (Original `rig` CLI Surface)

The complete matrix of native `rig` CLI commands organized by functional operational domain. These commands are directly usable during agent and operator sessions.

### 1. Daemon & Infrastructure Control

| Command | Usage & Arguments | Description |
|---|---|---|
| `rig daemon status` | `rig daemon status [--json]` | Check if local daemon is running, inspect PID and listening port. |
| `rig daemon start` | `rig daemon start` | Start the local control-plane daemon (auto-launches kernel rig). |
| `rig daemon stop` | `rig daemon stop` | Gracefully shut down the daemon and save state snapshots. |
| `rig doctor` | `rig doctor [--fix]` | Run health checks on dependencies, paths, ports, and runtimes. |
| `rig preflight` | `rig preflight` | Check system requirements (Node, tmux, SQLite) before launch. |
| `rig crash-cart` | `rig crash-cart [--json]` | Read-only diagnostic dump when daemon is crashed or unreachable. |
| `rig config` | `rig config [get\|set] <key> [value]` | Inspect or modify OpenRig local configuration settings. |

### 2. Fleet & Topology Observability

| Command | Usage & Arguments | Description |
|---|---|---|
| `rig ps` | `rig ps [--all\|--nodes\|--rig <name>\|--json]` | List running rigs, node counts, uptime, and attention flags. |
| `rig status` | `rig status [rig-id]` | Show detailed status of a specific rig or overall system. |
| `rig parked` | `rig parked [seat]` | Detect stopped seats owing uncompleted work or held leases. |
| `rig whoami` | `rig whoami [--json]` | Show current managed identity and assigned topology node. |
| `rig usage` | `rig usage [--rig <name>\|--top <N>]` | Display token telemetry and consumption series across seats. |
| `rig telemetry` | `rig telemetry [--page <N>]` | Read retained execution metadata and session events. |
| `rig health` | `rig health` | Inspect read-only explainable health records and warnings. |

### 3. Messaging, Terminal & Interactive Control

| Command | Usage & Arguments | Description |
|---|---|---|
| `rig send` | `rig send <sessionRef> "<text>"` | Type keystrokes, text, or escape sequences into an agent's terminal. |
| `rig capture` | `rig capture [options] <sessionRef>` | Read recent terminal output screen lines from an agent session. |
| `rig broadcast` | `rig broadcast "<text>" [--rig <rig>]` | Send an urgent notice to multiple active agent sessions. |
| `rig terminal open` | `rig terminal open <sessionRef> [--window]` | Open desktop terminal window/tab or attach via tmux/Herdr. |
| `rig transcript` | `rig transcript <sessionRef> [--tail <N>]` | Read raw model/agent conversation transcript history. |
| `rig ask` | `rig ask <rig> "<question>"` | Query rig transcript history with a natural language prompt. |
| `rig chatroom` | `rig chatroom [options]` | Enter interactive multi-seat chat room for rig communication. |

### 4. Work Coordination & Queues (L1–L3)

| Command | Usage & Arguments | Description |
|---|---|---|
| `rig queue list` | `rig queue list [-a] [--destination <seat>]` | List coordination tasks by destination seat, status, or lifecycle. |
| `rig queue show` | `rig queue show <taskId> [--full]` | Display complete task specification, payload, and handoff chain. |
| `rig queue create` | `rig queue create --destination <seat> --body-file <f>` | Create a durable owned-work task in the daemon queue. |
| `rig stream` | `rig stream [append\|read\|tail]` | L1 append-only intake stream for event ingestion. |
| `rig project` | `rig project [list\|claim\|release]` | L2 classifier work items with daemon leases and timeouts. |
| `rig view` | `rig view [name]` | L5 daemon-backed state views over coordination entities. |
| `rig watchdog` | `rig watchdog [status\|eval\|trigger]` | Inspect or evaluate watchdog policies, reminder gates, and idle limits. |
| `rig workflow` | `rig workflow [run\|status\|step]` | Inspect or step declarative daemon-native workflow state machines. |

### 5. Topology Lifecycle & Seat Scaling

| Command | Usage & Arguments | Description |
|---|---|---|
| `rig up` | `rig up <spec\|bundle>` | Launch a rig topology from a specification file or library entry. |
| `rig down` | `rig down <rig-id>` | Tear down a running rig topology and unbind associated seats. |
| `rig snapshot` | `rig snapshot <rig-id>` | Capture a point-in-time state snapshot of a running rig. |
| `rig restore` | `rig restore <snapshot-file>` | Restore a rig topology from a saved snapshot (enforces honesty rule). |
| `rig grow` | `rig grow <rig-id> <member-specs...>` | Add one or more seats dynamically to an active rig. |
| `rig shrink` | `rig shrink <rig-id> <pod-ref>` | Remove a pod or seat from a running rig. |
| `rig unclaim` | `rig unclaim <sessionRef>` | Release an adopted session from control without killing its process. |
| `rig release` | `rig release <rig-id>` | Release all claimed sessions in a rig without killing tmux sessions. |
| `rig archive` | `rig archive <rig-id>` | Soft-hide an inactive rig while preserving all logs and state. |
| `rig unarchive` | `rig unarchive <rig-id>` | Return an archived rig to active view. |

### 6. Agent Continuity, Context & Specialization

| Command | Usage & Arguments | Description |
|---|---|---|
| `rig handover` | `rig handover <seat>` | Guided seat successor sequence: create -> context -> continuity -> rebind. |
| `rig context get` | `rig context get <pack-name>` | Retrieve an operator context pack or reference document. |
| `rig context list` | `rig context list` | List available context packs and reference manuals in the library. |
| `rig walk` | `rig walk <seat>` | Walk a seat step-by-step through a paced sequence of context files. |
| `rig compact` | `rig compact <session>` | Run guided compaction flow: prep -> /compact -> restore -> audit. |
| `rig compact-plan`| `rig compact-plan` | Audit context windows to identify candidates needing compaction. |
| `rig restore-packet`| `rig restore-packet [generate\|read]` | Export or inspect cross-runtime agent restore packets (v0 format). |
| `rig agent-image` | `rig agent-image [list\|snapshot]` | Manage agent images and context base layers. |
| `rig fork` | `rig fork <source-session>` | Fork a live seat's active context into a new parallel seat. |
| `rig startup-proof`| `rig startup-proof [submit\|inspect]` | Verify that an agent completed role orientation and startup checklist. |

---

## Operating Behavior & Safety Principles

1. **Restore-Honesty Rule:** A failed restore or resume is treated as `FAILED` loudly. Never fall back silently to a fresh, unprimed session when state or history was expected.
2. **Non-Destructive Inspections:** Diagnostic commands (`status`, `ps`, `capture`, `doctor`, `telemetry`, `crash-cart`) never mutate running processes or alter files.
3. **No Blind Sends:** Never send instructions or keys to a seat via `rig send` without first inspecting current state via `rig capture` when the seat is not known to be idle.
4. **Queue-First Delivery:** Work delegation is recorded through durable queues (`rig queue create`) so tasks survive crashes, restarts, and reboots. Keystrokes via `rig send` inform and nudge, but durable queue items define ownership.
5. **Cadence Discipline:** Watchdog interventions must adhere to the 3-level stack (wake, refocus, alignment checkpoint) and must never interrupt an agent currently producing output.
