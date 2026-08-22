# Environment Rules

## Skill Runtime

Primary language: Python
Runtime version: Python 3.9 or newer
Package manager: none; standard library only
Frameworks: none
Service manager: Docker Compose v2
Required services: Git, Docker Engine, Drone Server, Drone Docker Runner, and a
supported Git provider

The scaffold script does not install packages or start services.

## Required Host Inputs

Discover or ask for these values before starting Drone:

- Git provider type and externally reachable URL.
- OAuth client ID and client secret.
- Drone externally reachable host and protocol.
- A persistent Drone Server data location.
- Runner name and capacity.
- A securely generated Server/Runner RPC shared secret.

Do not invent ports, hosts, storage paths, usernames, or credentials. The
starter `.env.example` uses placeholders only.

## Secrets

- Store runtime values in `.ci/drone/.env` and keep it ignored by Git.
- Never print or commit OAuth secrets, RPC secrets, Drone tokens, registry
  credentials, signing keys, or provider access tokens.
- Generate the RPC secret with `openssl rand -hex 16` or an equivalent secure
  random generator.
- Store pipeline secrets in Drone's repository or organization secret store,
  then reference them with `from_secret` in `.drone.yml`.

## Images And Dockerfiles

- Default Server image: `drone/drone:2`.
- Default Docker Runner image: `drone/drone-runner-docker:1`.
- Resolve and pin immutable image digests before production rollout when the
  environment's update policy requires reproducibility.
- Use direct images in Compose by default. Optional Dockerfiles inherit from
  `DRONE_SERVER_BASE_IMAGE` or `DRONE_RUNNER_BASE_IMAGE` and must not embed
  secrets.
- Never add tools to the Runner image merely to satisfy a pipeline step; each
  step should normally select its own purpose-built image.
