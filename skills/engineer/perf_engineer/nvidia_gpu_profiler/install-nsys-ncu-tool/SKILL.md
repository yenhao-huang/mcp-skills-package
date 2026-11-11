---
name: install-nsys-ncu-tool
description: Build and start a Docker environment (vLLM + Nsight Systems nsys + Nsight Compute ncu) for profiling GPU workloads, and package the image with zstd for offline transfer. Use when asked to install, set up, package, or remove the nsys/ncu profiling container.
---

# Install nsys/ncu Tool

`scripts/Dockerfile` builds `vllm-openai:v0.32.0-cu129-nsight`
(`vllm/vllm-openai:v0.32.0-cu129` + nsys 2026.5.2 + ncu 2026.3.1 from the
NVIDIA CUDA apt repo). `scripts/compose.yaml` only starts that image.

Requirements: NVIDIA driver, NVIDIA Container Toolkit, Docker, network access
during build, `zstd` for packaging.

## Workflow

Reset `STATE.md` from `references/template/STATE.template.md`, then:

1. **Install**

   ```bash
   cd <skill-dir>/scripts
   docker build -t vllm-openai:v0.32.0-cu129-nsight .
   WORK_DIR=<report dir> MODEL_DIR=<model dir> docker compose up -d
   docker compose exec profiler sh -c 'nsys --version; ncu --version'
   ```

   Reports written to `/work` in the container land in `WORK_DIR`; the model
   is mounted read-only at `/model`. Profile with e.g.
   `nsys profile -o /work/run vllm serve /model ...` inside the container.

2. **Package with zstd** (optional, for offline hosts)

   ```bash
   docker save vllm-openai:v0.32.0-cu129-nsight | zstd -T0 -3 -o nsys-ncu-tool.tar.zst
   # on the target host:
   zstd -dc nsys-ncu-tool.tar.zst | docker load
   ```

   Then run step 1 from `docker compose up -d` (skip `docker build`).

3. **Rollback**

   ```bash
   cd <skill-dir>/scripts && docker compose down
   docker rmi vllm-openai:v0.32.0-cu129-nsight   # base vLLM image is kept
   rm -f nsys-ncu-tool.tar.zst                    # only if step 2 created it
   ```

   `WORK_DIR` reports are user data; do not delete them unless asked.

Record the version output (step 1) and archive path (step 2) in `STATE.md`.

## Rules

- Do not pass `--build-context` or add a `build:` section to compose: the
  Dockerfile builds the image, compose only starts it.
- ncu needs `SYS_ADMIN` (already set in compose) on hosts with
  `RmProfilingAdminOnly=1`.
