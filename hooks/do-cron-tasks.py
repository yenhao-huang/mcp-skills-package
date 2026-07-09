#!/usr/bin/env python3
"""SessionStart hook: dispatch set-daily-cron task folders when due."""

from __future__ import annotations

import datetime as dt
import hashlib
import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.UTC).replace(microsecond=0)


def load_payload() -> dict:
    if sys.stdin.isatty():
        return {}
    try:
        return json.load(sys.stdin)
    except json.JSONDecodeError:
        return {}


def hook_project_dir() -> Path:
    return Path(__file__).resolve().parents[2]


def workspace_dir_from_payload(payload: dict, project_dir: Path) -> Path:
    return hook_project_dir()


def tasks_root(workspace_dir: Path) -> Path:
    return (
        workspace_dir
        / ".codex"
        / "skills"
        / "Operations"
        / "set-daily-cron"
        / "references"
        / "tasks"
    )


def load_json(path: Path, default: dict) -> dict:
    if not path.is_file():
        return dict(default)
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return dict(default)


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def load_task_module(task_path: Path) -> ModuleType:
    digest = hashlib.sha256(str(task_path).encode("utf-8")).hexdigest()[:16]
    module_name = f"set_daily_cron_task_{digest}"
    spec = importlib.util.spec_from_file_location(module_name, task_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"cannot load task module: {task_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def dispatch_task(task_path: Path, context: dict) -> str | None:
    task_dir = task_path.parent
    config = load_json(task_dir / "config.json", {})
    state = load_json(task_dir / "state.json", {})
    if not config.get("enabled", True):
        return None

    module = load_task_module(task_path)
    if not hasattr(module, "should_run") or not hasattr(module, "run"):
        return None

    task_context = dict(context)
    task_context["task_dir"] = task_dir

    if not module.should_run(config, state, task_context):
        return None

    result = module.run(config, state, task_context)
    if not isinstance(result, dict):
        result = {}

    next_state = dict(state)
    next_state.update(result)
    write_json(task_dir / "state.json", next_state)

    last_report = next_state.get("last_report")
    if last_report:
        report_path = Path(str(last_report))
        if not report_path.is_absolute():
            report_path = task_dir / report_path
        return f"{task_dir.name}: {report_path}"
    return task_dir.name


def main() -> int:
    payload = load_payload()
    project_dir = hook_project_dir()
    workspace_dir = workspace_dir_from_payload(payload, project_dir)
    root = tasks_root(workspace_dir)
    if not root.is_dir():
        return 0

    context = {
        "now": utc_now(),
        "project_dir": project_dir,
        "workspace_dir": workspace_dir,
    }

    ran: list[str] = []
    for task_path in sorted(root.glob("*/task.py")):
        try:
            result = dispatch_task(task_path, context)
        except Exception as exc:  # Hook must not block session startup.
            result = f"{task_path.parent.name}: ERROR {exc}"
        if result:
            ran.append(result)

    if not ran:
        return 0

    json.dump(
        {
            "hookSpecificOutput": {
                "hookEventName": payload.get("hook_event_name", "SessionStart"),
                "additionalContext": "Daily cron tasks ran: " + "; ".join(ran),
            }
        },
        sys.stdout,
        ensure_ascii=False,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
