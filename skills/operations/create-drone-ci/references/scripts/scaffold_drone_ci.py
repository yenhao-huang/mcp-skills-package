#!/usr/bin/env python3
"""Create a conservative Gitea + Drone CI starter layout."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
from pathlib import Path
from textwrap import dedent


def normalized_project_name(repo: Path) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", repo.name.lower()).strip("-")
    return value or "repository"


def templates(project: str, with_dockerfiles: bool) -> dict[str, str]:
    generated = {
        ".drone.yml": dedent("""\
            kind: pipeline
            type: docker
            name: ci

            platform:
              os: linux
              arch: amd64

            steps:
              - name: test
                image: python:3.12-slim
                commands:
                  - sh .ci/scripts/ci.sh

            trigger:
              event:
                - push
                - pull_request
            """),
        ".ci/drone/compose.yaml": dedent(f"""\
            name: {project}-drone

            services:
              server:
                image: "${{DRONE_SERVER_IMAGE}}"
                container_name: {project}-drone-server
                ports:
                  - "${{DRONE_HTTP_PORT}}:80"
                environment:
                  DRONE_GITEA_SERVER: "${{DRONE_GITEA_SERVER}}"
                  DRONE_GITEA_CLIENT_ID: "${{DRONE_GITEA_CLIENT_ID}}"
                  DRONE_GITEA_CLIENT_SECRET: "${{DRONE_GITEA_CLIENT_SECRET}}"
                  DRONE_RPC_SECRET: "${{DRONE_RPC_SECRET}}"
                  DRONE_SERVER_HOST: "${{DRONE_SERVER_HOST}}"
                  DRONE_SERVER_PROTO: "${{DRONE_SERVER_PROTO}}"
                volumes:
                  - drone-data:/data
                restart: unless-stopped

              runner:
                image: "${{DRONE_RUNNER_IMAGE}}"
                container_name: {project}-drone-runner
                depends_on:
                  - server
                environment:
                  DRONE_RPC_PROTO: http
                  DRONE_RPC_HOST: server
                  DRONE_RPC_SECRET: "${{DRONE_RPC_SECRET}}"
                  DRONE_RUNNER_NAME: "${{DRONE_RUNNER_NAME}}"
                  DRONE_RUNNER_CAPACITY: "${{DRONE_RUNNER_CAPACITY}}"
                volumes:
                  - /var/run/docker.sock:/var/run/docker.sock
                restart: unless-stopped

            volumes:
              drone-data:
            """),
        ".ci/drone/.env.example": dedent("""\
            DRONE_SERVER_IMAGE=drone/drone:2
            DRONE_RUNNER_IMAGE=drone/drone-runner-docker:1
            DRONE_GITEA_SERVER=https://gitea.example.com
            DRONE_GITEA_CLIENT_ID=replace-with-oauth-client-id
            DRONE_GITEA_CLIENT_SECRET=replace-with-oauth-client-secret
            DRONE_RPC_SECRET=replace-with-openssl-rand-hex-16
            DRONE_SERVER_HOST=drone.example.com
            DRONE_SERVER_PROTO=https
            DRONE_HTTP_PORT=80
            DRONE_RUNNER_NAME=replace-with-runner-name
            DRONE_RUNNER_CAPACITY=2
            """),
        ".ci/drone/CONVENTIONS.md": dedent("""\
            # Drone CI conventions

            - `.drone.yml` is the canonical repository pipeline entry point.
            - `compose.yaml` owns Drone Server and Docker Runner lifecycle.
            - `.env` contains runtime secrets and must never be committed.
            - Official Drone images are used directly by default; pin digests before production rollout.
            - Dockerfiles are optional and require a documented customization need.
            - The Docker socket makes the runner host-level trusted infrastructure.
            - Activate only reviewed repositories and restrict privileged pipelines.
            - Keep task logic in `.ci/scripts/` and its regression tests in `.ci/tests/`.
            """),
        ".ci/docs/pipeline.md": dedent("""\
            # CI pipeline

            The root `.drone.yml` runs `.ci/scripts/ci.sh` for push and pull-request events.

            Before enabling the repository:

            1. Replace the starter test command with the repository's real validation.
            2. Copy `.ci/drone/.env.example` to `.ci/drone/.env` and replace every placeholder.
            3. Create the Git provider OAuth application with `<public Drone URL>/login` as callback.
            4. Start Server and Runner with Docker Compose and inspect both logs.
            5. Sign in to Drone and activate the repository to create its webhook.

            Do not commit `.ci/drone/.env` or any pipeline secret.
            """),
        ".ci/scripts/ci.sh": dedent("""\
            #!/bin/sh
            set -eu

            python3 -m unittest discover -s .ci/tests -p 'test_*.py' -v
            """),
        ".ci/tests/test_ci_smoke.py": dedent("""\
            from pathlib import Path
            import unittest


            class DroneCiLayoutTest(unittest.TestCase):
                def test_required_ci_files_exist(self):
                    required = (
                        Path(".drone.yml"),
                        Path(".ci/drone/compose.yaml"),
                        Path(".ci/drone/.env.example"),
                        Path(".ci/docs/pipeline.md"),
                        Path(".ci/scripts/ci.sh"),
                    )
                    self.assertEqual([], [str(path) for path in required if not path.is_file()])

                def test_runtime_env_is_gitignored(self):
                    entries = Path(".gitignore").read_text(encoding="utf-8").splitlines()
                    self.assertIn(".ci/drone/.env", entries)


            if __name__ == "__main__":
                unittest.main()
            """),
    }
    if with_dockerfiles:
        generated[".ci/drone/Dockerfile.server"] = dedent("""\
            ARG DRONE_SERVER_BASE_IMAGE=drone/drone:2
            FROM ${DRONE_SERVER_BASE_IMAGE}

            # Add only documented custom CA certificates or approved extensions.
            """)
        generated[".ci/drone/Dockerfile.runner"] = dedent("""\
            ARG DRONE_RUNNER_BASE_IMAGE=drone/drone-runner-docker:1
            FROM ${DRONE_RUNNER_BASE_IMAGE}

            # Keep pipeline tooling in step images; customize the runner only when required.
            """)
    return generated


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True, type=Path, help="target repository path")
    parser.add_argument("--init-git", action="store_true", help="run git init when .git is absent")
    parser.add_argument("--with-dockerfiles", action="store_true", help="add optional image extension points")
    parser.add_argument("--force", action="store_true", help="replace generated files that already exist")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = args.repo.expanduser().resolve()
    if not repo.exists():
        if not args.init_git:
            raise SystemExit(f"target does not exist: {repo}; pass --init-git to create it")
        repo.mkdir(parents=True)
    elif not repo.is_dir():
        raise SystemExit(f"target is not a directory: {repo}")

    git_dir = repo / ".git"
    if not git_dir.exists():
        if not args.init_git:
            raise SystemExit(f"not a Git repository: {repo}; pass --init-git to initialize it")
        subprocess.run(["git", "init", str(repo)], check=True)

    generated = templates(normalized_project_name(repo), args.with_dockerfiles)
    conflicts = [path for path in generated if (repo / path).exists()]
    if conflicts and not args.force:
        joined = "\n".join(f"  - {path}" for path in conflicts)
        raise SystemExit(f"refusing to overwrite existing files; review or pass --force:\n{joined}")

    for relative, content in generated.items():
        destination = repo / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")

    os.chmod(repo / ".ci/scripts/ci.sh", 0o755)

    gitignore = repo / ".gitignore"
    ignore_entry = ".ci/drone/.env"
    existing = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    entries = existing.splitlines()
    if ignore_entry not in entries:
        separator = "" if not existing or existing.endswith("\n") else "\n"
        gitignore.write_text(f"{existing}{separator}{ignore_entry}\n", encoding="utf-8")

    print(f"Created Drone CI scaffold in {repo}")
    print("Next: review .drone.yml, populate ignored .ci/drone/.env, validate, then activate the repository in Drone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
