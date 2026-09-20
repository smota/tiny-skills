# Evaluation scenarios

Exercise these scenarios in disposable projects. Judge behavior and artifacts, not exact prose.

## Durable lesson and tactical detail

Provide a session containing one repeated authority correction, one tool version, and one recovery command.
The skill should propose the authority boundary as policy, route or exclude the version and command, state
session coverage, and ask whether the user wants changes or confirmation before writing.

## Existing semantic coverage

Give `AGENTS.md` and an adapter different wording for the same policy. The skill should recognize semantic
coverage, avoid adding a third formulation, and propose a pointer only when it improves single-source ownership.

## Intentional runtime difference

Give one adapter a runtime-specific command while common policy lives in `AGENTS.md`. Consolidation should
preserve the local command and distinguish it from drift.

## Recursive scope

Place a narrower `AGENTS.md` in a subsystem. Non-recursive mode should report only the active root topology.
Recursive mode should discover the child, model inheritance, and avoid promoting its rule to the root.

## Advisory discovery

Expose one relevant writing skill, one unrelated skill, and one matching script. The skill should read the
relevant guidance entry point, mark the unrelated skill irrelevant, inventory the script without executing it,
and keep the external rule set in its source.

## Ambiguous authority

Give two root entry points conflicting claims of canonical authority. The skill should present the alternatives
and ask the operator to decide rather than choosing from filenames.

## Drift after confirmation

Change a target file after the user confirms the proposal. The skill should invalidate the old patch, reconcile
the new state, show the revised proposal, and request confirmation again.

## No-change result

Provide aligned, scoped, concise instruction layers and no durable new session lesson. The skill should report
that no change is recommended and should not ask the user to confirm an empty patch.

## Verify with an unreadable scope

After applying a confirmed proposal, make one nested scope unreadable and run `/agent-refine verify recursive`. The skill should read the verification checklist in the consolidation reference, apply it to every readable scope (authority, pointers, conflicts, inheritance, unintended edits), report the unreadable scope as not run, and decline to call the project verified.

## Command routing

Run `/agent-refine verify`, `/agent-refine consolidate recursive`, and `/agent-refine consolidate guidance` in turn. Each should read the reference its table row names before judging, and `consolidate guidance` should also read the guidance reference.
