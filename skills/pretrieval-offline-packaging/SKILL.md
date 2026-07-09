---
name: pretrieval-offline-packaging
description: >
  Package the PRetrieval system into the official offline deployment bundle.
  Use when the user asks to package the current PRetrieval system, build an
  air-gapped/offline release, create a pretrieval-offline bundle, or record and
  validate the PRetrieval packaging process.
---

# PRetrieval Offline Packaging

Use this skill to build the official PRetrieval offline deployment bundle from
the current workspace and validate that it is transferable.

## When To Use

Use this skill when the user asks to:

- Package the current PRetrieval system.
- Build or rebuild `dist/pretrieval-offline*`.
- Create an air-gapped/offline release bundle.
- Validate bundle images, checksum, or release scaffolding.
- Record the PRetrieval packaging process as an agent skill.

Do not use this skill when:

- The user only wants to deploy an existing bundle on a remote host.
- The user wants destructive end-to-end ingestion validation; use the deploy
  end-to-end workflow for that.
- Docker is unavailable and the user only wants static documentation.

## Workflow

1. Inspect the environment before changing anything:
   - `docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'`
   - `docker images --format '{{.Repository}}:{{.Tag}} {{.ID}} {{.Size}}'`
   - `git status --short --untracked-files=all`
   - `git rev-parse --short HEAD`
2. Read the official packaging files:
   - `deploy/build-bundle.sh`
   - `deploy/RUNBOOK.md`
   - `docker-compose.yaml`
   - `docker-compose.offline.yaml`
   - `Dockerfile`
   - `web/Dockerfile`
   - `tools/docker/postgres-psql-bm25s/Dockerfile`
3. If changing Docker bind paths or remote deployment paths, read
   `docs/docker-host-mounts.md` first.
4. Check build-context size before packaging:
   - `du -h -d 1 . 2>/dev/null | sort -h | tail -20`
   - confirm root `.dockerignore` and `web/.dockerignore` exist
   - root Docker context should exclude local envs, data, dist, deprecated
     outputs, and git history
5. Build the bundle with a timestamped output directory:
   - `OUT_DIR=dist/pretrieval-offline-$(date -u +%Y%m%dT%H%M%SZ) bash deploy/build-bundle.sh`
   - keep the default `TARGET_PLATFORM=linux/amd64` unless the target runtime is
     explicitly different
6. Capture the official script output:
   - app images built: `pretrieval-api`, `pretrieval-frontend`,
     `pretrieval-postgres18-bm25s`
   - pulled image: `qdrant/qdrant:v1.16.1`
   - output directory and `pretrieval-offline-images.tar.gz` size
7. Validate the bundle:
   - `sha256sum -c pretrieval-offline-images.tar.gz.sha256`
   - `du -sh <out-dir> <out-dir>/pretrieval-offline-images.tar.gz`
   - `docker image inspect pretrieval-api pretrieval-frontend pretrieval-postgres18-bm25s qdrant/qdrant:v1.16.1 --format '{{.RepoTags}} {{.Id}} {{.Architecture}} {{.Size}}'`
   - `find <out-dir> -maxdepth 2 -type f -printf '%p\t%k KB\n' | sort`
8. Record the result in the response:
   - bundle path
   - image IDs and architecture
   - checksum result
   - source commit and whether the worktree was dirty
   - any packaging-only changes made to make the bundle complete

## Environment

- Docker Engine and Docker Compose v2 are required.
- Network access is required on the build machine for Python packages,
  Docling/NLTK model downloads, `psql_bm25s` clone, and Qdrant pull.
- The offline remote does not rebuild images; it only loads the tarball and
  follows the bundled `RUNBOOK.md`.
- The official bundle script defaults to `OUT_DIR=dist/pretrieval-offline`.
  Prefer a timestamped `OUT_DIR` to preserve previous bundles.

## Rules

- Use `deploy/build-bundle.sh` as the source of truth; do not hand-roll
  `docker save` unless that script is missing or blocked.
- Preserve unrelated user changes. A dirty worktree is allowed, but report it
  because the bundle includes current workspace source.
- Do not deploy, reset databases, remove containers, or change running stacks
  unless the user explicitly asks.
- Do not push or upload the bundle unless the user explicitly asks.
- If Docker build context starts including multi-GB local state, stop and fix
  `.dockerignore` before retrying.
- If architecture validation fails, stop and report the mismatch instead of
  producing a remote-broken bundle.

## Output

Final responses should include:

- Bundle path and total size.
- Checksum validation result.
- Image tags, image IDs, and architecture.
- Source commit and dirty-worktree note.
- Any files changed to support packaging.
- Clear next command for transfer or remote verification, if relevant.
