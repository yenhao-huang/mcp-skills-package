#!/usr/bin/env python3
"""Prepare a Remote SSH workspace and optionally request a connected VS Code UI."""
import argparse
import json
import os
import re
import shlex
import shutil
import socket
import subprocess
import sys
from pathlib import Path, PurePosixPath
from urllib.parse import quote


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project")
    parser.add_argument(
        "--path", required=True,
        help="Absolute directory resolved from the current conversation",
    )
    parser.add_argument("--host")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--launch", action="store_true")
    args = parser.parse_args()
    registry = json.loads((Path(__file__).parent.parent / "projects.json").read_text())
    defaults = registry.get(args.project.lower(), {})
    host = args.host or defaults.get("host")
    path = args.path
    if not host or not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.-]*", host):
        parser.error("Provide a valid desktop SSH host alias")
    if (
        not path
        or not path.startswith("/")
        or any(c in path for c in "\n\r\0")
        or ".." in PurePosixPath(path).parts
    ):
        parser.error("Provide an absolute remote POSIX directory without traversal")
    if not re.fullmatch(r"[A-Za-z0-9_-]+", args.project):
        parser.error("Invalid project name")
    authority = "ssh-remote+" + host
    uri = "vscode-remote://" + authority + quote(path, safe="/")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    workspace = args.output_dir / (args.project + ".code-workspace")
    contents = (
        json.dumps({"folders": [{"name": args.project, "uri": uri}]}, indent=2) + "\n"
    )
    if workspace.exists() and workspace.read_text() != contents:
        parser.error(
            "Workspace exists with different content; choose a new output directory"
        )
    workspace.write_text(contents)
    command = ["code", "--new-window", "--remote", authority, path]
    result = {
        "host": host,
        "path": path,
        "workspace": str(workspace.resolve()),
        "desktop_argv": command,
        "desktop_command": shlex.join(command),
        "status": "prepared",
        "reason": "Launch not requested",
    }
    if args.launch:
        code = shutil.which("code")
        ipc = os.environ.get("VSCODE_IPC_HOOK_CLI")
        if ipc:
            try:
                with socket.socket(socket.AF_UNIX) as probe:
                    probe.settimeout(1)
                    probe.connect(ipc)
            except OSError:
                ipc = None
        if ipc and not code:
            candidates = list(
                (Path.home() / ".vscode-server/cli/servers").glob(
                    "*/server/bin/remote-cli/code"
                )
            )
            if candidates:
                code = str(
                    max(candidates, key=lambda candidate: candidate.stat().st_mtime)
                )
        desktop = sys.platform in ("darwin", "win32") or bool(
            os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")
        )
        if code and (ipc or desktop):
            try:
                proc = subprocess.run(
                    [code, *command[1:]], capture_output=True, text=True, timeout=30
                )
                result.update(
                    status=(
                        "launch_requested" if proc.returncode == 0 else "launch_failed"
                    ),
                    returncode=proc.returncode,
                    reason=proc.stderr.strip(),
                )
            except (OSError, subprocess.TimeoutExpired) as exc:
                result.update(status="launch_failed", reason=type(exc).__name__)
        else:
            result["reason"] = (
                "No desktop code CLI or inherited live VS Code client bridge; run desktop_command on your computer."
            )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
