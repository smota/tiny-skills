# tiny-skills

Self-contained, production-ready agent skills repository.

Each directory under `skills/` is an independent agent. Skills are grouped by class for discovery, while remaining fully independent. Agents do not depend on, import, or coordinate with other agents in this repository. Every agent follows the Agent Skill standard and can be installed directly with:

```bash
npx skills add smota/tiny-skills --skill <skill-name>
```

## Skill catalog

Skills listed here. Each skill's own `SKILL.md` is authoritative for detailed usage.

| Class | Skill | Purpose | Prerequisites | Install |
|---|---|---|---|---|
| software-engineering | [empirical-refinement-loop](skills/software-engineering/empirical-refinement-loop/) | Run bounded, reviewed refinement cycles with comparable evidence and repository-backed continuity | Project read/write access, native test/measurement tools, and an independent subagent or configured reviewer CLI for reviewed execution | `npx skills add smota/tiny-skills --skill empirical-refinement-loop` |
| software-engineering | [git-deliver](skills/software-engineering/git-deliver/) | Commit and push task-owned work, optionally integrate into the parent branch, and assess multi-agent worktrees | Git, repository access, commit identity, remote credentials for pushes, and project validation tools | `npx skills add smota/tiny-skills --skill git-deliver` |
| software-engineering | [local-agent-instruction-intelligence](skills/software-engineering/local-agent-instruction-intelligence/) | Distill session lessons and consolidate scoped agent-instruction layers with optional recursive and advisory-guidance review | Project read access and visible session context; write access only for confirmed changes | `npx skills add smota/tiny-skills --skill local-agent-instruction-intelligence` |
| software-engineering | [project-init](skills/software-engineering/project-init/) | Initialize project practices through a short intake, canonical instructions, ADRs, stack-aware validation, and optional multi-harness model tiering | Read/write access; selected toolchain for code; optional AFD and agent CLIs | `npx skills add smota/tiny-skills --skill project-init` |
| writing | [release-notes](skills/writing/release-notes/) | Write value-led technical notes, user-facing release notes, and release announcements from selected commits, with flexible focus and presentation | None for supplied commit output; Git and repository read access for collection; optional hosted-source read access | `npx skills add smota/tiny-skills --skill release-notes` |

## Empirical refinement quick start

Use `/empirical-refinement-loop init [path]` to connect existing engineering
documentation and agree where missing guidance belongs. The compact
`.empirical-refinement-loop/state.json` index points to that documentation and
tracks progress across conversations; internal document storage is also an option.

Use `/empirical-refinement-loop plan [scope]` for a read-only proposal,
`/empirical-refinement-loop run [scope] [rounds=N]` for bounded execution, and
`/empirical-refinement-loop resume` to revalidate state and continue. These are
conversational commands. Reviewed execution uses a real independent reviewer;
commits and pushes require their own delivery scope. See the
[skill documentation](skills/software-engineering/empirical-refinement-loop/SKILL.md).

## Git delivery quick start

Use `/git-deliver` to commit and push the current task, `/git-deliver-merge [parent]`
to also merge and push the parent branch, or `/git-deliver-audit` for an inspection
without mutations. These are conversational commands; equivalent prose works.
The standard workflow proceeds within the command's authorization. Mixed changes,
uncertain parent branches, and concurrent writers receive a concrete scope review.
Worktree orphan candidates are reported for review; delivery does not delete them.
See the [skill documentation](skills/software-engineering/git-deliver/SKILL.md).

## Release communication quick start

Use `/release-notes technical`, `/release-notes release`, or `/release-notes announce`
followed by a commit selection and conversational preferences. `/release-notes` defaults
to user-facing release notes. These are conversational entry points, not CLI flags;
use equivalent prose if your harness does not register slash commands.

```text
/release-notes release v1.0.0..v1.1.0
For operators, in English, with icons. Focus on reliability.

/release-notes technical v1.0.0..v1.1.0
Without icons. Structure: behavior changes, compatibility, validation.

/release-notes announce v1.0.0..v1.1.0
For LinkedIn, plain text, up to 180 words.
```

All modes use selected commits as their factual basis. Optional context and highlights
guide emphasis; audience, language, length, structure, and presentation remain flexible.
See the [skill documentation](skills/writing/release-notes/SKILL.md) for evidence boundaries,
prerequisites, and failure behavior. Generating text does not publish it.

## Project initialization quick start

Install `project-init` to plan or apply an engineering baseline for a new or existing project:

```bash
npx skills add smota/tiny-skills --skill project-init
```

In your agent session, use `/project-init --plan [path]` for a read-only intake and proposal,
`/project-init --apply [path]` to apply reviewed choices within your authorization, or
`/project-init --verify [path]` to check an existing baseline. `/project-init [path]` combines
intake and initialization when authorized. These are conversational entry points; use the
equivalent natural-language request if your harness does not register slash commands.

The skill preserves existing work and covers canonical agent instructions, project structure,
architecture decisions, and stack-aware checks. Code scaffolding needs the selected toolchain;
AFD and live harness checks are optional and require their own setup and authorization.
Multi-harness governance and frontier/Chinese model tiering can be planned using the
embedded model catalog and execution model references.
See the [skill documentation](skills/software-engineering/project-init/SKILL.md) for inputs,
prerequisites, outputs, and failure behavior.

## Design

- **Self-contained:** skill instructions, references, examples, and command definitions live inside one skill directory.
- **Independent:** no shared runtime, prompts, state, or cross-skill assumptions.
- **Standard:** each skill exposes `SKILL.md` with standard frontmatter and can be consumed by compatible agent clients.
- **Lean installs:** a skill directory holds only what agents read or run; evals and refresh procedures live in `maintenance/<skill-name>/`.
- **Simple:** prefer small slash commands over frameworks or deployment infrastructure.
- **Composable commands:** use explicit command sections when one skill offers multiple related slash commands.

Skill structures are inspired by [`smota/metaskills --skill agent-builder`](https://github.com/smota/metaskills), but intentionally constrained for straightforward maintenance and direct installation.

## Repository layout

```text
skills/
  personal/
    <skill-name>/
  research/
    <skill-name>/
  writing/
    <skill-name>/
  software-engineering/
    <skill-name>/

  # Each skill directory contains:
  # SKILL.md, optional README.md, references/, examples/, scripts/

templates/
  SKILL.md                # minimal starter template

docs/
  authoring.md            # authoring and validation rules

maintenance/
  <skill-name>/           # maintainer-only evals, refresh procedures, generators
```

## Add skill

1. Choose a class: `personal`, `research`, `writing`, or `software-engineering`.
2. Copy `templates/SKILL.md` to `skills/<class>/<skill-name>/SKILL.md`.
3. Keep all context needed by the agent inside that directory.
4. Define simple slash commands under `## Commands`; document arguments, output, and failure behavior. Set `disable-model-invocation: true` when only the user should start the skill.
5. Declare prerequisites and credits, and add examples for non-obvious workflows. Put evals and refresh procedures in `maintenance/<skill-name>/`.
6. Update the root README catalog with the class, purpose, prerequisites, and install command.
7. Validate locally, then test installation from the branch or commit with `npx skills add`.
8. Commit the skill and catalog update together.

## Repository guidance

Repository structure and contribution rules live in [`AGENTS.md`](AGENTS.md); authoring details live in [`docs/authoring.md`](docs/authoring.md).
