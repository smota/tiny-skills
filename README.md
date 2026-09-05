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
| software-engineering | [deer-workflow](skills/software-engineering/deer-workflow/) | Operate Deer Workflow graphs from inside an agent session | Node.js/Bun, `@deerwork-ai/deer-workflow`, selected agent harness | `npx skills add smota/tiny-skills --skill deer-workflow` |
| software-engineering | [project-init](skills/software-engineering/project-init/) | Initialize project practices through a short intake, canonical instructions, ADRs, and stack-aware validation | Read/write access; selected toolchain for code; optional AFD and agent CLIs | `npx skills add smota/tiny-skills --skill project-init` |
| writing | [release-notes](skills/writing/release-notes/) | Turn supplied change material or selected Git commits into user-centered release notes | None for supplied content; Git and repository read access for commit collection | `npx skills add smota/tiny-skills --skill release-notes` |

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
See the [skill documentation](skills/software-engineering/project-init/SKILL.md) for inputs,
prerequisites, outputs, and failure behavior.

## Design

- **Self-contained:** skill instructions, references, examples, and command definitions live inside one skill directory.
- **Independent:** no shared runtime, prompts, state, or cross-skill assumptions.
- **Standard:** each skill exposes `SKILL.md` with standard frontmatter and can be consumed by compatible agent clients.
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
```

## Add skill

1. Choose a class: `personal`, `research`, `writing`, or `software-engineering`.
2. Copy `templates/SKILL.md` to `skills/<class>/<skill-name>/SKILL.md`.
3. Keep all context needed by the agent inside that directory.
4. Define simple slash commands under `## Commands`; document arguments, output, and failure behavior.
5. Declare prerequisites and credits, and add examples for non-obvious workflows.
6. Update the root README catalog with the class, purpose, prerequisites, and install command.
7. Validate locally, then test installation from the branch or commit with `npx skills add`.
8. Commit the skill and catalog update together.

## Repository guidance

Repository structure and contribution rules live in [`AGENTS.md`](AGENTS.md); authoring details live in [`docs/authoring.md`](docs/authoring.md).
