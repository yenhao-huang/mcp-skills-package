# Lifecycle and data ownership

A lifecycle request applies only to the named instances/resources. Preserve
shared services, peer instances, raw corpus/models and unrelated host projects.
Run commands on W78. Record IDs, image IDs, mounts, labels and StartedAt first.

## Frontend-only lifecycle (reversible)

For instance A (`...-b` for B):

```bash
D=/mnt/share_data_78/howard/data/deployments
F="$D/pretrieval-draft-reference-a/frontend/docker-compose.yml"
docker compose --env-file /dev/null -f "$F" up -d --wait --pull never
# Verify /, static assets, /api/health and nginx upstream.
docker compose --env-file /dev/null -f "$F" down
# Verify only pretrieval-draft-reference-a-frontend disappeared.
docker compose --env-file /dev/null -f "$F" up -d --wait --pull never
# Repeat HTTP checks; peer/core/shared IDs and StartedAt must stay unchanged.
```

That Compose has exactly one service, no volumes, and its own `*-ui` project.
It cannot select the core by Compose label. `down` retains prepared configuration
and the built image for reinstall. To undo initial **preparation** as well, after
removing that frontend delete only its `frontend/docker-compose.yml` and
`frontend/receipt.json`, then `rmdir frontend` if empty. Do not remove the instance
root or core receipt. A newly built image may be removed by exact image ID only
when no container/tag outside this task needs it and image cleanup is requested.

## Stop or remove a private core

Use the exact saved `compose.json` and verify it contains only that instance's
API/Postgres/Qdrant and the expected project name. Stop frontend first, then API,
then databases. For simple stop use `docker compose ... stop`; restart with
`start --wait` when supported or `up -d --wait --pull never`.
For container removal without data deletion use the exact project's `down`
after verifying labels. Its bind data directories remain. Frontend lives in a
separate project and needs its own command. Never match only `pretrieval-*`.

Recreating retained core containers may run API startup/migrations: pin the same
images and validate schema/data before calling it a successful recovery. A
rollback to older source must use a compatible schema or an explicit DB restore;
changing an image tag is not a safe database rollback.

## Explicit permanent deletion

“Stop” does not authorize removal; “remove containers and do not retain data”
authorizes deleting the selected instance's private state. Do not ask again for
already-explicit deletion of those same resources.

1. Inventory all containers, **including stopped ones**. Resolve actual volumes
   and bind sources from inspect, not just naming prefixes. Find all other
   references; if a mount is shared, exclude it and report why.
2. Stop the selected frontend/API/workers before its DBs. Remove only captured
   container IDs after checking their names and project match the target.
3. Remove exact exclusive named/anonymous volumes with `docker volume rm`, not
   prune. For current A/B, private data is **bind-mounted**, so volume removal
   alone does not erase it. Verify the canonical non-symlink paths for `parsed`,
   `postgres`, `qdrant`, `snapshots`; ensure no surviving container uses them.
4. Delete only the authorized private directories. Never delete their common
   `/data` ancestor, raw `draft_inference`, model mounts, converter client/service
   token directories, peer directories or a symlink target. Ordinary host-user
   deletion may fail on UID-999 PGDATA; do not broaden deletion or use sudo.
   If needed use a reviewed, pinned helper container with a nonrecursive bind of
   only the exact owned target and no network, or report the precise permission
   blocker. No privileged container or Docker socket mount is needed.
5. Verify containers/selected data are absent, then verify peers/shared services
   are still running with the same IDs/StartedAt. Record what was deleted versus
   retained (e.g. source checkout, Compose metadata and images).

Permanent deletion is **not reversible**. Do not promise restore without a
verified preexisting backup. Cleanup documentation is not standing permission
for future destructive operations.

## Shared services / rollback

Shared services have their own owners. Preserve running compatible services and
reuse them; adding a consumer does not require restarting inference. If a shared
change is explicitly requested, capture its original owner config/image/model/
GPU/ports before mutation. Reversing a rename means restoring that exact name
and owner config, not recreating a container under a different project. OCR
restart causes an interruption and needs endpoint readiness verification.

Never run `down` on legacy draft-b or draft-office as part of consumer cleanup:
shared embedding/converter still carry those Compose labels. Draft C has been
retired; never use its old configuration as a live restore target.
