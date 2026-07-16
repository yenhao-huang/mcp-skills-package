# Filetree Rules

Use these placement rules for PRetrieval offline packaging work.

## Bundle Output

Write generated bundles under `dist/pretrieval-offline-<timestamp>/`. The
default `dist/pretrieval-offline/` path is valid, but timestamped output avoids
overwriting an earlier release.

Expected release contents include:

```text
pretrieval-offline-<timestamp>/
├── pretrieval-offline-images.tar.gz
├── pretrieval-offline-images.tar.gz.sha256
├── docker-compose.offline.yaml
├── RUNBOOK.md
├── deploy/
├── configs/
├── scripts/
├── alembic/
└── alembic.ini
```

## Source Changes

Packaging support files belong at their existing project locations:

- root `.dockerignore` for root Docker build context
- `web/.dockerignore` for frontend build context
- `.codex/skills/custom/pretrieval-offline-packaging/` for this skill

Do not commit generated `dist/` bundles.
