# Canonical Model Catalog for Tiered Orchestration

**Verification:** each row carries the date it was last checked against the provider's own pages; `unverified` means no such check is recorded.  
**Scope:** Reference mapping of frontier Western and Chinese AI models to operational tiers (T1–T3) for multi-harness and multi-model project governance.

This catalog supplies the tier-to-model mapping in [execution-policy.template.md](../assets/execution-policy.template.md), which also defines tiers T0–T3. Verify API availability, identifiers, and current pricing against official provider documentation prior to locking budgets. For invocation flags and agent primitives, see [harness-parameters.md](harness-parameters.md).

## T1: Mechanical Models (Scout, Inventory, Fast Context)

Fast context extraction, project search, and deterministic-assisted tasks.

| Provider | Model Name | API Identifier | Origin | Context | In / Out (per 1M) | Cache In | Recommended Roles | Strengths | Verified |
|---|---|---|---|---|---|---|---|---|---|
| **Anthropic** | Claude 3.5 Haiku | `claude-3-5-haiku-20241022` | Western | 200k | $0.80 / $4.00 | $0.08 | `scout`, `oracle` | Fast context reading, high prompt-caching efficiency, structured inventory and extraction. | unverified |
| **OpenAI** | GPT-4o mini | `gpt-4o-mini` | Western | 128k | $0.15 / $0.60 | $0.07 | `scout` | Ultra-low token cost, broad ecosystem tooling compatibility, high throughput batching. | unverified |
| **Google** | Gemini 2.0 Flash | `gemini-2.0-flash` | Western | 1M | $0.10 / $0.40 | $0.03 | `scout` | Massive 1M context window at low price, multi-file code scanning, minimal latency. | unverified |
| **DeepSeek** | DeepSeek V3 (Chat) | `deepseek-chat` | Chinese | 64k | $0.14 / $0.28 | $0.01 | `scout`, `driver` | Unbeatable token economy, strong coding fundamentals, low cache read cost. | unverified |
| **Alibaba Cloud** | Qwen 2.5 Turbo | `qwen-turbo` | Chinese | 1M | $0.05 / $0.20 | $0.01 | `scout` | 1M context window at minimal cost, excellent multilingual and JSON schema compliance. | unverified |
| **Zhipu AI** | GLM-4 Flash | `glm-4-flash` | Chinese | 128k | $0.01 / $0.01 | $0.00 | `scout` | Near-zero cost tier for auxiliary scans, background documentation parsing, and lint sorting. | unverified |

## T2: Standard Models (Driver, Implementation Workhorse)

Code authoring, test creation, and spec-directed changes.

| Provider | Model Name | API Identifier | Origin | Context | In / Out (per 1M) | Cache In | Recommended Roles | Strengths | Verified |
|---|---|---|---|---|---|---|---|---|---|
| **Anthropic** | Claude 3.7 Sonnet | `claude-3-7-sonnet-20250219` | Western | 200k | $3.00 / $15.00 | $0.30 | `driver` | Industry gold standard for direct code generation, unit test writing, and complex diff execution. | unverified |
| **OpenAI** | GPT-4o | `gpt-4o` | Western | 128k | $2.50 / $10.00 | $1.25 | `driver` | Stable function calling, robust multi-language implementation, mature tool use. | unverified |
| **Google** | Gemini 2.5 Pro | `gemini-2.5-pro` | Western | 2M | $1.25 / $5.00 | $0.31 | `driver`, `scout` | Huge 2M context for holistic refactoring across large codebases, rigorous type compliance. | unverified |
| **Alibaba Cloud** | Qwen 2.5 Coder 32B | `qwen-2.5-coder-32b-instruct` | Chinese | 128k | $0.20 / $0.60 | $0.05 | `driver` | Specialized open-weight coding architecture with exceptional completion quality per dollar. | unverified |
| **Moonshot AI** | Moonshot v1 (Kimi) | `moonshot-v1-128k` | Chinese | 128k | $0.80 / $0.80 | $0.10 | `driver` | High long-context recall, consistent code style conformance, strong bilingual handling. | unverified |
| **MiniMax** | MiniMax Text-01 | `abab6.5s-chat` | Chinese | 245k | $0.10 / $0.20 | $0.02 | `driver` | Extended 245k window, high token throughput for heavy multi-file diff tasks. | unverified |

## T3: Judgment & Reasoning Models (Reviewer, Arbiter, Architecture)

Contract design before code, adversarial review, and invariant verification.

| Provider | Model Name | API Identifier | Origin | Context | In / Out (per 1M) | Cache In | Recommended Roles | Strengths | Verified |
|---|---|---|---|---|---|---|---|---|---|
| **Anthropic** | Claude 3.7 Sonnet (Thinking) | `claude-3-7-sonnet-thinking` | Western | 200k | $3.00 / $15.00 | $0.30 | `reviewer`, `arbiter` | Adjustable extended reasoning, sharp adversarial critique, high invariant verification. | unverified |
| **OpenAI** | OpenAI o1 | `o1` | Western | 200k | $15.00 / $60.00 | $7.50 | `reviewer`, `arbiter` | Deep multi-step reasoning, mathematical invariants, race condition and concurrency audit. | unverified |
| **OpenAI** | OpenAI o3-mini | `o3-mini` | Western | 200k | $1.10 / $4.40 | $0.55 | `reviewer` | High reasoning density at standard coding prices; fast adversarial audit passes. | unverified |
| **Google** | Gemini 2.0 Flash Thinking | `gemini-2.0-flash-thinking-exp` | Western | 1M | $0.00 / $0.00 | $0.00 | `reviewer`, `arbiter` | Full-repository reasoning context window for cross-module architecture verification. | unverified |
| **DeepSeek** | DeepSeek R1 | `deepseek-reasoner` | Chinese | 64k | $0.55 / $2.19 | $0.14 | `reviewer`, `arbiter` | Benchmark-grade open reasoning model, exceptional at catching logic bugs and corner cases at modest cost. | unverified |
| **Alibaba Cloud** | QwQ-32B | `qwq-32b` | Chinese | 128k | $0.30 / $1.20 | $0.05 | `reviewer` | Cost-effective open-weights reasoning model for logical validation and protocol review. | unverified |
| **Moonshot AI** | Kimi k1.5 | `kimi-k1.5` | Chinese | 128k | $1.00 / $3.00 | $0.20 | `reviewer`, `arbiter` | Long-context reasoning model suited for reviewing multi-session architectural drift. | unverified |

## Recommended Pairing Strategy (Mode A)

Under **Mode A (Cross-Harness)**, the `driver` and `reviewer` must never share the same harness or subagent lineage. Recommended high-yield pairings:

| Strategy | Driver Harness & Model (T2) | Reviewer Harness & Model (T3) | Key Advantage |
|---|---|---|---|
| **Pi + Claude Frontier** | Pi CLI (`pi.dev`) / Sonnet | Codex / OpenAI o1 or o3-mini | Minimalist four-tool driver paired with deep invariant auditor. |
| **Western Frontier** | Claude Code / Claude 3.7 Sonnet | Codex or Pi / OpenAI o1 or o3-mini | Full corporate independence; catches subtle logic defects. |
| **Hybrid High-Yield** | Claude Code / Claude 3.7 Sonnet | Cline or Pi / DeepSeek R1 | High-capability implementation paired with low-cost open reasoning. |
| **Budget Maximizer** | Pi or OpenCode / DeepSeek V3 | Pi (`--tools read,grep`) / DeepSeek R1 | 80–90% cost reduction with enforced read-only independent review. |
