# Skill authoring

## Required contract

Each skill is a directory under `skills/<class>/` containing `SKILL.md`. Supported classes: `personal`, `research`, `writing`, and `software-engineering`. Keep skill names lowercase, short, and hyphenated. `SKILL.md` starts with YAML frontmatter:

```yaml
---
name: example-skill
description: One-line description of when to use skill.
category: research
---
```

Use imperative instructions. State inputs, outputs, constraints, prerequisites, credits, and safe failure behavior. Do not reference another skill in same repository.

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

Composed commands should list each command separately, then document shared rules. Avoid hidden command routing or large orchestration layers.

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
- Deterministic scripts use relative paths and explain dependencies.
- Secrets never committed.
- Installation works with `npx skills add` against repository or skill path.

## Validation

From repository root:

```bash
find skills -mindepth 3 -maxdepth 3 -name SKILL.md -print
```

For each skill, verify frontmatter, unique `name`, useful `description`, command behavior, and absence of sibling dependencies. Test installation in a temporary consumer project before release.
