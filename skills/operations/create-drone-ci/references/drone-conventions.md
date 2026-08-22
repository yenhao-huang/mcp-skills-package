# Drone CI Conventions

## Architecture

Drone Server authenticates users through the Git provider, receives provider
webhooks, stores build metadata, and dispatches pipelines. A Drone Runner polls
Server over authenticated RPC and executes pipeline commands. The Docker
Runner launches each step in an ephemeral container.

For Gitea, create a confidential OAuth application whose callback URL is the
exact public Drone URL plus `/login`. Configure the same `DRONE_RPC_SECRET` on
Server and Runner. After signing in to Drone, activate the repository; that
activation creates the provider webhook.

Prefer a dedicated Drone host. Confirm routing in both directions: users and
Gitea must reach the public Drone URL, Drone must reach Gitea, and Runner must
reach Drone Server.

## Image Policy

The official Server and Docker Runner are self-contained Docker images. The
normal lifecycle is:

```bash
docker compose --env-file .ci/drone/.env -f .ci/drone/compose.yaml pull
docker compose --env-file .ci/drone/.env -f .ci/drone/compose.yaml up -d
```

Do not create a custom image by default. Use the optional Dockerfiles only when
there is a documented need such as an internal certificate authority. Pin
production images by digest and review release notes before upgrades.

## Pipeline Policy

- The default pipeline file is root `.drone.yml`; `.drone.ci` is not a standard
  Drone filename.
- Give every pipeline and step a stable, descriptive name.
- Keep shell logic in `.ci/scripts/`; keep YAML focused on images, environment,
  dependencies, volumes, failures, and triggers.
- Test `.ci/scripts/` behavior under `.ci/tests/`.
- Start with `push` and `pull_request` triggers. Add deploy or publication
  pipelines only with narrow branch, tag, or event conditions.
- Avoid secrets in commands or YAML. Use Drone secrets and `from_secret`.
- Pin pipeline images by digest when reproducibility is required.
- Set explicit timeouts for long jobs and document any `failure: ignore` use.

## Runner Security

Mounting `/var/run/docker.sock` gives the Docker Runner effective control of
the host Docker daemon. Limit repository activation and trusted mode to
reviewed code. Do not expose host volumes, devices, privileged mode, or the
Docker socket to pull requests from untrusted contributors.

## Ownership

- `.ci/drone/`: platform owner; Server/Runner lifecycle and security.
- `.drone.yml`: repository owner; pipeline graph, images, and triggers.
- `.ci/scripts/`: task owner; executable CI behavior.
- `.ci/tests/`: task owner; regression tests for CI behavior.
- `.ci/docs/`: shared; intent, prerequisites, and operational handoff.
