# Harness Parameters Maintenance and Continuous Refresh Checklist

## Purpose

Maintain the accuracy, invocation flags, headless options, and parameter constraints in `maintenance/project-init/harness-parameters.json` and its rendered companion `skills/software-engineering/project-init/references/harness-parameters.md`.

## Triggers

1. **CLI Version Updates:** When a harness CLI package updates (e.g. `@earendil-works/pi-coding-agent`, `@anthropic-ai/claude-code`, `aider-chat`).
2. **Provider Parameter Shifts:** When provider APIs alter reasoning controls (e.g. changing from fixed thinking tokens to reasoning effort levels or new temperature compatibility rules).
3. **New Harness Onboarding:** Adding new coding agents or runners (e.g., Goose, Mentat, Cursor Composer CLI).
4. **Automated Staleness Trigger:** When `python refresh_model_catalog.py --check-staleness` flags the snapshot as older than 90 days.

## Verification Surfaces and Commands

Inspect the installed version of each CLI to verify available flags:

| Harness | Primary Inspection Command | Critical Verification Questions |
|---|---|---|
| **Pi Coding Agent (`pi.dev`)** | `pi --help` | Has `--model`, `-p` (non-interactive), `--tools` syntax changed? |
| **Claude Code** | `claude --help` | Is `-p` and `--permission-mode accept-all` still current? |
| **Aider** | `aider --help` | What are the current `--reasoning-effort` and `--architect` flags? |
| **OpenCode / Codex** | `opencode --help` | Are `--headless` and `run -f` flags intact? |
| **Antigravity** | Check `invoke_subagent` docstring | What are the valid string values for `Model` (`flash_lite`, `flash`, `pro`, `inherit`)? |

## Continuous Refresh Procedure

1. **Check Staleness:**
   ```bash
   python maintenance/project-init/refresh_model_catalog.py --check-staleness
   ```

2. **Probe Flag Changes:**
   Run a dry-run invocation of the target CLI in a sandbox to confirm non-interactive behavior:
   ```bash
   # Example: Verify pi.dev non-interactive print mode
   pi -p "hello" --model sonnet
   ```

3. **Update JSON Schema Records:**
   Edit `maintenance/project-init/harness-parameters.json` to update flags, environment variables, tier presets, or prohibitions.

4. **Validate Schema and Integrity:**
   Ensure valid JSON, unique IDs, valid role definitions, and no missing keys:
   ```bash
   python maintenance/project-init/refresh_model_catalog.py --validate
   ```

5. **Re-render Markdown Reference:**
   Regenerate `references/harness-parameters.md` deterministically:
   ```bash
   python maintenance/project-init/refresh_model_catalog.py --render
   ```

6. **Inspect Diff and Commit:**
   Confirm changes and commit atomically:
   ```bash
   git diff skills/software-engineering/project-init/references/
   git commit -m "chore(project-init): refresh harness parameters snapshot to YYYY-MM-DD"
   ```
