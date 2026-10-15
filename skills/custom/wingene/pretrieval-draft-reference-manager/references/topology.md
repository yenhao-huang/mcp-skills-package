# Topology and deployment records

Baseline inventory: 2026-10-15 Asia/Taipei. Recheck live receipts before changes.

| Instance | Frontend (LAN) | API (LAN) | PostgreSQL (W78 loopback) | Qdrant (W78 loopback) | DB subnet |
| --- | --- | --- | --- | --- | --- |
| A | `http://192.168.1.78:28179` | `http://192.168.1.78:28178` | `28173` | `28174` | `172.30.108.0/24` |
| B | `http://192.168.1.78:28279` | `http://192.168.1.78:28278` | `28273` | `28274` | `172.30.109.0/24` |

Private core project/container prefix: `pretrieval-draft-reference-a` or `-b`.
Services: `pretrieval-api`, `pretrieval-postgres`, `pretrieval-qdrant`.
Frontend project: `pretrieval-draft-reference-a-ui` or `-b-ui`; service `frontend`;
container `pretrieval-draft-reference-a-frontend` or `-b-frontend`.
API and frontend use host networking; database containers use private bridges
and publish only to `127.0.0.1`. Browser requests use relative `/api/...`; nginx
strips `/api` and proxies to **that instance's** `127.0.0.1:<API_PORT>`.

| Shared service | Host | Container | Endpoint from W78 | Device |
| --- | --- | --- | --- | --- |
| Converter | W78 | `pretrieval-shared-office-converter` | `http://127.0.0.1:59690` | CPU |
| Embedding | W78 | `pretrieval-shared-embedding` | `http://127.0.0.1:59480/v1` | GPU 0 |
| Docling | W78 | `pretrieval-shared-docling` | `http://127.0.0.1:59681` | GPU 0 |
| OCR/VLM | W76 | `pretrieval-shared-ocr` | `http://192.168.1.76:3132` | GPU 0 |

Embedding served model: `snowflake-arctic-embed-l-v2.0` (1024 dimensions).
Do not substitute `localhost` on another host for these W78 loopback endpoints.

## Authoritative files

All paths below are **W78 host paths** under
`/mnt/share_data_78/howard/data/deployments/`:

- `pretrieval-draft-reference-{a,b}/compose.json`: private core; contains DB
  credentials, keep mode 0600 and do not publish its full contents.
- `pretrieval-draft-reference-{a,b}/receipt.json`: core source SHA/image IDs,
  ports, subnet and private data paths.
- `pretrieval-draft-reference-{a,b}/frontend/docker-compose.yml`: frontend only.
- `pretrieval-draft-reference-{a,b}/frontend/receipt.json`: frontend source/image,
  paired API image/port and frontend port.
- `issue-708/source/`: attested initial staging export, including
  `.shared-consumer-source.json` (full file hashes).
- `issue-708/images.json`: initial API/Postgres/Qdrant image IDs.
- `issue-708/frontend-image.json`: exact matching frontend build receipt.
- `issue-708/shared-services.json`: shared endpoints; original repository source
  `deploy/w78/shared-services.json` in PR #709.
- `issue-708/shared_consumer.py`: deployed helper copy; repository source
  `deploy/w78/shared_consumer.py`. Inspect its provenance before reusing it.
- `issue-708/shared-docling.yaml`: shared Docling Compose.
- `issue-708/shared-embedding.adopted.json`: saved legacy embedding owner config.
- `pretrieval-draft-office/docker-compose.yaml`: converter owner config.
- `issue-708/runtime-acceptance.json`, `post-ci-services.json`,
  `ci-root/reports/`: prior bounded CI and runtime evidence.

W76 original OCR owner config:
`/tmp2/howard/model-deploy-tool/vllm/docker-compose-mistral3-14b.yml`.

Initial A/B source: `42378d059669b8297390151fe71c871791c2628d` (staging when first
created). This is a historical baseline, **not a promise of today's latest
staging**. Both initially have identical immutable core image IDs; later A/B
experiments may intentionally differ. Query receipts and image labels rather
than treating image names or StartedAt as source provenance.

## Legacy lifecycle trap

Renaming a container does not change Compose labels. Shared embedding still has
legacy `pretrieval-draft-b` ownership; shared converter has `pretrieval-draft-office`
ownership. Their unchanged IDs/StartedAt are intentional. A broad `compose down`
on either legacy project can stop shared services used by A/B/CI.

`pretrieval-draft-b-*` is **not** `pretrieval-draft-reference-b-*`.
`pretrieval-qdrant` at port 8074 is used by the main API/ingestion worker.

On 2026-10-15 the user explicitly authorized deleting the old offline/NAS/manual
PG containers and Draft C containers plus their private data. They are retired,
not rollback targets. Do not recreate them or infer this past authorization
permits deleting a new instance. The separate `pretrieval_eval_p0_1b6363eb_*`
pair was inspected but not removed in that session.
