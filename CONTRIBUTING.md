# Contributing

Add only independent skills under `skills/<skill-name>/`.

## Pull request rules

- One skill per focused change when practical.
- Include `SKILL.md`; keep agent context self-contained.
- Document slash commands and failure behavior.
- Do not add dependencies between skills.
- Include examples for composed commands.
- Test installation with `npx skills add` from a clean temporary project.

Keep implementation small. Prefer plain Markdown and deterministic scripts over frameworks.
