# Install nsys/ncu Tool State

Run ID: 20261111-create-install-nsys-ncu-tool
Started: 2026-11-11T07:30:00Z
Scope: Skill creation validation (issue #124): install -> rollback -> install lifecycle on the dev host (GB10).

| Step | Status | Evidence | Notes |
| --- | --- | --- | --- |
| 1. Install | completed | `docker build` + `docker compose up -d`; container reported `NVIDIA Nsight Systems version 2026.5.2.323` and ncu `Version 2026.3.1.0`. Re-ran after rollback with the same output. | Second build may reuse BuildKit cache. |
| 2. Package with zstd | completed | Pipeline smoke-tested on `ubuntu:24.04`: `docker save \| zstd -T0 -3` -> 26 MB archive -> `zstd -dc \| docker load` printed `Loaded image: ubuntu:24.04`. | Full 29.6 GB image not archived during validation. |
| 3. Rollback | completed | `docker compose down`; `docker rmi` deleted `sha256:e88a7bf1...`; image inspect failed (removed); base `vllm/vllm-openai:v0.32.0-cu129` kept; 0 `nsys-ncu-tool` containers left. | `WORK_DIR` pointed outside the repo; skill dir unchanged. |
