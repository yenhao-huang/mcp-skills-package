# Cron Config Reference

Use this reference before editing cron task folders or
`.codex/hooks/do-cron-tasks.py`.

## Active Files

```text
.codex/hooks/do-cron-tasks.py
.codex/hooks.json
.codex/skills/operations/set-daily-cron/references/tasks/
```

The package source lives under:

```text
mcp-skills-package/hooks/do-cron-tasks.py
mcp-skills-package/hooks.json
mcp-skills-package/skills/set-daily-cron/references/tasks/
```

Keep the package source and installed `.codex` copy behaviorally aligned.

## Runner Workflow

The hook runner must:

1. Derive the project root from the hook file location:
   `.codex/hooks/do-cron-tasks.py` -> project root. Do not use `/workspace`,
   payload `cwd`, or container mount names as the source of truth for the task
   root.
2. Find `.codex/skills/operations/set-daily-cron/references/tasks/*/task.py` under that
   hook-derived project root.
3. Treat each task folder as self-contained with `config.json`, `state.json`,
   and `reports/`.
4. Dynamically import `task.py`.
5. Call the fixed task interface:

```python
def should_run(config: dict, state: dict, context: dict) -> bool:
    ...

def run(config: dict, state: dict, context: dict) -> dict:
    ...
```

`run()` returns the next state fragment for that task. The runner writes the
merged state back to the same task folder's `state.json`.

## Task Folder Contract

Each cron task uses this layout:

```text
references/tasks/<task-name>/
├── task.py
├── config.json
├── state.json
└── reports/
```

Fields:

- `config.json`: Static task configuration such as `enabled`,
  `interval_hours`, and task-specific options.
- `state.json`: Mutable task state such as `last_run_at`, `last_report`, and
  `last_result`.
- `reports/`: Generated reports for that task only.

An enabled task should run when:

- `last_run_at` is empty.
- `last_run_at` is older than `interval_hours`.
- `last_report` is empty or points to a missing file.

## Supported Task Types

`references/tasks/git-commit/task.py` tracks a configured remote branch and
records:

- Remote fetch target and branch.
- Previous remote head/base and current remote head.
- New commits in the selected compare range.
- Diff stat and changed files.
- Insight about why those commits were likely added.
- Implementation risks inferred from changed areas.

## Validation

Syntax check:

```bash
python3 -m py_compile .codex/hooks/do-cron-tasks.py
```

Run the hook manually:

```bash
printf '{"cwd":"/any/path","hook_event_name":"SessionStart"}' | python3 .codex/hooks/do-cron-tasks.py
```

List reports:

```bash
find .codex/skills/operations/set-daily-cron/references/tasks/git-commit/reports -maxdepth 1 -type f -printf '%f\n' | sort
```
