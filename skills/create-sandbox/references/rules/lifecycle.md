# Lifecycle Rules

Use this reference before changing build/run/post-create behavior or explaining
which work belongs before vs. after container creation.

## Before Create-Container

- Validate confirmed host paths.
- Prepare project-local runtime files such as `.runtime/.ssh`.
- Compute image/container names.
- Validate Docker socket access.
- Verify `src/Dockerfile`, `src/build_and_exec.sh`,
  `src/after_create_container.sh`, and `src/test_service.sh` exist.
- Build the Docker image.
- Assemble `docker run` arguments.

## Create-Container

- Stop/remove the previous same-name container if present.
- Start the new detached container.
- Run `sudo /usr/sbin/sshd`.
- Keep the container alive with `sleep infinity`.

## After Create-Container

Run `src/after_create_container.sh` against the running container. This phase
performs workspace-level bootstrap:

- Confirm the container is running.
- If `RUN_AGENT_PACKAGE_INIT=1`, clone or update the agent package in
  `${CONTAINER_WORKDIR}/${AGENT_PACKAGE_DIRNAME}`.
- Run `${AGENT_PACKAGE_DIRNAME}/init.sh` from `${CONTAINER_WORKDIR}` to populate
  `.codex` and `.claude` skills/hooks while preserving existing project
  content.

## After-Create Validation

- Run `src/test_service.sh` after `after_create_container.sh` completes.
- Enter the container with `docker exec -it "${CONTAINER_NAME}" bash` only after
  service tests finish or are skipped.
