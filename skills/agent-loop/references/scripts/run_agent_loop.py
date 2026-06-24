import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CONTROLLER_DIR = Path(__file__).resolve().parent
PROMPT_DIR = CONTROLLER_DIR / "prompts"
LOOPS_DIR = CONTROLLER_DIR / "loops"
DEFAULT_STATE = CONTROLLER_DIR / "state.json"
DEFAULT_LOG_DIR = CONTROLLER_DIR / "logs"
PHASES = ["plan", "develop", "experiment", "reflect"]
DAY_TIMEOUT_SECONDS = 24 * 60 * 60


def now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def loop_name(loop_id: int) -> str:
    return f"loops{loop_id:03d}"


def loop_dir(loop_id: int) -> Path:
    return LOOPS_DIR / loop_name(loop_id)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(read_text(path))


def save_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def default_state(start: int, end: int, best_artifact: str) -> dict:
    return {
        "next_loop": start,
        "target_loop": end,
        "phase": "plan",
        "current_loop": None,
        "last_completed_loop": start - 1,
        "best_artifact": best_artifact,
        "updated_at": now(),
    }


def load_or_init_state(args: argparse.Namespace) -> dict:
    if args.state.exists() and args.resume:
        state = load_json(args.state)
        state.setdefault("target_loop", args.end)
        state.setdefault("best_artifact", args.best_artifact)
        return state
    state = default_state(args.start, args.end, args.best_artifact)
    if not args.dry_run:
        save_json(args.state, state)
    return state


def update_state(args: argparse.Namespace, state: dict, **updates: object) -> dict:
    state.update(updates)
    state["updated_at"] = now()
    if not args.dry_run:
        save_json(args.state, state)
    return state


def ensure_loop_dirs(loop_id: int, dry_run: bool) -> None:
    if dry_run:
        return
    for name in ["plans", "dev", "exp", "reflect"]:
        (loop_dir(loop_id) / name).mkdir(parents=True, exist_ok=True)


def prior_plan_index(max_chars: int = 12000) -> str:
    paths = sorted(LOOPS_DIR.glob("loops[0-9][0-9][0-9]/plans/*.md"))
    lines = []
    for path in paths:
        rel = path.relative_to(ROOT)
        content = read_text(path)
        heading = next((line.strip() for line in content.splitlines() if line.strip()), "")
        novelty = ""
        for line in content.splitlines():
            if "Novelty Check" in line:
                novelty = line.strip()
                break
        lines.append(f"- {rel}: {heading} {novelty}".strip())
    text = "\n".join(lines)
    if len(text) > max_chars:
        return text[-max_chars:]
    return text


def strip_fences(text: str) -> str:
    """Remove a single outer markdown code fence if Claude wrapped its output in one."""
    stripped = text.strip()
    for lang in ("markdown", "md", ""):
        fence_open = f"```{lang}\n" if lang else "```\n"
        if stripped.startswith(fence_open) and stripped.endswith("```"):
            return stripped[len(fence_open):-3].strip()
    return stripped


def render_prompt(name: str, loop_id: int, state: dict) -> str:
    template = read_text(PROMPT_DIR / name)
    return template.format(
        loop_id=f"{loop_id:03d}",
        target_loop=f"{state['target_loop']:03d}",
        best_artifact=state.get("best_artifact", ""),
        prior_plan_index=prior_plan_index(),
    )


def command_preview(command: list[str]) -> str:
    rendered = []
    for part in command:
        if "\n" in part or len(part) > 240:
            rendered.append('"<prompt>"')
        else:
            rendered.append(part)
    return " ".join(rendered)


def run_command(
    command: list[str],
    prompt: str,
    timeout: int,
    log_path: Path,
    dry_run: bool,
) -> tuple[int, str]:
    if dry_run:
        preview = f"DRY RUN: {command_preview(command)}\n\nPROMPT:\n{prompt}\n"
        print(preview)
        return 0, preview
    log_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        proc = subprocess.run(
            command,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=ROOT,
            timeout=timeout,
            check=False,
        )
        output = proc.stdout or ""
        write_text(log_path, output)
        return proc.returncode, output
    except subprocess.TimeoutExpired as exc:
        output = f"TIMEOUT after {timeout}s\n{exc.stdout or ''}"
        write_text(log_path, output)
        return 124, output


def claude_command(prompt: str) -> list[str]:
    return ["claude", "--print", "--dangerously-skip-permissions", prompt]


def write_phase_record(loop_id: int, phase: str, body: str, dry_run: bool) -> Path:
    filenames = {
        "plan": ("plans", "agent_loop_plan"),
        "develop": ("dev", "agent_loop_dev"),
        "experiment": ("exp", "agent_loop_exp"),
    }
    subdir, stem = filenames[phase]
    path = loop_dir(loop_id) / subdir / f"{loop_id:03d}_{stem}.md"
    if not dry_run:
        write_text(path, body)
    return path


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def run_agent_phase(args: argparse.Namespace, state: dict, loop_id: int, phase: str) -> None:
    prompt_name = {
        "plan": "plan.md",
        "develop": "develop.md",
        "experiment": "experiment.md",
    }[phase]
    prompt = render_prompt(prompt_name, loop_id, state)
    log_path = args.log_dir / loop_name(loop_id) / f"{phase}.log"
    command = claude_command(prompt)
    code, output = run_command(
        command,
        prompt,
        args.timeout,
        log_path,
        args.dry_run,
    )
    if code != 0:
        raise RuntimeError(f"Claude {phase} phase failed for loop {loop_id:03d}; see {log_path}")
    record_path = write_phase_record(loop_id, phase, strip_fences(output), args.dry_run)
    print(f"{phase}: wrote {record_path.relative_to(ROOT)}")


def run_reflect(args: argparse.Namespace, state: dict, loop_id: int) -> None:
    prompt = render_prompt("reflect.md", loop_id, state)
    log_path = args.log_dir / loop_name(loop_id) / "reflect.log"
    command = claude_command(prompt)
    code, output = run_command(
        command,
        prompt,
        args.timeout,
        log_path,
        args.dry_run,
    )
    if code != 0:
        raise RuntimeError(f"Claude reflect phase failed for loop {loop_id:03d}; see {log_path}")

    path = loop_dir(loop_id) / "reflect" / f"{loop_id:03d}_agent_loop_reflect.md"
    if not args.dry_run:
        write_text(path, strip_fences(output))
    print(f"reflect: wrote {path.relative_to(ROOT)}")


def next_phase(phase: str) -> str:
    idx = PHASES.index(phase)
    if idx == len(PHASES) - 1:
        return "complete"
    return PHASES[idx + 1]


def run_once(args: argparse.Namespace, state: dict) -> bool:
    loop_id = int(state.get("current_loop") or state["next_loop"])
    target = int(state["target_loop"])
    if loop_id > target:
        print("No work: target loop already completed.")
        return False

    phase = state["phase"]
    if phase == "complete":
        update_state(
            args,
            state,
            last_completed_loop=loop_id,
            next_loop=loop_id + 1,
            current_loop=None,
            phase="plan",
        )
        print(f"completed loop {loop_id:03d}")
        return True

    ensure_loop_dirs(loop_id, args.dry_run)
    update_state(args, state, current_loop=loop_id, phase=phase)
    print(f"loop {loop_id:03d} phase={phase}")

    if phase in {"plan", "develop", "experiment"}:
        run_agent_phase(args, state, loop_id, phase)
    elif phase == "reflect":
        run_reflect(args, state, loop_id)
    else:
        raise ValueError(f"Unsupported phase: {phase}")

    update_state(args, state, current_loop=loop_id, phase=next_phase(phase))
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Checkpointed Claude agent-loop controller.")
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    parser.add_argument("--resume", action="store_true", help="Resume from state if it exists.")
    parser.add_argument("--once", action="store_true", help="Run a single phase then exit.")
    parser.add_argument("--dry-run", action="store_true", help="Print commands/prompts without executing them.")
    parser.add_argument("--state", type=Path, default=DEFAULT_STATE)
    parser.add_argument("--log-dir", type=Path, default=DEFAULT_LOG_DIR)
    parser.add_argument("--best-artifact", default="results/eval/e2e/stage4_bert_st1_codex_st4.json")
    parser.add_argument("--timeout", type=int, default=DAY_TIMEOUT_SECONDS)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    args.state = args.state if args.state.is_absolute() else ROOT / args.state
    args.log_dir = args.log_dir if args.log_dir.is_absolute() else ROOT / args.log_dir

    if args.start > args.end:
        raise ValueError("--start must be <= --end")

    state = load_or_init_state(args)
    if int(state["target_loop"]) != args.end:
        state = update_state(args, state, target_loop=args.end)

    while int(state["next_loop"]) <= int(state["target_loop"]) or state.get("current_loop"):
        progressed = run_once(args, state)
        if not progressed or args.once:
            break
        state = load_json(args.state) if args.state.exists() and not args.dry_run else state

    return 0


if __name__ == "__main__":
    sys.exit(main())
