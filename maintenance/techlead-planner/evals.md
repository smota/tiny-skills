# Behavioral evaluation scenarios

Use a disposable project with a small codebase. Judge behavior and artifacts, not exact wording. These cases test decisions; a static walkthrough is not a live agent eval.

| Request and context | Expected behavior | Failure signal |
|---|---|---|
| `/techlead-planner` for a typo fix or a rename | A one-paragraph plan: the change, the check that proves it, done | The full nine-step ceremony with slices and an NFR table |
| Goal adds a module with authentication and a schema change | Full workflow; assumptions get extra scrutiny; security, data, and operability marked *applies* with targets or decisions | Skips the non-functional pass, or marks security *not applicable* |
| Ambiguous requirement where a wrong answer would discard work | At most three blocking questions, each with a recommended default; stops at step 2 | Open-ended questions, more than three, or continues to the breakdown |
| Test framework, language version, and lint rules are discoverable in the repo | Reads them, cites the paths, asks nothing about them | Asks the user for facts the repository contains |
| The codebase contradicts itself (two conflicting conventions) | Raises the contradiction and states which it assumes | Silently picks one |
| Draft breakdown where a slice depends on a later slice | Reorders or flags it; every non-forced position has a rationale | Keeps the ordering cycle |
| Irreversible schema migration | Stages expand, migrate, contract, with a rollback per step or an explicit no-rollback decision | One-step migration with no rollback stated |
| Task has no user interface | Usability and accessibility marked *not applicable*, with the reason | Blank, or an invented accessibility target |
| A new use case imports a framework type | Flags the outward dependency and names the inversion | Approves the import |
| Change adds a public API field | Compatibility window and consumer impact stated; ADR marked if the contract is hard to reverse | No compatibility statement |
| `/techlead-planner review` on a plan with "the code should be maintainable" and no acceptance checks | Findings by severity; rewrites the assumption as falsifiable and adds checkable done conditions | A summary or praise without corrections |
| Plan for a goal with three slices | Each slice has a goal condition with one end state, a check whose output will be shown, constraints, the assumptions that stop the run, and a turn limit | Conditions like "the feature works", or a check the evaluator cannot see |
| User answers "yes" after the plan | The plan is final; the skill has created and changed nothing | Starts implementing or writes files |
| A repository area is unreadable | Labels the evidence unavailable and adds an assumption | Invents facts about the area |

Also validate frontmatter and category, that `disable-model-invocation` is set, command documentation, prerequisites and credits, reference resolution, unique skill name, catalog entry, and a local disposable install.
