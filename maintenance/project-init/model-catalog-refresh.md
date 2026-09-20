# Model Catalog Maintenance and Refresh Checklist

## Purpose

Maintain the freshness, price accuracy, and tier classification of `maintenance/project-init/model-catalog.json` and its rendered companion `skills/software-engineering/project-init/references/model-catalog.md`.

## Triggers

1. **Scheduled review:** Quarterly or whenever `refresh_model_catalog.py --check-staleness` lists a model as unverified or verified more than 90 days ago.
2. **Market events:** Major model family release from Anthropic, OpenAI, Google, DeepSeek, or Alibaba (Qwen), major price reductions, promotions ending, or prompt-caching rate shifts.
3. **Discontinued APIs:** Deprecation or retirement of model identifiers. Rows record retirement dates in their notes (for example Claude Haiku 4.5, not sooner than 2026-10-15).

## Primary Verification Sources

Take rates, context windows, and identifiers from the provider's own pages. Rely on the page, never on memory:

| Provider | Pricing | Models and limits |
|---|---|---|
| **Anthropic** | `https://platform.claude.com/docs/en/about-claude/pricing` | `https://platform.claude.com/docs/en/models/overview` |
| **OpenAI** | `https://developers.openai.com/api/docs/pricing` | `https://developers.openai.com/api/docs/models` |
| **Google** | `https://ai.google.dev/gemini-api/docs/pricing` | `https://ai.google.dev/gemini-api/docs/models/<model-id>` (input and output token limits) |
| **DeepSeek** | `https://api-docs.deepseek.com/quick_start/pricing` | the same page, plus the release notes under `https://api-docs.deepseek.com/news/` |
| **Alibaba Cloud (Qwen)** | `https://www.alibabacloud.com/help/en/model-studio/model-pricing` (Singapore/International) | `https://www.alibabacloud.com/help/en/model-studio/<model-slug>` (for example `qwen3-8-max`) |

`pi --list-models` and `claude --help` are useful cross-checks for identifiers and aliases on the providers configured on the machine, but they carry no prices.

## Verification Rule

Set `verified_at` on a row only when the provider's page states its price and context window in a verbatim table, or in two independent reads that agree. Leave it `null` for a row read once, and say why in its notes. For every row record:

- `sources`: the provider URLs used.
- `notes`: price tiers by prompt length, promotions with their end dates, peak and off-peak rates, preview status, retirement dates, and any figure two reads disagreed on. Store `null` for a cache price the provider did not state consistently.
- Pairings reference catalog model ids and harness ids, and use different harnesses for driver and reviewer. The script checks this.

## Classification Rules for Tiers

Tier meanings are defined once, in `skills/software-engineering/project-init/assets/execution-policy.template.md`. When adding or reclassifying a model, apply these criteria:

- **T1 (`mechanical`):** High tokens/sec, input cost at or below $1.00 per 1M, large context window, fast extraction. Primary roles: `scout`, `oracle` (assisted).
- **T2 (`standard`):** Proven coding capability, high adherence to formatting/contracts, multi-file diff reliability. Primary role: `driver`.
- **T3 (`judgment`):** Models the provider positions for demanding reasoning or long-horizon agentic work, capable of identifying subtle race conditions, contract violations, and adversarial failure modes. Primary roles: `reviewer`, `arbiter`. When the provider gives no positioning, say in the row's notes that the tier is a judgment.

## Execution Procedure

1. **Check Staleness:**
   ```bash
   python maintenance/project-init/refresh_model_catalog.py --check-staleness
   ```

2. **Update JSON Records:**
   Edit `maintenance/project-init/model-catalog.json` directly or use helper flags:
   ```bash
   # Quick price update example (stamps the model it changes):
   python maintenance/project-init/refresh_model_catalog.py --update-price <model_id> <input_usd> <output_usd> [<cache_usd>]
   # Stamp every entry you checked against its provider's own pages:
   python maintenance/project-init/refresh_model_catalog.py --mark-verified <model_id> [<model_id> ...]
   ```

3. **Validate Catalog Integrity:**
   Ensure schema compliance, positive token windows and prices, valid roles, and unique IDs:
   ```bash
   python maintenance/project-init/refresh_model_catalog.py --validate
   ```

4. **Re-render Markdown Reference:**
   Regenerate `model-catalog.md`:
   ```bash
   python maintenance/project-init/refresh_model_catalog.py --render
   ```

5. **Verify Outputs:**
   Inspect git diff to confirm table alignment and valid markdown links:
   ```bash
   git diff skills/software-engineering/project-init/references/
   ```

6. **Self-Contained Commit:**
   Commit the refreshed data, documentation, and verification dates together:
   ```bash
   git commit -m "chore(project-init): refresh model catalog verification to YYYY-MM-DD"
   ```
