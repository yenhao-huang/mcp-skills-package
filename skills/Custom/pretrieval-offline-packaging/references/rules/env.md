# Environment Rules

Use these rules before building a PRetrieval offline bundle.

## Required Tools

- Docker Engine.
- Docker Compose v2, or `docker-compose` if v2 is unavailable.
- Network access on the build host.
- Enough free disk space for the built images and the gzipped tarball.

## Build Inputs

The official script builds from the current checkout and packages loose source
beside the images. A dirty worktree is allowed, but it must be reported because
the release reflects those uncommitted files.

## Target Platform

The official remote target is amd64. Keep `TARGET_PLATFORM=linux/amd64` unless
the user explicitly names another deployment target.

## Service Safety

Packaging should not start, stop, remove, or reset running services. It builds
images and writes files under `dist/`.
