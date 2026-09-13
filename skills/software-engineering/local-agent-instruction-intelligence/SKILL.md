---
name: local-agent-instruction-intelligence
description: Review session lessons and consolidate a project's local agent-instruction layers into scoped, reviewable policy without promoting tactical details or duplicating advisory guidance.
category: software-engineering
---

# Local agent instruction intelligence

Turn evidence from the current session and the project's instruction files into a
reviewable policy proposal. Find drift across agent-specific entry points, preserve
intentional runtime differences, and keep one source of truth for shared behavior.

Treat analysis, agreement, file mutation, and publication as separate actions. A loaded
skill does not authorize edits. Continue the conversation through proposal and refinement;
write only after the user confirms the final proposal in their language.

## Inputs

Use the active project supplied by the harness. Otherwise use the Git repository root,
then the current working directory. If several roots are plausible, show them and ask the
user to select one. Accept another root when the user names it explicitly; a path is not
required in ordinary use.

Use only session history and runtime instructions visible to the current agent. State the
coverage as `complete`, `compacted`, `partial`, or `unavailable`; never claim to have read
conversation content the harness did not expose.

## Prerequisites

- Read access to the target project and its applicable instruction files.
- Access to the visible conversation and runtime instructions for session analysis.
- A file-search capability for consolidation; Git is optional but useful for root discovery,
  ignore rules, status, and diffs.
- Write access is required only after the user confirms a final proposal.
- Guidance discovery uses only skill/plugin registries and configured roots exposed by the
  current harness. No particular skill, plugin, account, service, package, or script is required.

## Commands

Slash commands are conversational entry points, not a CLI. The words after the skill name
select a mode or modifier. If the harness uses another skill-invocation syntax, interpret
the equivalent natural-language request the same way.

### `/local-agent-instruction-intelligence`

- **Input:** Active project, visible session, and currently applicable instruction layers.
- **Action:** Run session analysis and non-recursive consolidation, then prepare one integrated
  proposal. Read [session-learning.md](references/session-learning.md) and
  [layer-consolidation.md](references/layer-consolidation.md).
- **Output:** Coverage declaration, instruction topology, classified lessons, difference matrix,
  excluded tactical findings, and a minimal proposal.
- **Failure:** Complete every available read-only part and label unavailable evidence; do not
  infer missing history, authority, or policy.

### `/local-agent-instruction-intelligence session`

- **Input:** Visible session and the instruction layers applicable to its project scope.
- **Action:** Read [session-learning.md](references/session-learning.md), extract durable lessons,
  and compare them with current policy. Do not perform a project-wide nested-file scan.
- **Output:** Qualified policy candidates, existing coverage, tactical exclusions, scope, evidence,
  confidence, and proposed destinations.
- **Failure:** Downgrade isolated or ambiguous observations instead of turning them into universal rules.

### `/local-agent-instruction-intelligence session guidance`

- **Input:** Same as `session`, plus guidance sources exposed by the harness and project.
- **Action:** Discover advisory guidance first using
  [guidance-discovery.md](references/guidance-discovery.md), then use relevant readable sources as
  review lenses without copying their rule sets.
- **Output:** The session report plus an advisory-source register showing what influenced the review.
- **Failure:** Continue with the skill's own criteria when no advisory source is available.

### `/local-agent-instruction-intelligence consolidate`

- **Input:** Instruction files at the active project root and documents reached through their pointers.
- **Action:** Read [layer-consolidation.md](references/layer-consolidation.md), build the instruction
  graph, compare meaning across layers, and propose consolidation. Do not descend into every subsystem.
- **Output:** Source-of-truth assessment, layer matrix, intentional differences, gaps, conflicts,
  duplications, weak pointers, orphans, scope leaks, and a proposed topology.
- **Failure:** When canonical authority is ambiguous, present the candidates and ask the user to decide.

### `/local-agent-instruction-intelligence consolidate recursive`

- **Input:** Same as `consolidate`, extended to nested instruction scopes inside the active project.
- **Action:** Perform bounded recursive discovery, model inheritance and overrides for each nested scope,
  and compare each rule only where its scope applies.
- **Output:** A project-wide scope tree and a consolidation matrix partitioned by scope.
- **Failure:** Report excluded or unreadable areas; never promote a nested rule to a broader scope by inference.

### `/local-agent-instruction-intelligence consolidate guidance`

- **Input:** Root-level instruction layers and configured guidance sources.
- **Action:** Run non-recursive consolidation and apply relevant advisory guidance discovered through
  [guidance-discovery.md](references/guidance-discovery.md).
- **Output:** Consolidation report plus advisory provenance and any advisory conflicts.
- **Failure:** Treat unreadable or incompatible guidance as unavailable, not as a failed project policy.

### `/local-agent-instruction-intelligence consolidate recursive guidance`

- **Input:** All nested project scopes and configured guidance sources.
- **Action:** Combine bounded recursive consolidation with advisory discovery. Account for every discovered
  instruction layer once in the scope tree and every used advisory once in the provenance register.
- **Output:** Full scope tree, semantic difference matrix, advisory register, and one bounded proposal.
- **Failure:** Stop the affected branch at permission or access boundaries and complete the remaining branches.

### `/local-agent-instruction-intelligence guidance`

- **Input:** Skill/plugin registries, configured skill roots, project pointers, and relevant validation scripts.
- **Action:** Read [guidance-discovery.md](references/guidance-discovery.md) and inventory available guidance
  for authoring, reviewing, consolidating, or validating agent instruction files. Do not execute discovered scripts.
- **Output:** Advisory-source register with provenance, relevance, accessibility, and intended contribution.
- **Failure:** State which configured sources could not be checked; do not scan unrelated home or disk locations.

### `/local-agent-instruction-intelligence verify`

- **Input:** Current root-level instruction topology and any proposal just applied in this conversation.
- **Action:** Rebuild the non-recursive graph and verify canonicality, pointers, semantic consistency,
  intentional runtime differences, references, and the absence of unintended edits.
- **Output:** Passed, failed, and not-run checks with evidence.
- **Failure:** Verification does not authorize repair; propose corrections through the interaction contract below.

### `/local-agent-instruction-intelligence verify recursive`

- **Input:** Current instruction topology across all discovered project scopes.
- **Action:** Apply the same verification to the bounded recursive scope tree, including inheritance and overrides.
- **Output:** Verification results by scope and an aggregate gap list.
- **Failure:** Do not call the project verified when a relevant scope could not be inspected.

## Common workflow

1. Establish the active root, selected mode, visible-session coverage, and read/write boundaries.
2. Inventory the relevant instruction layers before judging individual rules.
3. Separate observed evidence from interpretation and recommendation.
4. Compare rules by meaning, scope, authority, and behavioral effect rather than text alone.
5. Route common stable policy to a declared canonical source; preserve runtime-specific behavior in
   its adapter and branch-specific detail behind a precise pointer.
6. Route discoverable operational facts to configuration or scripts, decisions and rationale to ADRs
   or documentation, and temporary work to task records. Recommend these destinations without creating
   those artifacts unless the user asks.
7. Present the smallest proposal that resolves supported gaps. Include exact intended files and edits,
   open questions, exclusions, and validation.
8. Always end a proposal containing changes by asking, in the user's current language, whether they want
   to change anything or confirm it. Explain that they may confirm with `apply`, `aplique`, or an equivalent
   unambiguous phrase in that language. These are examples of intent, not magic tokens.
9. Refine until the user confirms. Every revision replaces the previous proposal. If there is no proposed
   change, report that result without asking for confirmation of an empty patch.
10. After confirmation, re-read every target, detect drift, and apply only the confirmed proposal. Material
    drift invalidates the proposal: show the revised patch and ask again. Then verify all changed scopes and
    report exact outcomes. Do not commit, push, publish, deploy, install, or activate anything unless separately
    authorized.

## Policy boundaries

- A filename alone does not establish authority. Use explicit pointers, harness configuration, scope,
  and operator decisions to identify a canonical source.
- Treat `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `CODEX.md`, `AGY.md`, `GROK.md`, `AGI.md`, `CLOUDS.md`,
  equivalent harness entry points, and their case variants as candidates only when present or configured.
- Prefer thin runtime adapters pointing to common policy. Preserve a local rule when the runtime genuinely
  requires different behavior; consolidation is semantic alignment, not byte identity.
- Keep narrower nested instructions in their scope. Do not lift them to the project root without evidence
  that they apply project-wide.
- Treat runtime/system instructions as evidence of the current operating context, not automatically as
  project-owned policy. Never copy provider policy, private conversation, secrets, or raw transcripts into
  a repository.
- A single correction, success, or failure is a candidate lesson. Require durability, recurrence or strong
  consequence, appropriate scope, and a behavior-changing formulation before recommending permanent policy.
- Preserve unrelated and user-authored content. Show conflicts instead of silently choosing a winner.
- Use detected guidance as optional advice with provenance. Do not duplicate its rule set, require its
  installation, invoke its mutating behavior, or let it override project policy or explicit user instructions.

## Credits

- Information hierarchy, context pointers, single-source-of-truth pruning, and no-op analysis are adapted
  from the locally supplied `writing-for-agents` guidance. That skill is optional and is not redistributed.
- Skill structure and progressive-disclosure choices are informed by OpenAI's `skill-creator` guidance.

Maintainers can exercise the scenarios in [evals.md](checklists/evals.md) without changing a live project.
