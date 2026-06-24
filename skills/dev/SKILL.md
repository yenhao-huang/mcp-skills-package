---
name: dev
description: Use for software development tasks, especially when the user asks to design, implement, debug, test, refactor, benchmark, or run experiments. Always apply the Superpowers design/develop/test workflow, always read this skill's bundled references/convention.md, strictly follow its File Tree unless an existing project convention explicitly overrides it, and use ralph-loop for experiment iteration when experiments, benchmarks, ablations, or uncertain technical choices are involved.
---

# Dev

Use this skill for coding work and engineering experiments.

## Required Habits

1. Always read this skill's bundled `references/convention.md` before changing code. Also read the target project's `references/convention.md` when it exists.
2. Use Superpowers for the development workflow:
   - `design`: clarify the target behavior, constraints, risks, and smallest useful implementation.
   - `develop`: make scoped changes that fit the existing codebase and `references/convention.md`.
   - `test`: run the most relevant validation and report what passed or could not be run.
3. When creating a new project, scaffold it from the active `File Tree` before adding feature code. A new project must comply with the active `File Tree` from its first committed/finished state, not only after later cleanup.
4. Use `ralph-loop` for experiments:
   - Use it when the task involves experiments, benchmarks, ablations, model/data comparisons, hyperparameters, performance tuning, or uncertain technical choices.
   - Treat each loop as: hypothesis -> command/config -> result -> decision -> next loop.
   - Keep experiment outputs reproducible by recording commands, changed configs, inputs, metrics, and artifacts.
   - Stop when the result answers the question, the next step is blocked, or the user-provided budget is reached.

## Workflow

### Convention

- Before Superpowers `design`, read this skill's bundled `references/convention.md`. Treat its `File Tree` section as the default mandatory project structure.
- Also check whether `references/convention.md` exists in the target project. If it exists, read it completely enough to extract the project rules that affect the task.
- If both conventions exist, the target project's convention may override the bundled convention only when it explicitly defines a conflicting structure or rule. Otherwise, the bundled `File Tree` remains mandatory.
- For new projects, create the project using the bundled `File Tree` exactly: `data/`, `logs/`, `lib/`, `test/`, `external/`, `configs/`, `core/api/`, `core/service/`, `ui/`, `results/`, `exp/`, `docs/`, `.gitignore`, `AGENT.md`, `CLAUDE.md`, and `README.md`.
- New files and directories must be placed under the exact tree defined by the active convention unless the user explicitly asks for a different structure or the existing project already has a conflicting established structure.
- Do not create alternate top-level directories, duplicate category folders, or convenience locations that bypass the active file tree. For example, do not create generic Python `src/` or `tests/` directories when the active tree requires `core/` and `test/`.
- Carry those rules into the following `design`, `develop`, and `test` steps.

### New Project Gate

Apply this gate whenever the task is to create, open, initialize, scaffold, or set up a new project.

- Before creating files, choose the active convention: bundled `references/convention.md` by default, or a target-project convention only if it explicitly overrides the bundled tree.
- Scaffold the required top-level tree first. For the bundled convention, that means: `data/`, `logs/`, `lib/`, `test/`, `external/`, `configs/`, `core/api/`, `core/service/`, `ui/`, `results/`, `exp/`, `docs/`, `.gitignore`, `AGENT.md`, `CLAUDE.md`, and `README.md`.
- Place application logic under `core/service/`, API/CLI/routes under `core/api/`, tests under `test/`, shared helpers under `lib/`, UI code under `ui/`, configs under `configs/`, experiment code or notes under `exp/`, outputs under `results/`, and logs under `logs/`.
- Do not scaffold framework-default directories that conflict with the active tree. If a framework expects names like `src/`, `tests/`, `app/`, or `packages/`, adapt the framework configuration to the active tree instead.
- Before finishing, inspect the new project file list and remove or relocate any generated files that violate the active tree, including build metadata, caches, or framework defaults created during validation.

### Design

- Read the local context before deciding.
- Use the rules learned from the bundled convention and any target-project convention.
- Map each planned file or directory change to the documented file tree before editing.
- For new projects, state the active file tree and where the initial code, tests, configs, and README will go before editing.
- State the intended change or experiment briefly when the work is non-trivial.
- Prefer existing project conventions over new abstractions.
- Define the validation target before editing or running experiments.

### Develop

- Keep edits narrowly scoped.
- Follow the active documented file tree strictly for every new or moved file.
- For new projects, create the required tree before adding feature code and keep all subsequent files inside the matching directories.
- Preserve user changes and avoid unrelated cleanup.
- Use deterministic scripts or config files when an experiment will be repeated.
- For experiment work, isolate outputs under the project's existing output/log directory when one exists.
- For long data-processing tasks, design a checkpoint mechanism so work can resume from where it left off rather than restarting from scratch.

### Test

- Run focused tests, linters, type checks, or smoke commands that directly cover the change.
- For new projects, also validate the final file tree by listing the created files/directories and confirming they match the active convention.
- For experiments, summarize the ralph-loop table with command/config, key metric, observation, and next decision.
- If validation cannot run, report the blocker and the best available static check.

## Output Style

Final responses should include:

- What changed or what experiment was run.
- Validation results.
- For ralph-loop work, the final decision and the most relevant metric or artifact path.
