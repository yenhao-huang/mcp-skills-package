"""Create/remove a dedicated DeerFlow runtime without modifying Codex login state."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from pathlib import Path

UPSTREAM = "https://github.com/bytedance/deer-flow.git"
REVISION = "d0d66d62fae2b7cc9fb0fb814df3403397ae8831"
MARKER = ".start-deer-runtime.json"


def python_path(root: Path) -> Path:
    return root / ".venv" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def install(root: Path, source: str = UPSTREAM) -> None:
    if root.exists():
        raise FileExistsError(
            "Runtime target must be a new directory; existing state is never overwritten"
        )
    uv = shutil.which("uv")
    git = shutil.which("git")
    if not uv or not git:
        raise RuntimeError("Install uv and Git before provisioning this runtime")
    root.mkdir(parents=True)
    marker = {
        "kind": "start-deer-runtime-v1",
        "root": str(root),
        "revision": REVISION,
        "status": "installing",
        "managed": ["external", ".venv"],
    }
    (root / MARKER).write_text(json.dumps(marker, indent=2), encoding="utf-8")
    checkout = root / "external/deer-flow"
    subprocess.run([git, "clone", "--no-checkout", source, str(checkout)], check=True)
    subprocess.run(
        [git, "-C", str(checkout), "checkout", "--detach", REVISION], check=True
    )
    subprocess.run([uv, "venv", "--python", "3.12", str(root / ".venv")], check=True)
    subprocess.run(
        [
            uv,
            "pip",
            "install",
            "--python",
            str(python_path(root)),
            "-e",
            str(checkout / "backend/packages/extension-api"),
            "-e",
            str(checkout / "backend/packages/harness"),
            "pymupdf==2.0",
        ],
        check=True,
    )
    subprocess.run(
        [
            str(python_path(root)),
            "-c",
            "from deerflow.agents.factory import create_deerflow_agent; import pymupdf; print('Runtime imports OK')",
        ],
        check=True,
    )
    marker["status"] = "ready"
    (root / MARKER).write_text(json.dumps(marker, indent=2), encoding="utf-8")
    print(f"Runtime ready: {root}\nPython: {python_path(root)}")


def remove(root: Path) -> None:
    marker_path = root / MARKER
    marker = json.loads(marker_path.read_text(encoding="utf-8"))
    if marker.get("kind") != "start-deer-runtime-v1" or marker.get("root") != str(root):
        raise ValueError("Refusing to remove an unrecognized runtime")
    allowed = {"external", ".venv", MARKER}
    if any(p.name not in allowed for p in root.iterdir()):
        raise ValueError(
            "Runtime contains unrelated files; preserve them before removal"
        )
    if (root / "external").exists() and any(
        p.name != "deer-flow" for p in (root / "external").iterdir()
    ):
        raise ValueError(
            "External directory contains unrelated files; preserve them before removal"
        )
    checkout = root / "external/deer-flow"
    if checkout.exists():
        dirty = subprocess.check_output(
            ["git", "-C", str(checkout), "status", "--porcelain"], text=True
        )
        if dirty.strip():
            raise ValueError(
                "Upstream checkout has local changes; preserve them before removal"
            )
    for component in [root, root / "external", root / ".venv", checkout]:
        if component.is_symlink() or component.is_junction():
            raise ValueError("Refusing recursive removal through a link or junction")

    def writable_retry(function, path, error):
        import stat

        if not isinstance(error, PermissionError):
            raise error
        os.chmod(path, stat.S_IWRITE | stat.S_IREAD)
        function(path)

    for name in ["external", ".venv"]:
        target = root / name
        if target.exists():
            shutil.rmtree(target, onexc=writable_retry)
    marker_path.unlink()
    root.rmdir()
    print(f"Removed managed runtime: {root}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["install", "remove"])
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument(
        "--upstream-source",
        default=UPSTREAM,
        help="Git source for offline/local-mirror testing; revision remains pinned",
    )
    args = parser.parse_args()
    requested = args.workspace.expanduser().absolute()
    if requested.is_symlink() or requested.is_junction():
        parser.error("Runtime workspace must not be a symlink or junction")
    root = requested.resolve()
    if args.command == "install":
        install(root, args.upstream_source)
    else:
        remove(root)


if __name__ == "__main__":
    main()
