# Deployment and versions

Run host commands over SSH to W78. Paths below are W78 paths, not sandbox paths.
`D=/mnt/share_data_78/howard/data/deployments`; replace variables deliberately.
The user authorizes the requested deployment, not a blanket upgrade of all peers.

## Existing instance: inspect before changing

Read its `receipt.json`, then inspect live API image ID, API_PORT, network mode,
mounts and health. Compare PostgreSQL/Qdrant image IDs and data paths with the
receipt. Do not print the generated core Compose: it contains credentials.
Determine whether the request means adding a frontend, restarting, or changing
source version. Record pre-change container IDs/StartedAt and DB system ID.
For frontend-only requests, leave all core and shared service processes alone.

## New core or candidate version

The repository's `deploy/w78/shared_consumer.py` prepares only API, PostgreSQL
and Qdrant. It is versioned with PRetrieval, not duplicated in this skill. Resolve
its reviewed revision from PR #709 or merged staging; do not assume the historical
`issue-708` host copy is the latest code.

1. Fetch `leo/PRetrieval` staging and resolve the intended full SHA. For identical
   fresh A/B resolve once and use the same image receipt; for comparisons record
   explicit A/B SHAs and which is the baseline. **Existing A/B databases are not
   replaced by rerendering.** This helper refuses existing output destinations.
2. Use a clean exact-SHA checkout, or a trusted `git archive` export with the
   helper's `.shared-consumer-source.json` file-hash attestation. Never fabricate
   a receipt to bless modified source. Call `verify_source(source, sha)` before
   builds; for archives this checks the exporter-provided hashes, not the remote
   Git server. The exporter must attest the SHA from Git.
3. The helper's command shape is:

   ```bash
   python3 "$HELPER" build --source-dir "$SOURCE" --source-sha "$SHA" \
     --image-tag "$TAG" --receipt "$IMAGE_RECEIPT"
   python3 "$HELPER" render --source-dir "$SOURCE" --images "$IMAGE_RECEIPT" \
     --shared-config "$SHARED_MANIFEST" --output-dir "$NEW_INSTANCE_DIR" \
     --project "$PROJECT" --api-port "$API_PORT" --postgres-port "$PG_PORT" \
     --qdrant-port "$QDRANT_PORT" --network-subnet "$SUBNET" \
     --corpus /mnt/share_data_78/howard/data/draft_inference \
     --corpus-container /mnt/samba/files --uid 1016 --gid 1016
   ```

   These are interface examples, not permission to create a new database or
   choose arbitrary ports. Read `--help`, collision checks and active inventory.
   Do not invoke a fresh render over existing A/B to perform an upgrade.
4. Inspect generated service names, image IDs, ports, endpoint equality, paths,
   and token readability. Run `docker compose --env-file /dev/null -f
   "$NEW_INSTANCE_DIR/compose.json" config --quiet`, then `up -d --wait --pull never`.
   Verify API health, PG and Qdrant independently; capture receipts outside Git.
5. On a new disposable target, verify create → stop/remove its exact containers
   → recreate with retained config/data before claiming restart reversibility.
   A source-version downgrade is **not generally reversible**: API startup may
   migrate DB schema. For real upgrades, decide backup/restore and schema
   compatibility before changing images. Preserve the original private data,
   credentials and CHUNK_IDENTITY_ROOT unless a reset is explicitly requested.

This skill's initial validation adds frontends to existing A/B; it does not
claim a newly tested core create/delete/recreate or database migration path.
Prior core acceptance evidence is in PRetrieval issue #708's host reports.

## Upgrade one existing API while retaining data

This is a planning/runbook path; no database migration was executed in the
frontend validation run. Resolve the requested target SHA and its migration
requirements before mutation. For instance A (`$I`), keep B unchanged.

1. Save A's core/frontend Compose and receipts with mode 0600 in a timestamped
   directory outside source/data. Record each component image ID and its own
   revision, PG system identifier/schema revision, row counts and Qdrant counts.
   Prepare and verify the required backup/restore procedure if the target can
   migrate schema. If restore cannot be established, report that blocker before
   starting the new API. Do not assume an older binary can read a newer schema.
2. Build the API and matching frontend from the verified target source, recording
   immutable IDs. Keep the current PostgreSQL/Qdrant images, credentials, bind
   paths, ports, network and CHUNK_IDENTITY_ROOT. A request to change application
   version is not a request to rebuild database services or reset data.
3. Prepare the core Compose update changing only
   `services.pretrieval-api.image` to the target API ID (plus any explicitly
   required, reviewed application setting). Validate with `config --quiet`.
   Stop this instance's frontend during the API transition to avoid a mismatched
   UI/API pair. Apply only the API:

   ```bash
   docker compose --env-file /dev/null -f "$I/compose.json" \
     up -d --no-deps --wait --pull never pretrieval-api
   ```

4. Verify target image, API health, migration outcome, PG system identifier/data
   continuity, Qdrant counts and unchanged database/peer/shared container IDs.
   Only after the API succeeds, update the existing frontend's image/receipt and
   start it with its separate Compose. Do not add a new frontend merely because
   an upgrade was requested if no frontend exists and it is out of scope.
5. Update the **deployment** receipt to the observed API `source_sha`,
   `source_dir`, API image/tag and `image_ids.api`, preserving DB image IDs and
   all data/port fields. Record per-component source/tag provenance separately
   (e.g. `component_sources`) because retained PostgreSQL may come from the old
   source. Keep the original build receipt immutable; a mixed-version deployment
   receipt is not a new all-components build receipt. Update frontend receipt's
   paired API image/source only after it agrees with live state.
6. If a transition fails, leave an explicit failed/pending run record with the
   actual live image/schema; never label it upgraded. Restore saved configs and
   the old API/frontend only when schema compatibility is verified. Otherwise
   keep that instance stopped while executing the established DB restore plan;
   preserve B/shared services and never erase data as a repair shortcut.

## Build a matching frontend

Build from the same verified source as the selected API, **not today's staging
if the API is older**. `web/Dockerfile` bakes the SPA and `web/nginx.conf`, whose
upstream is `127.0.0.1:${API_PORT}` and listen port `${FRONTEND_PORT}`.
Do not use the bridge-only VDI nginx template with a host-network frontend.

```bash
docker build --label "org.opencontainers.image.revision=$SHA" \
  --label ai.pretrieval.source.dirty=false --label ai.pretrieval.role=frontend \
  -t "pretrieval-frontend:$TAG" -f "$SOURCE/web/Dockerfile" "$SOURCE/web"
docker image inspect --format '{{.Id}}' "pretrieval-frontend:$TAG"
```

First verify source; labels alone do not prove provenance. Do not overwrite a
preexisting tag with another source. Record full source SHA and immutable image
ID in a build receipt. The runtime Compose must use the image ID.

Copy `references/scripts/render_frontend.py` to W78 or invoke the W78 copy of
this skill. The helper performs read-only Docker inspection, validates source
labels against the live core receipt/API and writes **new** frontend files. It
must run on W78 because its socket probe examines the local host port space.
For initial A use 28179; B 28279. Recheck port availability immediately before up.

```bash
python3 "$SKILL/references/scripts/render_frontend.py" \
  --consumer-dir "$D/pretrieval-draft-reference-a" \
  --image-id "$FRONTEND_IMAGE_ID" --frontend-port 28179
docker compose --env-file /dev/null \
  -f "$D/pretrieval-draft-reference-a/frontend/docker-compose.yml" config --quiet
docker compose --env-file /dev/null \
  -f "$D/pretrieval-draft-reference-a/frontend/docker-compose.yml" up -d --wait --pull never
```

For an already prepared frontend, inspect its receipt and reuse the saved
Compose. The helper intentionally refuses overwriting its output or an existing
container. To update version, record the old Compose/image, verify the new image
against the paired API, and edit only that frontend's image and receipt. Never
rebuild its database. Keep API and frontend changes compatible as a pair.

Validation:

- HTTP `/` is 200 and contains SPA asset paths; fetch an actual `/assets/...`
  file and verify nonempty content/type (a SPA fallback 200 alone is not enough).
- `/api/health` returns JSON from the intended API; `docker exec <frontend>
  nginx -t` passes and the rendered config contains exactly the expected
  `proxy_pass http://127.0.0.1:<api_port>/;`.
- Verify both LAN frontend URLs and container health; compare existing core and
  shared IDs/StartedAt with pre-deployment inventory.
- Use the frontend-only lifecycle in `lifecycle.md` for first install testing.
  Retain evidence such as `issue-708/frontend-acceptance.json` on W78.

## Current limitations to check before load tests

PR #709's initial consumer renderer applies VDI defaults: OCR workers/concurrency
500, active-file concurrency 24, Docling lanes 4. The old CI config file's OCR
16/active-file 4 values are **not read by this renderer**. Do not claim conservative
limits are active; inspect the live API env. Coordinate heavy CI/A/B ingestion or
implement reviewed explicit limits before interpreting concurrent benchmark data.

API `/health` does not cover all shared dependencies. Before ingestion probe
VLM `/v1/models`, Docling `/ready`, converter with an authenticated synthetic
conversion and embedding with the configured model from the consumer's network.
A/B direct functional requests were tested on W78; simultaneous heavy load and
full 12-hour corpus were not. Drone PR smoke is not full-corpus acceptance.

The renderer adapts a selected source template with string replacement for
healthcheck/corpus and fixed DB internal ports. Inspect the rendered result when
source templates change; do not infer compatibility with all future versions.
Host cleanup failures may remove the ownership marker before completion; do not
recreate markers or delete leftovers without verifying retained ownership/source
receipts and remaining containers.

A/B also inherit `REFINE_AI_BASE_URL=http://192.168.1.80:19990` and
`MONGO_LOG_ENABLED=true`; review whether query logging is appropriate for the
experiment. These are not a fifth newly managed shared service.
