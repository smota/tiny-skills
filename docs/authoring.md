# Skill authoring

## Required contract

Each skill is a directory under `skills/` containing `SKILL.md`. Keep skill names lowercase, short, and hyphenated. `SKILL.md` starts with YAML frontmatter:

```yaml
---
name: example-skill
description: One-line description of when to use skill.
---
```

Use imperative instructions. State inputs, outputs, constraints, and safe failure behavior. Do not reference another skill in same repository.

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

## Self-containment checklist

- No references to sibling skill paths.
- No required shared environment variables, services, or databases.
- Supporting references/examples stored inside skill directory.
- Deterministic scripts use relative paths and explain dependencies.
- Secrets never committed.
- Installation works with `npx skills add` against repository or skill path.

## Validation

From repository root:

```bash
find skills -mindepth 2 -maxdepth 2 -name SKILL.md -print
```

For each skill, verify frontmatter, unique `name`, useful `description`, command behavior, and absence of sibling dependencies. Test installation in a temporary consumer project before release.
