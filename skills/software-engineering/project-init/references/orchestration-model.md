# Multi-Harness and Multi-Model Execution Model

A disciplined governance framework for multi-agent, multi-harness, and tiered-model engineering. When adopted, resolve the four project placeholders (`[FILL 1]` through `[FILL 4]`) during project planning. A template with blank placeholders is non-functional; these bindings connect the abstract model to concrete repository reality.

## 0. Adoption Gate: Does this project need this?

This model carries real coordination overhead. It pays for itself only when at least one condition holds:

- **Irreversible decisions:** Published data formats, external API contracts, database schemas, or wire protocols.
- **Cross-session continuity:** Work spans multiple sessions and context must outlive individual executor lifecycles.
- **Verification exceeds test suites:** Correctness invariants cannot be fully captured by tests alone (concurrency, process semantics, cross-platform portability).
- **Evidence-heavy verification:** Empirical measurements must be independently audited to confirm they are not right for the wrong reasons.

If none apply — single-file scripts, disposable prototypes, or routine mechanical refactors — **do not adopt this model**. Keep the baseline lightweight.

## 1. Principles

1. **Separation of powers:** The implementer never reviews their own work.
2. **Reviewer independence:** The reviewer operates in an independent harness, never as a subagent of the implementer.
3. **Escalation on evidence:** Tier promotions occur only upon concrete unresolved defects, never out of vague caution.
4. **No silent substitution:** The executed model and harness are always explicitly declared in delivery records.
5. **Deterministic work uses no model:** A script, compiler, or test gate decides faster, reliably, and at zero token cost.

## 2. Roles

| Role | Core Function | Produces | Prohibited From |
|---|---|---|---|
| `oracle` | Deterministic verification | Pass/fail verdict | Exercising open subjective judgment |
| `scout` | Context reading, code inventory | Facts with `file:line` | Proposing architecture or broad redesigns |
| `driver` | Implements specifications | Diff + unit/regression tests | Deciding open architectural ambiguities |
| `reviewer` | Independent adversarial audit | Concrete, reproducible defects | Modifying source code directly |
| `arbiter` | Resolves disputes, decides open design | Authoritative recorded decision | Implementing production code |

**Hard rule:** `driver` and `reviewer` MUST NOT share the same harness or subagent lineage for the same delivery. Shared lineage breeds correlated errors: an implementer reviewing their own work repeats the mental blind spot that caused the defect, and child subagents inherit their parent's premises.

## 3. Tiers

| Tier | Name | Work Nature | Primary Focus |
|---|---|---|---|
| **T0** | `deterministic` | Native builds, test suites, linters, formatters, hashes, metrics | Zero LLM usage. Local scripts and compiler commands. |
| **T1** | `mechanical` | Inventory, grep/search, context extraction, edits under exact spec | Fast, cost-efficient models with high context efficiency. |
| **T2** | `standard` | Implementation from spec, test writing, standard refactoring | High-discipline coding models. Daily engineering workhorse. |
| **T3** | `judgment` | Open architecture, ambiguous tradeoffs, cross-cutting invariants | Frontier reasoning models. Critique before code. |

**`[FILL 1]` — Tier-to-Model Mapping:** Resolve available models to tiers using [model-catalog.md](model-catalog.md). Verify current pricing and API IDs at primary provider sources before establishing budgets. Do not infer rates across providers or rely on memorized pricing.

## 4. Cost Lever Hierarchy

Routing by model tier is the **second** cost lever, not the first. Two counterintuitive properties govern LLM cost dynamics:

1. **Prompt caches are model-scoped:** Cascading between different model families forfeits cache reuse. Rereading large repository context across tiers can exceed the token price difference.
2. **Unit of cost is the completed task, not the request:** A cheap model that requires three iterations or produces diffs rejected by the reviewer costs more than a capable model that succeeds on the first attempt.

| Priority | Lever | Prerequisite before advancing |
|---|---|---|
| 1 | Eliminate models (T0) | Convert every deterministic check into a runnable command. |
| 2 | Context hygiene | Feed the agent bounded, relevant slices rather than whole trees. |
| 3 | Effort level tuning | Verify that lower reasoning/thinking effort retains quality. |
| 4 | Tier substitution | Measure that the cheaper tier reliably completes the task. |
| 5 | Cross-harness | Adopt only when purchasing true reviewer independence. |

*Corollary:* Before introducing a model cascade, test the primary model at lower effort. Single-model caching is frequently cheaper per completed task.

## 5. Execution Modes

### Mode A — Cross-Harness
- **Mechanism:** Separate contexts, distinct agent harnesses, independent model families.
- **Value:** Buys true independence. The reviewer inherits neither context windows, prompt instructions, nor vendor blind spots. Arbitrates quota across distinct provider pools.
- **Cost:** High coordination overhead. Nothing is implicit; context transfer must be fully documented.
- **Use when:** The primary failure mode is **correlated error**.

### Mode B — Single-Harness Cross-Model
- **Mechanism:** Subagents across different tiers within a single harness; shared memory or task dispatch.
- **Value:** Buys token economy. Fan-out context reads in T1, synthesis in T2/T3.
- **Cost:** Shared context windows risk shared blind spots; inter-tier transitions lose prompt cache reuse.
- **Use when:** The primary failure mode is **token cost**, not verification bias.

> **Cross-harness when you require independence. Cross-model when you require economy.**
>
> Never cross-harness solely for cost savings — coordination overhead dwarfs token savings.
> Never rely on cross-model subagents for critical verification — shared context is not independent.

*Composition:* Use Mode B inside each harness for mechanical reading, and Mode A between the `driver` and the `reviewer`.

## 6. Allocation Principles

**High-tier models (T3) touch only work where errors are both costly AND difficult to detect.**

A published contract qualifies: errors survive peer review and fix costs compound with downstream adoption. Conversely, complex implementations that are thoroughly covered by tests do not qualify: bugs trigger deterministic gates immediately.

*Counterintuitive consequence:* High-risk but immediately detectable code warrants lower tiers than lower-risk but silent, invisible invariants.

### Key Patterns:
- **T3 before code, never after:** For any contract (schema, API protocol, wire format), draft, challenge, and lock the specification in prose before authoring code. Changing prose costs zero; changing implemented code fights sunk-cost bias.
- **Convert T2 to T0:** When an invariant can be asserted deterministically ("outputs are byte-identical", "both implementations agree"), write that test. Paying a model once to create a T0 test permanently removes models from that verification path.

## 7. Operational Rules

1. **Exclusive Resource Ownership:** Only one active writer per shared resource.
   > **`[FILL 2]`** — Document assigned working trees, ports, build locks, and test service instances.
2. **Authority of the Gate:** No role can declare green without deterministic verification.
   > **`[FILL 3]`** — Exact test, lint, and build commands that hold final authority.
3. **Declared Harness Roster:**
   > **`[FILL 4]`** — List active harnesses (e.g. Pi CLI `pi.dev`, Claude Code, Cursor, Cline, OpenCode, Codex, Agy) and the canonical `driver`/`reviewer` pairing. Consult [harness-parameters.md](harness-parameters.md) for direct invocation commands and parameter rules.
4. **Escalation on Evidence:** Raising tier requires citing a concrete reproducible failure — never vague difficulty. Downgrading tier requires measured completion rates.
5. **Bounded Attempts:** Declare maximum retry attempts upfront. Repeated failure without a new hypothesis indicates a need to stop and escalate to `arbiter`.
6. **Surface-Separated Evidence:** Local sandbox passes do not prove behavior in target staging or release environments.

## 8. Mandatory Delivery Declaration

Every commit, pull request, or task handoff operating under this model must include this declaration:

```yaml
stream:     <work identifier>
item:       <task number or name>
role:       scout | driver | reviewer | arbiter | oracle
harness:    <which harness executed this task>
tier:       T0 | T1 | T2 | T3
model:      <exact provider model identifier>
escalation: no | <concrete defect motivating tier escalation>
gates:      <verdict of each T0 gate command>
```

The `escalation` field enforces discipline: promoting tiers without naming the concrete defect is how costs silently inflate.

## 9. Honesty About Operational State

Until a project systematically tracks **cost per completed task by tier against reviewer acceptance rate**, tier allocations remain declared hypotheses. A tier that appears cheap per token request is the most expensive in practice if its diffs are repeatedly rejected during independent review.
