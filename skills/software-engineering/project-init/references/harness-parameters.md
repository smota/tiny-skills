# Agent Harness Invocation & Parameter Reference

**Snapshot Date:** 2026-09-20  
**Scope:** Definitive command templates, CLI flags, internal agent primitives, and parameter constraints for major agent harnesses to eliminate trial-and-error model selection.

Use this reference to construct execution commands and to bind the harness roster in [execution-policy.template.md](../assets/execution-policy.template.md).

## Operating Rules

1. **Snapshot first, then verify:** Take flags from this table. When a command fails, or the snapshot date above is more than 90 days old, confirm the flag with the harness's `--help` or the provider's documentation, and report the difference so the snapshot can be refreshed.
2. **Strict Reasoning Parameter Rules:**
   - **Anthropic Thinking:** When `thinking` is enabled, `temperature` MUST NOT be passed, or must be set strictly to `1.0`. Enforcing `temperature: 0.0` causes HTTP 400 rejection.
   - **OpenAI Reasoning (o1, o3-mini):** Never pass `temperature`, `top_p`, or penalty parameters. Set reasoning intensity via `reasoning_effort` (`low`, `medium`, `high`).
   - **DeepSeek Reasoner (R1):** Temperature is fixed internally by DeepSeek. Do not attempt to override temperature for R1.
3. **Headless Execution Requirement:** Always supply non-interactive / auto-approve flags (`-p`, `--yes`, `--permission-mode accept-all`) when dispatching background subagents to prevent CLI processes from locking up on interactive prompts.

## Harness Reference Cards

### Pi Coding Agent (pi.dev) (`pi-dev`)

- **Binary:** `pi`
- **Installation:** `npm install -g --ignore-scripts @earendil-works/pi-coding-agent`
- **Website:** https://pi.dev
- **Type:** `cli`

**Key CLI Flags:**

| Purpose | Flag Syntax | Description / Example |
|---|---|---|
| `model` | `--model {model_id}` | Direct parameter binding |
| `headless_prompt` | `-p "{prompt}"` | Direct parameter binding |
| `mode` | `--mode text|json|rpc` | Direct parameter binding |
| `restricted_tools` | `--tools {comma_separated_tools}` | Direct parameter binding |
| `exclude_tools` | `--exclude-tools {tool_name}` | Direct parameter binding |
| `system_prompt` | `--system-prompt "{text}"` | Direct parameter binding |
| `append_system_prompt` | `--append-system-prompt "{text}"` | Direct parameter binding |

**Operational Tier Presets (Copy-Pasteable):**

- **T1 (`scout`):**
  ```bash
  pi --model deepseek/deepseek-chat --tools read,grep,find,ls -p "{prompt}"
  ```
- **T2 (`driver`):**
  ```bash
  pi --model sonnet -p "{prompt}"
  ```
- **T3 (`reviewer`):**
  ```bash
  pi --model sonnet:high --tools read,grep,find,ls -p "{prompt}"
  ```
- **T3_budget (`reviewer`):**
  ```bash
  pi --model deepseek/deepseek-r1 --tools read,grep,find,ls -p "{prompt}"
  ```

**Prohibitions & Critical Constraints:**

- ⚠️ **Always pass -p / --print in non-interactive sessions to avoid TUI terminal lockup.**
- ⚠️ **Always use --tools read,grep,find,ls when running in reviewer or scout role to enforce read-only boundary.**

### Claude Code CLI (`claude-code`)

- **Binary:** `claude`
- **Installation:** `npm install -g @anthropic-ai/claude-code`
- **Type:** `cli`

**Key CLI Flags:**

| Purpose | Flag Syntax | Description / Example |
|---|---|---|
| `model` | `--model {model_id}` | Direct parameter binding |
| `headless_prompt` | `-p "{prompt}"` | Direct parameter binding |
| `stdin_prompt` | `echo "{prompt}" | claude -p` | Direct parameter binding |
| `auto_approve` | `--permission-mode accept-all` | Direct parameter binding |
| `output_format` | `--output-format json|text` | Direct parameter binding |

**Operational Tier Presets (Copy-Pasteable):**

- **T1 (`scout`):**
  ```bash
  claude -p "{prompt}" --model claude-3-5-haiku-20241022 --permission-mode accept-all
  ```
- **T2 (`driver`):**
  ```bash
  claude -p "{prompt}" --model claude-3-7-sonnet-20250219 --permission-mode accept-all
  ```
- **T3 (`reviewer`):**
  ```bash
  MAX_THINKING_TOKENS=16000 claude -p "{prompt}" --model claude-3-7-sonnet-20250219 --permission-mode accept-all
  ```

**Prohibitions & Critical Constraints:**

- ⚠️ **Never run without -p in non-interactive subagent sessions (blocks waiting for stdin).**
- ⚠️ **Do not pass --temperature flags (unsupported on Claude Code CLI).**

### Aider CLI (`aider`)

- **Binary:** `aider`
- **Installation:** `pip install aider-chat`
- **Type:** `cli`

**Key CLI Flags:**

| Purpose | Flag Syntax | Description / Example |
|---|---|---|
| `model` | `--model {model_id}` | Direct parameter binding |
| `reasoning_effort` | `--reasoning-effort {low|medium|high}` | Direct parameter binding |
| `thinking_tokens` | `--thinking-tokens {tokens}` | Direct parameter binding |
| `headless_prompt` | `--message "{prompt}"` | Direct parameter binding |
| `prompt_file` | `--message-file {file_path}` | Direct parameter binding |
| `auto_approve` | `--yes --no-auto-commits` | Direct parameter binding |
| `architect_mode` | `--architect --model {reasoning_model} --editor-model {coding_model}` | Direct parameter binding |

**Operational Tier Presets (Copy-Pasteable):**

- **T1 (`scout`):**
  ```bash
  aider --model deepseek/deepseek-chat --message "{prompt}" --yes --no-auto-commits --read-only
  ```
- **T2 (`driver`):**
  ```bash
  aider --model claude-3-7-sonnet-20250219 --message "{prompt}" --yes --no-auto-commits
  ```
- **T3 (`reviewer`):**
  ```bash
  aider --model openrouter/deepseek/deepseek-r1 --reasoning-effort high --message "{prompt}" --yes --no-auto-commits --read-only
  ```

**Prohibitions & Critical Constraints:**

- ⚠️ **Always include --yes in scripts to prevent blocking interactive commit/git prompts.**
- ⚠️ **Include --no-auto-commits when running inside task-owned delivery loops.**

### OpenCode / Codex CLI (`opencode-codex`)

- **Binary:** `opencode`
- **Type:** `cli`

**Key CLI Flags:**

| Purpose | Flag Syntax | Description / Example |
|---|---|---|
| `model` | `--model {model_id}` | Direct parameter binding |
| `run_file` | `run -f {file_path}` | Direct parameter binding |
| `headless` | `--headless` | Direct parameter binding |
| `auto_approve` | `--auto-approve` | Direct parameter binding |

**Operational Tier Presets (Copy-Pasteable):**

- **T1 (`scout`):**
  ```bash
  opencode run -f {prompt_file} --model gpt-4o-mini --headless --auto-approve
  ```
- **T2 (`driver`):**
  ```bash
  opencode run -f {prompt_file} --model gpt-4o --headless --auto-approve
  ```
- **T3 (`reviewer`):**
  ```bash
  opencode run -f {prompt_file} --model o3-mini --headless --auto-approve
  ```

**Prohibitions & Critical Constraints:**

- ⚠️ **Never run without --headless in unattended automation.**

### Cline / Roo-Code Config (`cline-roo`)

- **Type:** `configuration_file`

**Operational Tier Presets (Copy-Pasteable):**

- **T1 (`scout`):**
  ```json
{
    "apiProvider": "deepseek",
    "apiModelId": "deepseek-chat",
    "autoApprove": [
        "read",
        "command"
    ]
}
  ```
- **T2 (`driver`):**
  ```json
{
    "apiProvider": "anthropic",
    "apiModelId": "claude-3-7-sonnet-20250219",
    "autoApprove": [
        "read",
        "write",
        "command"
    ]
}
  ```
- **T3 (`reviewer`):**
  ```json
{
    "apiProvider": "deepseek",
    "apiModelId": "deepseek-reasoner",
    "autoApprove": [
        "read"
    ]
}
  ```

**Prohibitions & Critical Constraints:**

- ⚠️ **Do not set temperature for deepseek-reasoner or thinking models in config.**

### Antigravity Agent Primitive (invoke_subagent) (`antigravity-subagent`)

- **Type:** `agent_primitive`

**Operational Tier Presets (Copy-Pasteable):**

- **T1 (`scout`):**
  ```python
  invoke_subagent(Subagents=[{'TypeName': 'research', 'Role': 'Codebase Scout', 'Model': 'flash_lite', 'Prompt': '...'}])
  ```
- **T2 (`driver`):**
  ```python
  invoke_subagent(Subagents=[{'TypeName': 'self', 'Role': 'Feature Driver', 'Model': 'flash', 'Prompt': '...'}])
  ```
- **T3 (`reviewer`):**
  ```python
  invoke_subagent(Subagents=[{'TypeName': 'self', 'Role': 'Adversarial Reviewer', 'Model': 'pro', 'Prompt': '...'}])
  ```

**Prohibitions & Critical Constraints:**

- ⚠️ **Do not pass external model IDs (e.g. 'claude-3-7-sonnet' or 'gpt-4o') to invoke_subagent; use only 'flash_lite', 'flash', 'pro', or 'inherit'.**

### Direct Provider API Request Parameters (`direct-api`)

- **Type:** `api`

**Provider API Parameter Rules:**

- **Anthropic:** When thinking is enabled ({'type': 'enabled', 'budget_tokens': N}), temperature MUST NOT be set or must be exactly 1.0. Any other temperature returns HTTP 400.
- **Openai:** For reasoning models (o1, o3-mini), do NOT send temperature, top_p, or presence_penalty. Use reasoning_effort ('low' | 'medium' | 'high').
- **Deepseek:** For deepseek-reasoner (R1), temperature is fixed by the provider. Do not attempt to override temperature. For deepseek-chat, use temperature=0.0 for deterministic coding.
- **Google:** For gemini-2.0-flash-thinking-exp, set thinkingConfig in generationConfig. Pass temperature=0.0 for deterministic code checks.
