# Model Catalog Maintenance and Refresh Checklist

## Purpose

Maintain the freshness, price accuracy, and tier classification of `references/model-catalog.json` and its rendered companion `references/model-catalog.md` in the `project-init` skill.

## Triggers

1. **Scheduled review:** Quarterly or whenever `refresh_model_catalog.py --check-staleness` reports the snapshot exceeds 90 days.
2. **Market events:** Major model family release (Anthropic Claude, OpenAI, Google Gemini, DeepSeek, Alibaba Qwen, Moonshot, Zhipu, MiniMax), major price reductions, or prompt-caching rate shifts.
3. **Discontinued APIs:** Deprecation or retirement of snapshot dates and model identifiers.

## Primary Verification Sources

Always check official provider pricing and documentation. Never infer rates or rely on memorized numbers:

| Provider | Authoritative Verification Surface |
|---|---|
| **Anthropic** | Anthropic API Pricing (`anthropic.com/pricing`) and API Model Overview docs |
| **OpenAI** | OpenAI API Pricing (`openai.com/api/pricing`) and Platform Models index |
| **Google** | Google AI Studio Pricing (`ai.google.dev/pricing`) and Vertex AI Model Reference |
| **DeepSeek** | DeepSeek Open Platform Pricing (`platform.deepseek.com/api-docs/pricing`) |
| **Alibaba Cloud** | DashScope Model Pricing (`help.aliyun.com/document_detail/2712581.html`) |
| **Moonshot AI** | Moonshot Open Platform Pricing (`platform.moonshot.cn/docs/pricing`) |
| **Zhipu AI** | BigModel Open Platform Pricing (`open.bigmodel.cn/pricing`) |
| **MiniMax** | MiniMax Open Platform Pricing (`platform.minimaxi.com/document/pricing`) |

## Classification Rules for Tiers

When adding or reclassifying a model, apply these criteria:

- **T1 (`mechanical`):** High tokens/sec, low input cost ($ < 1.00 per 1M), large context window, fast extraction. Primary roles: `scout`, `oracle` (assisted).
- **T2 (`standard`):** Proven coding capability, high adherence to formatting/contracts, multi-file diff reliability. Primary role: `driver`.
- **T3 (`judgment`):** Dedicated reasoning/thinking models (o1, o3-mini, Claude Thinking, DeepSeek R1, QwQ), capable of identifying subtle race conditions, contract violations, and adversarial failure modes. Primary roles: `reviewer`, `arbiter`.

## Execution Procedure

1. **Check Staleness:**
   ```bash
   python skills/software-engineering/project-init/scripts/refresh_model_catalog.py --check-staleness
   ```

2. **Update JSON Records:**
   Edit `skills/software-engineering/project-init/references/model-catalog.json` directly or use helper flags:
   ```bash
   # Quick price update example:
   python skills/software-engineering/project-init/scripts/refresh_model_catalog.py --update-price <model_id> <input_usd> <output_usd> [<cache_usd>]
   ```

3. **Validate Catalog Integrity:**
   Ensure schema compliance, positive token windows and prices, valid roles, and unique IDs:
   ```bash
   python skills/software-engineering/project-init/scripts/refresh_model_catalog.py --validate
   ```

4. **Re-render Markdown Reference:**
   Regenerate `model-catalog.md`:
   ```bash
   python skills/software-engineering/project-init/scripts/refresh_model_catalog.py --render
   ```

5. **Verify Outputs:**
   Inspect git diff to confirm table alignment and valid markdown links:
   ```bash
   git diff skills/software-engineering/project-init/references/
   ```

6. **Self-Contained Commit:**
   Commit the refreshed data, documentation, and snapshot date together:
   ```bash
   git commit -m "chore(project-init): refresh model catalog snapshot to YYYY-MM-DD"
   ```
