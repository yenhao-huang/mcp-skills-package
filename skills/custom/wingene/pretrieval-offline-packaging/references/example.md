# Example Run Notes

This example records the 2026-07-09 packaging run.

## Commands

```bash
du -h -d 1 . 2>/dev/null | sort -h | tail -20
OUT_DIR=dist/pretrieval-offline-20260709T024812Z bash deploy/build-bundle.sh
cd dist/pretrieval-offline-20260709T024812Z
sha256sum -c pretrieval-offline-images.tar.gz.sha256
docker image inspect pretrieval-api pretrieval-frontend pretrieval-postgres18-bm25s qdrant/qdrant:v1.16.1 --format '{{.RepoTags}} {{.Id}} {{.Architecture}} {{.Size}}'
```

## Observed Evidence

- First attempt was stopped after Docker tried to send more than 7GB of build
  context from `deprecated/exp/...` backup files.
- Adding root `.dockerignore` and `web/.dockerignore` reduced root context to
  about 107KB at the beginning of the rebuild and frontend context to about
  55MB.
- Final output: `dist/pretrieval-offline-20260709T024812Z`.
- Final tarball: `pretrieval-offline-images.tar.gz`, about 4.6GB.
- Checksum: `pretrieval-offline-images.tar.gz: OK`.
- Images were amd64:
  - `pretrieval-api:latest`
  - `pretrieval-frontend:latest`
  - `pretrieval-postgres18-bm25s:latest`
  - `qdrant/qdrant:v1.16.1`
