# Service Test Rules

Use this reference before changing sandbox validation behavior.

## Test Script

Generated scripts should expose:

```text
RUN_SERVICE_TESTS=1
TEST_SERVICE_SCRIPT=${BUILD_CONTEXT}/test_service.sh
```

`RUN_SERVICE_TESTS=1` runs `src/test_service.sh` after
`src/after_create_container.sh` completes and before entering the container.
`RUN_SERVICE_TESTS=0` skips service tests.

## Required Checks

The service test should verify:

- Container running state.
- `docker exec` works.
- Codex and Claude CLIs are installed.
- Workspace mount is writable.
- Optional model/data mounts exist when configured.
- SSH server config/listener works.
- SSH key login works when keys are available.
- The Docker-in-Docker socket exists, the internal daemon responds to
  `docker info`, and its data root is `/var/lib/docker`.

When `RUN_AGENT_PACKAGE_INIT=1`, the service test should verify:

- `mcp-skills-package/.git`
- `.codex/hooks.json`
- A sandbox skill exists under both `.codex/skills/` and `.claude/skills/`

Accept both `create-sandbox` and the older package name `codex-sandbox` during
migration.
