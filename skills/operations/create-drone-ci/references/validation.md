# Validation

Run validation in this order and stop before service startup when static checks
fail.

## Scaffold

```bash
python3 references/scripts/scaffold_drone_ci.py --repo <repo-path>
python3 -m py_compile references/scripts/scaffold_drone_ci.py
```

Run the generated smoke test from the target repository root:

```bash
sh .ci/scripts/ci.sh
```

## Static Infrastructure

Create `.ci/drone/.env` from `.env.example` with real local values, then run:

```bash
docker compose \
  --env-file .ci/drone/.env \
  -f .ci/drone/compose.yaml \
  config --quiet
```

If Drone CLI is installed, also run:

```bash
drone lint .drone.yml
```

A YAML parser alone cannot prove Drone semantics; do not call a pipeline valid
solely because generic YAML parsing succeeded.

## Runtime

Only when the user authorized service startup:

```bash
docker compose \
  --env-file .ci/drone/.env \
  -f .ci/drone/compose.yaml \
  up -d

docker compose \
  --env-file .ci/drone/.env \
  -f .ci/drone/compose.yaml \
  ps

docker compose \
  --env-file .ci/drone/.env \
  -f .ci/drone/compose.yaml \
  logs --tail=100 server runner
```

Verify all of the following:

- Server remains running and its public URL is reachable.
- Runner remains running and logs show a successful Server connection.
- OAuth login returns to the expected Drone callback.
- Repository activation creates the expected Git provider webhook.
- A test push produces a pipeline with the expected trigger and step result.

Do not claim webhook completion before repository activation and provider-side
inspection succeed.
