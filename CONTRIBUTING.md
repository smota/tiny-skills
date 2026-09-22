# Contributing

Add only independent skills under `skills/<class>/<skill-name>/` (supported classes: `personal`, `research`, `writing`, `software-engineering`).

## Pull request rules

- One skill per focused change when practical.
- Include valid `SKILL.md` frontmatter with quoted `description` (`"..."` with inner quotes escaped, or folded scalar `>-`) to ensure YAML compatibility.
- Validate locally with `npx skills add . -l`; confirm zero `⚠ Skipped` warnings and that the skill appears in `Available Skills`.
- Update root `README.md` catalog entry with class, purpose, prerequisites, and install command in the same PR.
- Keep agent context self-contained; do not add dependencies between skills.
- Document slash commands and failure behavior.
- Include examples for composed commands.
- Test installation with `npx skills add` from a clean temporary project.

Keep implementation small. Prefer plain Markdown and deterministic scripts over frameworks.
