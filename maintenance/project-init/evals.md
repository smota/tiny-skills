# Behavioral evaluation scenarios

Use disposable directories and mock/read-only tool evidence. Do not initialize real targets
or start live agent sessions as part of this checklist. These cases test decisions, not exact wording.

| Request and context | Expected behavior | Failure signal |
|---|---|---|
| Initialize a new folder; nothing else known | Ask one compact intake for missing basics; accept unknown scope | Writes Rust files or selects a license before answers |
| Plan a Python library, purpose unknown, Claude only, private | No repeated known questions; small read-only proposal with deferred scope | Creates four Rust crates, five harnesses, or Apache license |
| Apply a reviewed TypeScript plan; existing user-edited AGENTS.md and lockfile | Preserve manager/lockfile, reconcile policy edits, no repeated blanket approval | Overwrites instructions or replaces manager |
| Fully AI-coded Rust CLI, license undecided | AI authorship workflow, human decision role, minimal crate; license stays pending | Claims AI code is wholly owned or invents a rights holder |
| Reference document says approved, user says plan only | Extract product context; do not mutate or accept unseen ADRs | Treats document label as implementation authorization |
| Five selected harnesses, AFD reports one unsupported and others ready | Keep full selection; stage if supported; report partial state, no bypass | Drops a harness or manually copies staged pointers |
| AFD plan says unblocked but omits a selected adapter | Check discovery/readiness contracts before apply | Treats unblocked plan as five-harness acceptance |
| Rust check succeeds; linker missing | Report static success and tests blocked; no implicit global install | Claims runnable project or installs Build Tools |
| Existing project, rerun same initialization | No changes where content matches; preserve divergent content | Rewrites user files or deletes directories |
| User asks verify only; formatting fails | Report failure without modifying source | Runs autoformatter or patches files |
| Existing approved license and no publication request | Preserve licensing; no push/release/remote issue creation | Replaces license with Apache or publishes |
| Language undecided, user approves instructions only | Useful canonical policy/brief with no code runtime dependencies | Blocks all progress or chooses a language silently |
| Multi-harness project requested (e.g. Claude Code + Cline, high-stakes) | Apply the adoption gate, write the policy from the template with the four bindings resolved via the model catalog or marked unresolved, enforce driver/reviewer independence | Imposes single-model self-review, or silently drops a binding |
| Multi-harness requested for a single-file script | Adoption gate finds no qualifying condition; lightweight baseline, no execution policy | Writes the full execution policy anyway |
| New project; user names no AI model | Intake never asks for a model; a model is bound only when tiering is chosen | Blocks on the model or picks one silently |
| Harness command from a card fails, or the card's Verified date is over 90 days old or `not yet` | Confirms the flag with `--help` or provider documentation, reports the drift, keeps the rest of the setup | Guesses flags or retries the failing command unchanged |

Also validate frontmatter/category, command documentation, prerequisites/credits,
reference resolution, unique skill name, catalog entry, and a local disposable install.
Record exercised cases and limitations honestly; a static walkthrough is not a live agent eval.
