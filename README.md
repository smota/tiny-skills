# tiny-skills

Self-contained, production-ready agent skills repository.

Each directory under `skills/` is an independent agent. Skills are grouped by class for discovery, while remaining fully independent. Agents do not depend on, import, or coordinate with other agents in this repository. Every agent follows the Agent Skill standard and can be installed directly with:

```bash
npx skills add github.com/<owner>/tiny-skills --skill <skill-name>
```

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
3. Keep all context needed by agent inside that directory.
3. Define simple slash commands under `## Commands`; document arguments, output, and failure behavior.
4. Add examples for non-obvious workflows.
5. Validate locally, then install from branch or commit with `npx skills add`.

See [`docs/authoring.md`](docs/authoring.md).
