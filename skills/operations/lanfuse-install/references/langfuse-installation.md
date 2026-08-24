# Langfuse Local Installation And Rollback

Use this reference for a local self-hosted Langfuse deployment driven by the
checkout's Docker Compose file.

## Preflight

1. Confirm Docker Engine, the Compose plugin, Git, and a browser are available.
2. Resolve the intended checkout path and inspect it before cloning or editing.
3. If a checkout exists, inspect its branch, changes, `.env`, Compose file,
   running containers, and named volumes. Preserve user changes.
4. Choose a unique Compose project name for disposable validation so it cannot
   collide with an existing deployment.

## Install

Clone Langfuse only when the target path is absent:

```bash
git clone https://github.com/langfuse/langfuse.git
cd langfuse
```

Create an untracked `.env` containing first-run identifiers and credentials.
Use values supplied by the user or generated unique values; do not reuse the
examples below as production secrets.

```dotenv
LANGFUSE_INIT_ORG_ID=<organization-id>
LANGFUSE_INIT_ORG_NAME=<organization-name>
LANGFUSE_INIT_PROJECT_ID=<project-id>
LANGFUSE_INIT_PROJECT_NAME=<project-name>
LANGFUSE_INIT_PROJECT_PUBLIC_KEY=<pk-lf-value>
LANGFUSE_INIT_PROJECT_SECRET_KEY=<sk-lf-value>
LANGFUSE_INIT_USER_EMAIL=<administrator-email>
LANGFUSE_INIT_USER_PASSWORD=<unique-password>
```

Review the Compose file and replace every development-only secret before a
non-disposable deployment, including `SALT`, `ENCRYPTION_KEY`,
`NEXTAUTH_SECRET`, `POSTGRES_PASSWORD`, `CLICKHOUSE_PASSWORD`, and
`MINIO_ROOT_PASSWORD`. Store secrets only in the deployment's ignored
environment mechanism.

Start the stack:

```bash
docker compose up -d
```

The standard local stack includes Langfuse web and worker services plus
Postgres, ClickHouse, Redis, and MinIO. Use the actual service names from the
checked-out Compose file rather than assuming names when the file differs.

## Validate

Run all applicable checks:

```bash
docker compose config --quiet
docker compose ps
docker compose logs --tail 100
curl --fail --show-error http://127.0.0.1:3000/
```

On PowerShell, the endpoint check can use:

```powershell
Invoke-WebRequest http://127.0.0.1:3000/ -UseBasicParsing
```

Confirm in the browser that the configured administrator can sign in and that
the intended organization and project exist. First-run `LANGFUSE_INIT_*`
values apply only while the Postgres database is empty. Changing them after
initialization does not update existing accounts or API keys; use Langfuse
Settings instead.

## Rollback Levels

Choose exactly one level and record it in `STATE.md`.

### Stop Or Remove Containers, Retain Data

Stop without removing containers:

```bash
docker compose stop
```

Remove Compose containers and networks while retaining named volumes:

```bash
docker compose down
```

### Delete Managed Persistent Data

This permanently deletes the Compose project's named Postgres, ClickHouse,
MinIO, and Redis volumes. Display the exact Compose project and obtain explicit
confirmation first:

```bash
docker compose down -v
```

Inspect `docker compose config --volumes` before and after the command to prove
which managed volumes are in scope.

### Delete Images

Only when the user also requests image cleanup:

```bash
docker compose down -v --rmi all
```

### Delete The Checkout

Resolve the absolute path, verify it is the intended Langfuse checkout, and
confirm that `.env` or other local material does not need retention. Delete
only that verified directory using the platform's native filesystem command.

## Reversible Lifecycle Validation

Use an isolated checkout, unique Compose project name, unused host ports, and
disposable credentials. Never point this test at an existing deployment.

1. First install: run `docker compose up -d`, wait for defined health checks,
   verify all expected services, and verify the HTTP endpoint.
2. Rollback: run `docker compose down -v`, verify the project's containers and
   networks are absent, and verify only its declared named volumes were removed.
3. Second install: run `docker compose up -d` again from the same source with
   freshly initialized storage, repeat health and HTTP checks, and confirm the
   instance does not depend on first-install state.
4. After recording evidence, remove the disposable project with explicit
   authorization for its already-declared test volumes.

Record the checkout path, Compose project name, commands, service state,
endpoint response, volume assertions, and timestamps without recording secret
values.
