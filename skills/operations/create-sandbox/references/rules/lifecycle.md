# Lifecycle Rules

Use this reference before changing build/run/post-create behavior or explaining
which work belongs before vs. after container creation.

## Before Create-Container

- Validate confirmed host paths.
- Prepare project-local runtime files such as `.runtime/.ssh`.
- Compute image/container names.
- Select the persistent Docker-in-Docker data volume.
- Stop/remove the previous same-name container, then select an unbound SSH host
  port immediately before assembling `docker run` arguments. Use `SSH_PORT`
  when explicitly configured; otherwise scan `SSH_PORT_RANGE_START` through
  `SSH_PORT_RANGE_END`.
- Verify `src/Dockerfile`, `src/build_and_exec.sh`,
  `src/after_create_container.sh`, and `src/test_service.sh` exist.
- Build the Docker image.
- Assemble `docker run` arguments.

The availability probe releases the port before `docker run` binds it. Docker
remains the final authority if another process claims the port in that short
interval.

## Create-Container

- Start the new detached container.
- Start the internal `dockerd` daemon and wait for it to become ready.
- Run `sudo /usr/sbin/sshd`.
- Write a readiness marker after both services start, and make the host script
  wait for that marker before post-create bootstrap.
- Keep the container alive with `sleep infinity`.

The outer sandbox container runs with `--privileged`; it must not bind-mount
the host Docker socket. The internal daemon stores its state in a named volume
mounted at `/var/lib/docker`, so bind-mount source paths used by inner
containers resolve in the sandbox filesystem.

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
