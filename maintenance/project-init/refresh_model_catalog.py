#!/usr/bin/env python3
"""
Model Catalog and Harness Parameter Maintenance and Rendering Script

Validates (next to this script):
    - `model-catalog.json`
    - `harness-parameters.json`
Renders (into the project-init skill):
    - `skills/software-engineering/project-init/references/model-catalog.md`
    - `skills/software-engineering/project-init/references/harness-parameters.md`

Usage:
    python refresh_model_catalog.py --render
    python refresh_model_catalog.py --validate
    python refresh_model_catalog.py --update-price <model_id> <input_usd> <output_usd> [<cache_read_usd>]
    python refresh_model_catalog.py --check-staleness [max_days]
"""

import argparse
from datetime import date, datetime
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REFERENCES_DIR = os.path.normpath(
    os.path.join(SCRIPT_DIR, "..", "..", "skills", "software-engineering", "project-init", "references")
)

MODELS_JSON_PATH = os.path.join(SCRIPT_DIR, "model-catalog.json")
MODELS_MD_PATH = os.path.join(REFERENCES_DIR, "model-catalog.md")

HARNESS_JSON_PATH = os.path.join(SCRIPT_DIR, "harness-parameters.json")
HARNESS_MD_PATH = os.path.join(REFERENCES_DIR, "harness-parameters.md")

VALID_TIERS = {"T1": "mechanical", "T2": "standard", "T3": "judgment"}
VALID_ORIGINS = {"western", "chinese"}
VALID_ROLES = {"oracle", "scout", "driver", "reviewer", "arbiter"}


# ---------------------------------------------------------------------------
# Model Catalog
# ---------------------------------------------------------------------------

def load_json(path: str) -> dict:
    if not os.path.isfile(path):
        raise FileNotFoundError(f"File not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(data: dict, path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def validate_models(data: dict) -> list[str]:
    errors = []
    if "models" not in data or not isinstance(data["models"], list):
        errors.append("Root object must contain a 'models' list.")
        return errors

    seen_ids = set()
    for idx, model in enumerate(data["models"]):
        mid = model.get("id")
        if not mid or not isinstance(mid, str):
            errors.append(f"Model at index {idx} has invalid or missing 'id'.")
            continue
        if mid in seen_ids:
            errors.append(f"Duplicate model id found: {mid}")
        seen_ids.add(mid)

        if not model.get("provider"):
            errors.append(f"Model '{mid}' is missing 'provider'.")
        if not model.get("name"):
            errors.append(f"Model '{mid}' is missing 'name'.")

        origin = model.get("origin")
        if origin not in VALID_ORIGINS:
            errors.append(f"Model '{mid}' has invalid origin '{origin}'. Expected one of {VALID_ORIGINS}.")

        tier = model.get("tier")
        if tier not in VALID_TIERS:
            errors.append(f"Model '{mid}' has invalid tier '{tier}'. Expected one of {list(VALID_TIERS.keys())}.")
        expected_tier_name = VALID_TIERS.get(tier)
        if model.get("tier_name") != expected_tier_name:
            errors.append(f"Model '{mid}' has tier_name '{model.get('tier_name')}', expected '{expected_tier_name}'.")

        ctx = model.get("context_tokens")
        if not isinstance(ctx, int) or ctx <= 0:
            errors.append(f"Model '{mid}' context_tokens must be a positive integer.")

        pricing = model.get("pricing_per_1m", {})
        for price_key in ("input_usd", "output_usd", "cache_read_usd"):
            val = pricing.get(price_key)
            if val is None or not isinstance(val, (int, float)) or val < 0:
                errors.append(f"Model '{mid}' pricing field '{price_key}' must be a non-negative number.")

        roles = model.get("recommended_roles", [])
        if not isinstance(roles, list) or not roles:
            errors.append(f"Model '{mid}' must have at least one recommended role.")
        for r in roles:
            if r not in VALID_ROLES:
                errors.append(f"Model '{mid}' role '{r}' is invalid. Expected one of {VALID_ROLES}.")

        if not model.get("strengths") or not isinstance(model.get("strengths"), str):
            errors.append(f"Model '{mid}' must have a non-empty 'strengths' description.")

    return errors


def format_price(val: float) -> str:
    if val == 0:
        return "$0.00"
    if val < 0.01:
        return f"${val:.3f}"
    return f"${val:.2f}"


def format_context(ctx: int) -> str:
    if ctx >= 1_000_000:
        return f"{ctx // 1_000_000}M"
    return f"{ctx // 1_000}k"


def render_models_markdown(data: dict) -> str:
    snapshot = data.get("snapshot_date", date.today().isoformat())
    models = data.get("models", [])

    md_lines = [
        "# Canonical Model Catalog for Tiered Orchestration",
        "",
        f"**Snapshot Date:** {snapshot}  ",
        "**Scope:** Reference mapping of frontier Western and Chinese AI models to operational tiers (T1–T3) for multi-harness and multi-model project governance.",
        "",
        "This catalog supplies the tier-to-model mapping in [execution-policy.template.md](../assets/execution-policy.template.md), which also defines tiers T0–T3. Verify API availability, identifiers, and current pricing against official provider documentation prior to locking budgets. For invocation flags and agent primitives, see [harness-parameters.md](harness-parameters.md).",
        "",
    ]

    tier_sections = [
        ("T1", "T1: Mechanical Models (Scout, Inventory, Fast Context)", "Fast context extraction, project search, and deterministic-assisted tasks."),
        ("T2", "T2: Standard Models (Driver, Implementation Workhorse)", "Code authoring, test creation, and spec-directed changes."),
        ("T3", "T3: Judgment & Reasoning Models (Reviewer, Arbiter, Architecture)", "Contract design before code, adversarial review, and invariant verification.")
    ]

    for tier_code, title, desc in tier_sections:
        tier_models = [m for m in models if m.get("tier") == tier_code]
        md_lines.append(f"## {title}")
        md_lines.append("")
        md_lines.append(desc)
        md_lines.append("")
        md_lines.append("| Provider | Model Name | API Identifier | Origin | Context | In / Out (per 1M) | Cache In | Recommended Roles | Strengths |")
        md_lines.append("|---|---|---|---|---|---|---|---|---|")

        for m in tier_models:
            pricing = m.get("pricing_per_1m", {})
            in_p = format_price(pricing.get("input_usd", 0))
            out_p = format_price(pricing.get("output_usd", 0))
            cache_p = format_price(pricing.get("cache_read_usd", 0))
            rates = f"{in_p} / {out_p}"
            ctx_str = format_context(m.get("context_tokens", 0))
            roles_str = ", ".join(f"`{r}`" for r in m.get("recommended_roles", []))
            origin_badge = "Western" if m.get("origin") == "western" else "Chinese"
            strengths = m.get("strengths", "").replace("|", "\\|")

            row = f"| **{m.get('provider')}** | {m.get('name')} | `{m.get('id')}` | {origin_badge} | {ctx_str} | {rates} | {cache_p} | {roles_str} | {strengths} |"
            md_lines.append(row)

        md_lines.append("")

    md_lines.extend([
        "## Recommended Pairing Strategy (Mode A)",
        "",
        "Under **Mode A (Cross-Harness)**, the `driver` and `reviewer` must never share the same harness or subagent lineage. Recommended high-yield pairings:",
        "",
        "| Strategy | Driver Harness & Model (T2) | Reviewer Harness & Model (T3) | Key Advantage |",
        "|---|---|---|---|",
        "| **Pi + Claude Frontier** | Pi CLI (`pi.dev`) / Sonnet | Codex / OpenAI o1 or o3-mini | Minimalist four-tool driver paired with deep invariant auditor. |",
        "| **Western Frontier** | Claude Code / Claude 3.7 Sonnet | Codex or Pi / OpenAI o1 or o3-mini | Full corporate independence; catches subtle logic defects. |",
        "| **Hybrid High-Yield** | Claude Code / Claude 3.7 Sonnet | Cline or Pi / DeepSeek R1 | High-capability implementation paired with low-cost open reasoning. |",
        "| **Budget Maximizer** | Pi or OpenCode / DeepSeek V3 | Pi (`--tools read,grep`) / DeepSeek R1 | 80–90% cost reduction with enforced read-only independent review. |",
        ""
    ])

    return "\n".join(md_lines)


# ---------------------------------------------------------------------------
# Harness Parameters
# ---------------------------------------------------------------------------

def validate_harnesses(data: dict) -> list[str]:
    errors = []
    if "harnesses" not in data or not isinstance(data["harnesses"], list):
        errors.append("Harness data must contain a 'harnesses' list.")
        return errors

    seen_ids = set()
    for idx, h in enumerate(data["harnesses"]):
        hid = h.get("id")
        if not hid or not isinstance(hid, str):
            errors.append(f"Harness at index {idx} missing 'id'.")
            continue
        if hid in seen_ids:
            errors.append(f"Duplicate harness id: {hid}")
        seen_ids.add(hid)

        if not h.get("name"):
            errors.append(f"Harness '{hid}' missing 'name'.")

        # Check presets if present
        presets = h.get("tier_presets", {})
        if presets:
            for t_key, preset in presets.items():
                if not isinstance(preset, dict):
                    errors.append(f"Harness '{hid}' preset '{t_key}' must be an object.")
    return errors


def render_harnesses_markdown(data: dict) -> str:
    snapshot = data.get("snapshot_date", date.today().isoformat())
    harnesses = data.get("harnesses", [])

    md_lines = [
        "# Agent Harness Invocation & Parameter Reference",
        "",
        f"**Snapshot Date:** {snapshot}  ",
        "**Scope:** Definitive command templates, CLI flags, internal agent primitives, and parameter constraints for major agent harnesses to eliminate trial-and-error model selection.",
        "",
        "Use this reference to construct execution commands and to bind the harness roster in [execution-policy.template.md](../assets/execution-policy.template.md).",
        "",
        "## Operating Rules",
        "",
        "1. **Snapshot first, then verify:** Take flags from this table. When a command fails, or the snapshot date above is more than 90 days old, confirm the flag with the harness's `--help` or the provider's documentation, and report the difference so the snapshot can be refreshed.",
        "2. **Run non-interactively:** Start background subagents with the harness's non-interactive form (`-p`, `--message`, `--headless`, `exec`) so the CLI cannot block on a prompt, and grant only the permission the role needs (see each card's constraints). Provider reasoning-parameter rules live in the Direct Provider API card.",
        "",
        "## Harness Reference Cards",
        ""
    ]

    for h in harnesses:
        hid = h.get("id")
        name = h.get("name")
        htype = h.get("type", "cli")
        binary = h.get("binary")
        install = h.get("install")

        md_lines.append(f"### {name} (`{hid}`)")
        md_lines.append("")
        if binary:
            md_lines.append(f"- **Binary:** `{binary}`")
        if install:
            md_lines.append(f"- **Installation:** `{install}`")
        if h.get("website"):
            md_lines.append(f"- **Website:** {h.get('website')}")
        md_lines.append(f"- **Type:** `{htype}`")
        md_lines.append("")

        # Flags or schema
        flags = h.get("flags")
        if flags:
            md_lines.append("**Key CLI Flags:**")
            md_lines.append("")
            md_lines.append("| Purpose | Flag Syntax |")
            md_lines.append("|---|---|")
            for flag_purpose, syntax in flags.items():
                md_lines.append(f"| `{flag_purpose}` | `{syntax.replace('|', chr(92) + '|')}` |")
            md_lines.append("")

        # Tier presets
        presets = h.get("tier_presets")
        if presets:
            md_lines.append("**Operational Tier Presets (Copy-Pasteable):**")
            md_lines.append("")
            for tier_name, preset in presets.items():
                role = preset.get("role", "")
                role_str = f" (`{role}`)" if role else ""
                md_lines.append(f"- **{tier_name}{role_str}:**")
                if "command_template" in preset:
                    md_lines.append(f"  ```bash\n  {preset['command_template']}\n  ```")
                elif "example_call" in preset:
                    md_lines.append(f"  ```python\n  {preset['example_call']}\n  ```")
                elif "config_snippet" in preset:
                    snippet_json = json.dumps(preset["config_snippet"], indent=4)
                    md_lines.append(f"  ```json\n{snippet_json}\n  ```")
            md_lines.append("")

        # Constraints
        prohibitions = h.get("prohibitions", [])
        if prohibitions:
            md_lines.append("**Constraints:**")
            md_lines.append("")
            for p in prohibitions:
                md_lines.append(f"- {p}")
            md_lines.append("")

        # API rules
        rules = h.get("rules", [])
        if rules:
            md_lines.append("**Provider API Parameter Rules:**")
            md_lines.append("")
            for r in rules:
                md_lines.append(f"- **{r['provider'].capitalize()}:** {r['rule']}")
            md_lines.append("")

    return "\n".join(md_lines)


# ---------------------------------------------------------------------------
# CLI Actions
# ---------------------------------------------------------------------------

def update_price(model_id: str, in_usd: float, out_usd: float, cache_usd: float | None = None) -> bool:
    data = load_json(MODELS_JSON_PATH)
    found = False
    for m in data.get("models", []):
        if m.get("id") == model_id:
            m["pricing_per_1m"]["input_usd"] = in_usd
            m["pricing_per_1m"]["output_usd"] = out_usd
            if cache_usd is not None:
                m["pricing_per_1m"]["cache_read_usd"] = cache_usd
            found = True
            break

    if not found:
        print(f"Error: Model id '{model_id}' not found in catalog.", file=sys.stderr)
        return False

    data["snapshot_date"] = date.today().isoformat()
    errors = validate_models(data)
    if errors:
        for err in errors:
            print(f"Validation error: {err}", file=sys.stderr)
        return False

    save_json(data, MODELS_JSON_PATH)
    rendered = render_models_markdown(data)
    with open(MODELS_MD_PATH, "w", encoding="utf-8") as f:
        f.write(rendered)
    print(f"Updated pricing for '{model_id}' and re-rendered {MODELS_MD_PATH}")
    return True


def check_staleness(max_days: int = 90) -> int:
    exit_code = 0
    for label, path in [("Model catalog", MODELS_JSON_PATH), ("Harness parameters", HARNESS_JSON_PATH)]:
        if not os.path.isfile(path):
            continue
        data = load_json(path)
        snap_str = data.get("snapshot_date")
        if not snap_str:
            print(f"{label} has no snapshot_date.", file=sys.stderr)
            exit_code = 1
            continue
        snap_date = datetime.strptime(snap_str, "%Y-%m-%d").date()
        days_old = (date.today() - snap_date).days
        if days_old > max_days:
            print(f"STALE: {label} snapshot is {days_old} days old (limit {max_days} days).", file=sys.stderr)
            exit_code = 1
        else:
            print(f"OK: {label} snapshot is {days_old} days old (within {max_days} days).")
    return exit_code


def main() -> int:
    parser = argparse.ArgumentParser(description="Model and Harness Catalog Maintenance Tool")
    parser.add_argument("--validate", action="store_true", help="Validate models and harness schemas.")
    parser.add_argument("--render", action="store_true", help="Re-render all markdown reference files.")
    parser.add_argument("--update-price", nargs="+", metavar="ARG", help="<model_id> <in_usd> <out_usd> [<cache_usd>]")
    parser.add_argument("--check-staleness", nargs="?", const=90, type=int, help="Check if snapshots exceed N days.")

    args = parser.parse_args()

    if not any([args.validate, args.render, args.update_price, args.check_staleness is not None]):
        parser.print_help()
        return 0

    # Validation
    if args.validate:
        has_error = False
        if os.path.isfile(MODELS_JSON_PATH):
            m_data = load_json(MODELS_JSON_PATH)
            m_errs = validate_models(m_data)
            if m_errs:
                has_error = True
                print("Model catalog validation FAILED:")
                for e in m_errs:
                    print(f"  - {e}")
            else:
                print("Model catalog validation PASSED.")

        if os.path.isfile(HARNESS_JSON_PATH):
            h_data = load_json(HARNESS_JSON_PATH)
            h_errs = validate_harnesses(h_data)
            if h_errs:
                has_error = True
                print("Harness parameters validation FAILED:")
                for e in h_errs:
                    print(f"  - {e}")
            else:
                print("Harness parameters validation PASSED.")

        if has_error:
            return 1

    if args.update_price:
        args_len = len(args.update_price)
        if args_len < 3:
            print("Usage: --update-price <model_id> <input_usd> <output_usd> [<cache_read_usd>]", file=sys.stderr)
            return 1
        mid = args.update_price[0]
        in_p = float(args.update_price[1])
        out_p = float(args.update_price[2])
        cache_p = float(args.update_price[3]) if args_len > 3 else None
        ok = update_price(mid, in_p, out_p, cache_p)
        if not ok:
            return 1

    if args.render:
        if os.path.isfile(MODELS_JSON_PATH):
            m_data = load_json(MODELS_JSON_PATH)
            m_errs = validate_models(m_data)
            if m_errs:
                print("Cannot render models: validation failed.", file=sys.stderr)
                return 1
            rendered_m = render_models_markdown(m_data)
            with open(MODELS_MD_PATH, "w", encoding="utf-8") as f:
                f.write(rendered_m)
            print(f"Rendered {MODELS_MD_PATH} successfully.")

        if os.path.isfile(HARNESS_JSON_PATH):
            h_data = load_json(HARNESS_JSON_PATH)
            h_errs = validate_harnesses(h_data)
            if h_errs:
                print("Cannot render harnesses: validation failed.", file=sys.stderr)
                return 1
            rendered_h = render_harnesses_markdown(h_data)
            with open(HARNESS_MD_PATH, "w", encoding="utf-8") as f:
                f.write(rendered_h)
            print(f"Rendered {HARNESS_MD_PATH} successfully.")

    if args.check_staleness is not None:
        return check_staleness(args.check_staleness)

    return 0


if __name__ == "__main__":
    sys.exit(main())
