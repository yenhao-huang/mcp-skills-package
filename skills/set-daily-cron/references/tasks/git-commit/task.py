"""Daily remote commit insight tracker task."""

from __future__ import annotations

import datetime as dt
import subprocess
from pathlib import Path


def parse_time(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    try:
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        return dt.datetime.fromisoformat(value).astimezone(dt.UTC)
    except ValueError:
        return None


def command(cmd: list[str], cwd: Path, timeout: int = 60) -> tuple[int, str]:
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return 1, str(exc)
    return proc.returncode, proc.stdout.strip()


def should_run(config: dict, state: dict, context: dict) -> bool:
    if not config.get("enabled", True):
        return False

    if not state.get("last_remote_head"):
        return True

    now = context["now"]
    interval_hours = int(config.get("interval_hours") or 24)
    last_run = parse_time(state.get("last_run_at"))
    if last_run is None:
        return True
    if now - last_run >= dt.timedelta(hours=interval_hours):
        return True

    last_report = state.get("last_report")
    if not last_report:
        return True

    task_dir = Path(context["task_dir"])
    report_path = Path(str(last_report))
    if not report_path.is_absolute():
        report_path = task_dir / report_path
    return not report_path.is_file()


def remote_exists(project_dir: Path, remote_name: str) -> bool:
    code, _ = command(["git", "remote", "get-url", remote_name], project_dir, timeout=10)
    return code == 0


def fetch_remote(project_dir: Path, config: dict) -> tuple[str, str, str]:
    remote_name = str(config.get("remote_name") or "upstream")
    remote_url = str(config.get("remote_url") or "")
    remote_branch = str(config.get("remote_branch") or "main")

    if remote_url:
        code, output = command(["git", "fetch", "--no-tags", remote_url, remote_branch], project_dir, timeout=120)
        if code != 0:
            raise RuntimeError(f"git fetch {remote_url} {remote_branch} failed: {output}")
        return remote_url, remote_branch, "FETCH_HEAD"

    if remote_exists(project_dir, remote_name):
        code, output = command(["git", "fetch", remote_name, remote_branch], project_dir, timeout=120)
        if code != 0:
            raise RuntimeError(f"git fetch {remote_name} {remote_branch} failed: {output}")
        return remote_name, remote_branch, f"{remote_name}/{remote_branch}"

    raise RuntimeError(f"remote {remote_name!r} not found and remote_url is empty")


def rev_parse(project_dir: Path, ref: str) -> str:
    code, output = command(["git", "rev-parse", ref], project_dir, timeout=10)
    if code != 0 or not output:
        raise RuntimeError(f"git rev-parse {ref} failed: {output}")
    return output.splitlines()[-1].strip()


def commit_count(project_dir: Path, commit_range: str) -> int:
    code, output = command(["git", "rev-list", "--count", commit_range], project_dir, timeout=20)
    if code != 0 or not output:
        return 0
    try:
        return int(output.strip())
    except ValueError:
        return 0


def output(project_dir: Path, cmd: list[str], timeout: int = 30) -> str:
    code, text = command(cmd, project_dir, timeout=timeout)
    if code != 0:
        return f"ERROR exit {code}: {text}"
    return text or "(none)"


def changed_paths(project_dir: Path, commit_range: str) -> list[str]:
    code, text = command(["git", "diff", "--name-only", commit_range], project_dir, timeout=30)
    if code != 0 or not text:
        return []
    return [line.strip() for line in text.splitlines() if line.strip()]


def infer_themes(paths: list[str], subjects: list[str]) -> list[str]:
    joined_paths = "\n".join(paths)
    joined_subjects = "\n".join(subjects).lower()
    themes: list[str] = []

    def add(condition: bool, text: str) -> None:
        if condition:
            themes.append(text)

    add(
        "ingest" in joined_paths or "ingestion" in joined_subjects or "ocr" in joined_subjects,
        "Ingestion/OCR state correctness: commits likely prevent long OCR drain work from being reported as stuck, idle, or completed too early.",
    )
    add(
        "preview" in joined_paths or "preview" in joined_subjects,
        "Preview integration: commits likely make generated preview artifacts and direct preview content easier to consume from external clients.",
    )
    add(
        "web/src/pages/OpsPage" in joined_paths or "audit" in joined_paths,
        "Operations observability: commits move detailed file/page/slow-path inspection into Ops-oriented APIs and UI.",
    )
    add(
        "deploy/" in joined_paths or "docker-compose" in joined_paths or "env.example" in joined_paths,
        "Deployment configurability: commits likely expose runtime knobs that were previously hard-coded or missing from offline deployment surfaces.",
    )
    add(
        "state/engine.py" in joined_paths or "DB_POOL" in joined_subjects,
        "Database pool tuning: commits likely address concurrent ingestion/API pressure by making SQLAlchemy pool sizing configurable.",
    )
    add(
        "pollingController" in joined_paths,
        "Frontend polling reliability: commits likely restart polling loops after idle-stop so active work is not missed.",
    )
    add(
        "openspec/" in joined_paths,
        "Specification alignment: commits include OpenSpec artifacts so implementation and expected behavior stay auditable.",
    )

    return themes or ["No clear theme inferred from paths/subjects; inspect individual diffs before implementation."]


def infer_risks(paths: list[str]) -> list[str]:
    joined = "\n".join(paths)
    risks: list[str] = []

    def add(condition: bool, text: str) -> None:
        if condition:
            risks.append(text)

    add(
        "scripts/api/schemas.py" in joined or "web/src/api/client.ts" in joined,
        "API contract drift: backend schemas and frontend TypeScript types must land together or UI code may read missing fields.",
    )
    add(
        "scripts/api/routers/audit.py" in joined,
        "Audit SQL complexity: page/job time windows and pagination may need index checks and re-ingest edge-case tests.",
    )
    add(
        "scripts/api/services/ingestion.py" in joined,
        "Status semantics: intake progress, conversion progress, and OCR slow-path activity must not be collapsed into one completed/pending number.",
    )
    add(
        "scripts/api/routers/preview.py" in joined or "preview_artifacts.py" in joined,
        "Preview compatibility: old ingested files may not have newly required preview artifacts, so fallback or rebuild behavior must be verified.",
    )
    add(
        "deploy/" in joined or "docker-compose" in joined or "env.example" in joined,
        "Deployment rollout: new env vars need compose, offline render config, examples, and actual host values kept in sync.",
    )
    add(
        "web/src/" in joined,
        "Frontend behavior: polling and page layout changes should be tested under idle, active OCR drain, failure, and empty-state scenarios.",
    )

    return risks or ["No specific implementation risks inferred; still review tests and changed files before merging."]


def commit_subjects(project_dir: Path, commit_range: str) -> list[str]:
    code, text = command(["git", "log", "--reverse", "--format=%s", commit_range], project_dir, timeout=30)
    if code != 0 or not text:
        return []
    return [line.strip() for line in text.splitlines() if line.strip()]


def section(title: str, body: str) -> str:
    return f"## {title}\n\n{body.strip()}\n"


def fenced(value: str, language: str = "text") -> str:
    return f"```{language}\n{value.strip()}\n```"


def run(config: dict, state: dict, context: dict) -> dict:
    project_dir = Path(context["project_dir"])
    task_dir = Path(context["task_dir"])
    now = context["now"]
    reports_dir = task_dir / str(config.get("reports_dir") or "reports")
    reports_dir.mkdir(parents=True, exist_ok=True)

    remote_label, remote_branch, remote_ref = fetch_remote(project_dir, config)
    remote_head = rev_parse(project_dir, remote_ref)
    base_ref = state.get("last_remote_head") or config.get("initial_compare_base") or "HEAD"
    commit_range = f"{base_ref}..{remote_ref}"
    count = commit_count(project_dir, commit_range)

    stamp = now.strftime("%Y%m%d-%H%M%S")
    prefix = str(config.get("report_filename_prefix") or "remote-commit-insight")
    report_path = reports_dir / f"{stamp}-{prefix}.md"

    paths = changed_paths(project_dir, commit_range) if count else []
    subjects = commit_subjects(project_dir, commit_range) if count else []
    themes = infer_themes(paths, subjects)
    risks = infer_risks(paths)

    if count:
        commit_log = output(
            project_dir,
            [
                "git",
                "log",
                "--reverse",
                "--date=iso",
                "--pretty=format:%h %s%n  author: %an%n  date: %ad",
                commit_range,
            ],
            timeout=60,
        )
    else:
        commit_log = "No new commits in the selected range."

    if count:
        diff_stat = output(project_dir, ["git", "diff", "--stat", commit_range], timeout=60)
        shortstat = output(project_dir, ["git", "diff", "--shortstat", commit_range], timeout=60)
        name_status = output(project_dir, ["git", "diff", "--name-status", commit_range], timeout=60)
    else:
        diff_stat = "No file changes."
        shortstat = "No changes."
        name_status = "No changed files."

    sections = [
        f"# Remote Commit Insight Report\n\nGenerated at: {now.isoformat()}\n",
        section(
            "Tracking Target",
            "\n".join(
                [
                    f"- Remote: `{remote_label}`",
                    f"- Branch: `{remote_branch}`",
                    f"- Remote ref: `{remote_ref}`",
                    f"- Previous remote head/base: `{base_ref}`",
                    f"- Current remote head: `{remote_head}`",
                    f"- Compare range: `{commit_range}`",
                    f"- New commits: `{count}`",
                ]
            ),
        ),
        section("Insight: Why These Commits Were Added", "\n".join(f"- {item}" for item in themes)),
        section("Implementation Risks", "\n".join(f"- {item}" for item in risks)),
        section("Commit List", fenced(commit_log)),
        section("Change Size", fenced(shortstat + "\n\n" + diff_stat)),
        section("Changed Files", fenced(name_status)),
    ]
    report_path.write_text("\n".join(sections), encoding="utf-8")

    return {
        "last_run_at": now.isoformat(),
        "last_remote_head": remote_head,
        "last_compare_base": str(base_ref),
        "last_compare_range": commit_range,
        "last_new_commit_count": count,
        "last_report": str(report_path.relative_to(task_dir)),
        "last_result": {
            "report": str(report_path),
            "remote_head": remote_head,
            "new_commit_count": count,
        },
    }
