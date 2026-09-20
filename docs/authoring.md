# Skill authoring

## Required contract

Each skill is a directory under `skills/<class>/` containing `SKILL.md`. Supported classes: `personal`, `research`, `writing`, and `software-engineering`. Keep skill names lowercase, short, and hyphenated. `SKILL.md` starts with YAML frontmatter:

```yaml
---
name: example-skill
description: One-line description of when to use skill.
category: research
disable-model-invocation: true
---
```

`disable-model-invocation: true` is optional and marks a skill only the user starts. Its `description` is then a one-line human summary with no triggers, and it adds no context load in clients that honor the flag. Omit the flag when the agent must reach the skill on its own, and write the `description` as a pointer: lead with the verb, list one trigger per distinct branch, and leave out what the body already says.

Use imperative instructions. State inputs, outputs, constraints, prerequisites, credits, and safe failure behavior. End each workflow step with a `Complete when:` criterion the agent can check. Do not reference another skill in same repository.

## Commands

Expose commands as explicit slash commands. Use this shape:

```markdown
## Commands

### `/example [input]`
- Input: ...
- Action: ...
- Output: ...
- Failure: ...
```

Composed commands should list each command separately, then document shared rules. When commands share the same fields, a table keeps each one listed while removing the repetition:

```markdown
| Command | Reads | Delta from the base command | Output |
|---|---|---|---|
| `/example` | `references/base.md` | none | Report |
| `/example deep` | `references/base.md`, `references/deep.md` | Adds nested scopes | Report per scope |
```

Put a command's failure behavior in the table only when it differs from the shared rule. Avoid hidden command routing or large orchestration layers.

## Prerequisites and credits

Add `## Prerequisites` listing every underlying tool, runtime, package, account, permission, and setup step. Add `## Credits` for upstream skills, prompts, research, tools, or substantial adaptations. Say `None` when no external basis exists.

## Self-containment checklist

- Category matches parent directory.
- No references to sibling skill paths.
- Root `README.md` contains catalog entry with class, purpose, prerequisites, and install command.
- `## Prerequisites` is explicit, including `None` when applicable.
- `## Credits` identifies upstream work or says `None`.
- No required shared environment variables, services, or databases.
- Supporting references/examples stored inside skill directory.
- Evals, refresh procedures, and generators stored in `maintenance/<skill-name>/`, with no link to them from `SKILL.md`.
- Deterministic scripts use relative paths and explain dependencies.
- Secrets never committed.
- Installation works with `npx skills add` against repository or skill path.

## Validation

From repository root:

```bash
find skills -mindepth 3 -maxdepth 3 -name SKILL.md -print
```

For each skill, verify frontmatter, unique `name`, useful `description`, command behavior, and absence of sibling dependencies. Test installation in a temporary consumer project before release.
