# Environment and mount rules

Primary runtime: Python 3.10+ (stdlib frontend helper), Docker Engine/Compose v2
on W78. Existing consumer renderer additionally requires PyYAML and Git.
Frontend: repository `web/`, React/Vite, multistage Node/nginx Dockerfile. Build
inside Docker; no global npm/Python installs. Use an existing Python environment
with PyYAML for generic skill validation. Docker commands require normal access;
never use sudo or prune on the shared host.

SSH target: `howard@192.168.1.78`. W76 OCR: `howard@192.168.1.76`.
Verify SSH host identity and `docker info` before mutation. The sandbox's `docker`
is not the W78 daemon. Host ports must be checked on W78, not from a Drone bridge
container or the agent sandbox.

## Filesystem namespaces

- Agent workspace data alias `/data/` corresponds in this session to W78
  `/mnt/share_data_78/howard/data/`. Verify the current mount mapping when moving
  to a different sandbox; do not assume a Docker daemon understands `/data/`.
- Agent model root is `/models/`; actual shared containers on W78 use the concrete
  `/tmp2/share_data/...` sources below. Do not replace them with `/models` merely
  because that directory exists in the agent environment.
- W78 deployment parent `D=/mnt/share_data_78/howard/data/deployments`.
- A/B instance root `$D/pretrieval-draft-reference-a` or `...-b`.

| W78 bind source | Container target | Owner/access |
| --- | --- | --- |
| `$D/pretrieval-draft-reference-{a,b}/parsed` | API `/data/parsed` | instance RW |
| `$D/pretrieval-draft-reference-{a,b}/postgres` | PG `/var/lib/postgresql` | instance RW; PG18 child `18/docker` |
| `$D/pretrieval-draft-reference-{a,b}/qdrant` | Qdrant `/qdrant/storage` | instance RW |
| `$D/pretrieval-draft-reference-{a,b}/snapshots` | Qdrant `/qdrant/snapshots` | instance RW |
| `/mnt/share_data_78/howard/data/draft_inference` | API `/mnt/samba/files` | shared corpus RO |
| `$D/pretrieval-draft-office/client` | API `/run/secrets/office-converter` | shared token directory RO |
| `$D/pretrieval-draft-office/service` | converter `/opt/office-converter/tokens` | shared auth directory RO |
| `/tmp2/share_data/Snowflake--snowflake-arctic-embed-l-v2.0` | embedding `/models/snowflake-arctic-embed-l-v2.0` | shared model RO |
| `/tmp2/share_data/docling-models` | Docling `/models` | shared models RO |

Frontend has **no data/model/token mounts**; HTML/assets and the host-network
nginx template are baked in its pinned image. Its Compose and receipt live in
`$D/pretrieval-draft-reference-{a,b}/frontend/` on the host, not mounted into nginx.

API UID/GID at initial deployment: `1016:1016`. PGDATA has its own image UID;
keep `/var/lib/postgresql` bind root traversable (0755), PGDATA child private
(0700), and never recursively chown a populated database to the API UID.

W76 VLM model source: `/tmp2/share_data/mistral-Ministral-3-14B-Instruct-2512`
→ `/workspace/llm_model` RO. Preserve live model/arguments/GPU/port when adopting.
