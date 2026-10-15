---
name: pretrieval-draft-reference-manager
description: Deploy, inspect, upgrade, stop, or remove PRetrieval draft-reference A/B on W78, including their frontends and shared W78/W76 inference services. Use for draft-reference ports, source versions, mount paths, data isolation, and A/B environment management.
---

# PRetrieval Draft Reference Manager

Manage `pretrieval-draft-reference-a` and `pretrieval-draft-reference-b` on
W78 (`192.168.1.78`). These are independent comparison environments using one
shared converter/embedding/Docling/OCR service set. The application repository is
`http://192.168.1.76:3000/leo/PRetrieval`; its integration branch is `staging`.
Issue and PR titles are English.

## Workflow

1. Read [environment and mounts](references/rules/env.md) and
   [state rules](references/rules/state-rules.md). Initialize a new local run
   record from `references/template/STATE.template.md`; do not overwrite another
   run or commit credentials. Resolve the requested instance and operation.
2. Inspect **the W78 host Docker daemon over SSH**, including stopped containers,
   image IDs/labels, port bindings, networks, mounts and saved receipts. The
   agent sandbox has a separate Docker daemon. Record the existing A/B and
   shared container IDs/StartedAt before changes. Dates are Asia/Taipei.
3. For ports/paths/status, answer from the live receipts and
   [topology](references/topology.md). For create/version change, follow
   [deployment](references/deployment.md). For frontend, use the same source SHA
   as its API, then the frontend-only Compose/helper described there. Existing
   compatible shared services stay running; a requested frontend addition does
   not authorize an API or database upgrade.
4. For start/stop/remove/rollback, follow
   [lifecycle](references/lifecycle.md). `stop`, container removal and data
   deletion are different operations. Carry out an already-authorized operation
   without asking again; if destructive scope is missing, prepare the exact
   affected resource list before requesting that scope. Never infer deletion
   from “restart” or “upgrade”.
5. For deploy/start/update, validate HTTP frontend, actual static asset, same-origin `/api/health`, exact
   nginx API upstream, API health and resource preservation. For stop/remove,
   verify the requested stopped/absent state and retained/deleted data instead;
   do not restart a service merely to run an HTTP check. Test first-time
   frontend installation with install → remove frontend only → install again.
   For any new reversible deployment path, validate that same lifecycle on a
   disposable target before claiming it verified; do not reset an existing DB
   to satisfy a test. Record unexecuted tests honestly.
6. Update the run record with source/image IDs, URLs, mount paths, commands,
   evidence and pending PR/merge state. Skill changes in this package follow its
   issue → task branch → PR workflow; an open PR is not merged publication.

## Boundaries

- API/Postgres/Qdrant are private per A/B; frontend is a separate `*-ui` Compose
  project with one `*-frontend` container. CI uses three private services and
  does not need a frontend. Inference services are not in consumer Compose.
- Host networking makes W78 loopback shared endpoints reachable. Separate DB
  ports/directories prevent accidental mixing; this is **not a security boundary
  between untrusted consumer processes**.
- Preserve `CHUNK_IDENTITY_ROOT=/mnt/samba/files` for existing indexed data.
  Shared raw corpus/model mounts are read-only and never instance-owned data.
- The shared converter/embedding retain legacy Compose project labels. Never
  run broad legacy project `down`, prefix-wide removal, or Docker prune.
- No secrets in Git/logs: refer to token **paths**, not contents; redact generated
  Compose credentials and database URLs from reports.
- Concurrency/readiness limitations from PR #709 are in deployment guidance;
  do not silently claim they have been fixed by adding this skill/frontend.
