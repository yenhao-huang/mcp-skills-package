---
name: dev
description: Use for software development tasks, especially when the user asks to design, implement, debug, test, refactor, benchmark, or run experiments. Always apply the Superpowers design/develop/test workflow, read src/convention.md when present, and use ralph-loop for experiment iteration when experiments, benchmarks, ablations, or uncertain technical choices are involved.
---

# Dev

Use this skill for coding work and engineering experiments.

## Required Habits

1. Read `reference/convention.md` before changing code when it exists in the target project.
2. Use Superpowers for the development workflow:
   - `design`: clarify the target behavior, constraints, risks, and smallest useful implementation.
   - `develop`: make scoped changes that fit the existing codebase and `reference/convention.md`.
   - `test`: run the most relevant validation and report what passed or could not be run.
3. Use `ralph-loop` for experiments:
   - Use it when the task involves experiments, benchmarks, ablations, model/data comparisons, hyperparameters, performance tuning, or uncertain technical choices.
   - Treat each loop as: hypothesis -> command/config -> result -> decision -> next loop.
   - Keep experiment outputs reproducible by recording commands, changed configs, inputs, metrics, and artifacts.
   - Stop when the result answers the question, the next step is blocked, or the user-provided budget is reached.

## Workflow

### Convention

- Before Superpowers `design`, check whether `reference/convention.md` exists in the target project.
- If it exists, read it completely enough to extract the project rules that affect the task.
- Carry those rules into the following `design`, `develop`, and `test` steps.
- If it does not exist, continue with the normal workflow and do not invent missing conventions.

### Design

- Read the local context before deciding.
- Use the rules learned from `reference/convention.md` when it exists.
- State the intended change or experiment briefly when the work is non-trivial.
- Prefer existing project conventions over new abstractions.
- Define the validation target before editing or running experiments.

### Develop

- Keep edits narrowly scoped.
- Preserve user changes and avoid unrelated cleanup.
- Use deterministic scripts or config files when an experiment will be repeated.
- For experiment work, isolate outputs under the project's existing output/log directory when one exists.
- For long data-processing tasks, design a checkpoint mechanism so work can resume from where it left off rather than restarting from scratch.

### Test

- Run focused tests, linters, type checks, or smoke commands that directly cover the change.
- For experiments, summarize the ralph-loop table with command/config, key metric, observation, and next decision.
- If validation cannot run, report the blocker and the best available static check.

## Output Style

Final responses should include:

- What changed or what experiment was run.
- Validation results.
- For ralph-loop work, the final decision and the most relevant metric or artifact path.
