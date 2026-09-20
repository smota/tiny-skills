# Maintenance

Maintainer-only material, one directory per skill: behavioral evals, refresh procedures, and the generators behind a skill's reference files. It sits outside `skills/` so a skill install carries only what agents read or run.

| Directory | Contents |
|---|---|
| `project-init/` | `evals.md`; `model-catalog-refresh.md` and `harness-parameters-refresh.md` procedures; `refresh_model_catalog.py`, which validates the JSON data here and renders `skills/software-engineering/project-init/references/model-catalog.md` and `harness-parameters.md` |
| `agent-refine/` | `evals.md` |
| `release-notes/` | `evals.md` |
| `techlead-planner/` | `evals.md` |

Run scripts from the repository root, for example `python maintenance/project-init/refresh_model_catalog.py --validate`.
