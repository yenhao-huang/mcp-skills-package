# Environment Rules

```text
Primary language: none (shell + Docker)
Runtime version: vllm/vllm-openai:v0.32.0-cu129, nsys 2026.5.2, ncu 2026.3.1
Package manager: apt (inside the image, NVIDIA CUDA ubuntu2404 repo)
Frameworks: vLLM
Service manager: Docker Compose (scripts/compose.yaml)
Required services: profiler
```

- Build the image only with `scripts/Dockerfile`; compose never builds.
- Do not install nsys/ncu on the host.
