# AGENTS.md

## Mission

Build and maintain a catalog of independent, installable agent skills. Each skill solves one focused problem through clear instructions and simple slash commands.

## Repository structure

- `skills/<class>/<skill-name>/` — one self-contained skill.
- Supported classes: `personal`, `research`, `writing`, `software-engineering`.
- `SKILL.md` — required agent entry point and usage documentation.
- `README.md` — repository catalog and installation guidance.
- `docs/` — repository-wide authoring guidance.
- `maintenance/<skill-name>/` — maintainer-only evals, refresh procedures, and generators for one skill; kept out of the skill directory so installs carry only what agents read or run.
- `templates/` — starter files only; never treated as runtime dependencies.

## Skill contract

Every skill MUST:

- Include valid `SKILL.md` frontmatter with unique `name`, useful quoted `description` (enclosed in `"..."` with inner quotes escaped as `\"`, or folded scalar `>-` to ensure YAML compliance), and matching `category` (matching parent `<class>`).
- Set `disable-model-invocation: true` and write a one-line human-facing `description` when only the user should start the skill. Omit the flag when the agent must reach the skill on its own, and put the trigger branches in its `description`.
- State purpose, behavior, inputs, outputs, constraints, failure behavior, and slash commands in its own documentation.
- Remain self-contained. No dependency on sibling skills, shared prompts, shared state, or undocumented services.
- Declare underlying tools, runtimes, accounts, packages, permissions, and setup steps under `## Prerequisites`.
- Credit upstream skills, prompts, research, tools, or substantial adaptations under `## Credits`.
- Avoid secrets and silently destructive behavior.

## Workflow

1. Choose exactly one class.
2. Create `skills/<class>/<skill-name>/`.
3. Write and test the skill's `SKILL.md`; add local references, examples, and scripts only when needed. Put its evals and refresh procedures in `maintenance/<skill-name>/`.
4. Update root `README.md` in the same change: add or remove the skill from the catalog, with class, purpose, prerequisites, and install command.
5. Validate frontmatter, syntax, paths, and catalog entry:
   - Run `npx skills add . -l`.
   - Verify output contains zero `⚠ Skipped` warnings (note: `npx skills` exits 0 even if skills are skipped due to YAML parse errors).
   - Verify the skill appears in `Available Skills` with its expected name and full description.
   - Confirm absence of cross-skill references, correct `category`, and that all prerequisites and credits are documented.
   - Complete when: `npx skills add . -l` runs with 0 skipped warnings, the skill is listed in `Available Skills`, and all self-containment checks pass.
6. Commit the skill and catalog update together.

## Consistency rules

- Prefer plain Markdown and deterministic helpers over frameworks.
- Keep command names explicit and focused. List each composed command individually, as a table row when commands share the same fields.
- Use lowercase, short, hyphenated skill names.
- README is the public catalog; each skill's own documentation is the authority for detailed usage.
- Never commit or merge a skill without running `npx skills add . -l` and confirming zero `⚠ Skipped` warnings and clean listing.
- Do not merge a skill without its README catalog entry.
