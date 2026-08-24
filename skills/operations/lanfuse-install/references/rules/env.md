# Environment Rules

Read this file before installing packages, cloning Langfuse, starting Compose
services, or changing Hermes.

## Expected Environment

```text
Primary language: Shell, PowerShell, Docker Compose YAML, dotenv
Runtime version: Use versions declared by the checked-out Langfuse repository
Package manager: Docker Compose; uv only for an isolated Hermes Python environment
Frameworks: Langfuse self-hosted, Hermes observability plugin
Service manager: Docker Compose
Required services: Use only services declared by the target docker-compose.yml
```

## Rules

- Verify `docker version`, `docker compose version`, and `git --version` before
  installation. Do not install missing prerequisites without user approval.
- Treat the target `docker-compose.yml` as the source of truth for service
  names, images, ports, health checks, dependencies, and volumes.
- Identify the relevant Compose file when multiple files exist. Do not invent
  service names, ports, credentials, or volumes.
- Do not install Python packages globally. For Windows Hermes, target the
  isolated interpreter with `uv pip install --python`.
- Use a unique Compose project name and isolated checkout for lifecycle tests.
- Keep `.env` and generated secrets outside version control and redact values
  from command output and `STATE.md`.
- Do not start, stop, rebuild, or remove unrelated services.
