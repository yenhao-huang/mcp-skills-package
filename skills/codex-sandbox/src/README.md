# Codex Sandbox

## Quick
```bash
# w78
bash build_and_exec.sh
```

Runtime files are stored under the repo-level `.runtime/` directory. Keep `.runtime/` ignored by git.

## How to use
Run Codex inside Docker with `ssh`, `git`, and a named user.

1. Clone the repo and enter the `codex-sandbox` directory.

```bash
git clone git@github.com:yenhao-huang/sandbox_utils.git
cd sandbox_utils/codex-sandbox
```

2. Build and verify the image.

```bash
docker build \
  --build-arg UID="$(id -u)" \
  --build-arg GID="$(id -g)" \
  --build-arg USERNAME=howard \
  -t codex-sandbox:local \
  .
```

Verify the image:

```bash
docker run --rm codex-sandbox:local whoami
docker run --rm codex-sandbox:local ssh -V
docker run --rm codex-sandbox:local codex --version
```

Prepare SSH files:

```bash
SSH_DIR="${SSH_DIR:-../.runtime/.ssh}"
mkdir -p "${SSH_DIR}"
cp ~/.ssh/id_ed25519 "${SSH_DIR}/"
cp ~/.ssh/id_ed25519.pub "${SSH_DIR}/"
cp ~/.ssh/known_hosts "${SSH_DIR}/"
chmod 700 "${SSH_DIR}"
chmod 600 "${SSH_DIR}/id_ed25519"
```

3. Start and use the container.

Set customized variables:

```bash
CONTAINER_NAME=codex-sandbox
WORKSPACE_DIR=/path/to/your/repo
SSH_DIR=/path/to/sandbox_utils/.runtime/.ssh
SKILLS_DIR=~/.agents/skills
GPU_DEVICES=all
CONTAINER_HOME=/home/howard
CONTAINER_WORKDIR=/workspace
MODEL_DIR=/path/to/your/models
DATA_DIR=/path/to/your/data
CONTAINER_SKILLS_DIR=/home/howard/.agents/skills
CONTAINER_MODEL_DIR=/models
CONTAINER_DATA_DIR=/data

docker run -d \
  --name "${CONTAINER_NAME}" \
  -w "${CONTAINER_WORKDIR}" \
  -e HOME="${CONTAINER_HOME}" \
  -e NVIDIA_VISIBLE_DEVICES="${GPU_DEVICES}" \
  -e NVIDIA_DRIVER_CAPABILITIES=compute,utility \
  --gpus "${GPU_DEVICES}" \
  -v "${WORKSPACE_DIR}:${CONTAINER_WORKDIR}" \
  -v "${SSH_DIR}:${CONTAINER_HOME}/.ssh:ro" \
  -v "${SKILLS_DIR}:${CONTAINER_SKILLS_DIR}" \
  -v "${MODEL_DIR}:${CONTAINER_MODEL_DIR}" \
  -v "${DATA_DIR}:${CONTAINER_DATA_DIR}" \
  codex-sandbox:local \
  sleep infinity
```

- `CONTAINER_NAME=codex-sandbox`，容器名稱。之後 `docker exec -it "${CONTAINER_NAME}" bash` 會用到。
- `WORKSPACE_DIR=/path/to/your/repo`，主機上的專案路徑。會掛到容器內的 `${CONTAINER_WORKDIR}`。
- `SSH_DIR=/path/to/sandbox_utils/.runtime/.ssh`，主機上的 SSH 檔案目錄。會掛到容器內的 `${CONTAINER_HOME}/.ssh`。
- `SKILLS_DIR=~/.agents/skills`，主機上的 skills 目錄。會掛到容器內的 `${CONTAINER_SKILLS_DIR}`。
- `GPU_DEVICES=all`，Optional。傳給 `docker run --gpus`；設成 `none` 可停用 GPU 掛載。
- `CONTAINER_HOME=/home/howard`，容器內使用者的 home 目錄。`HOME` 環境變數會設成這個值。
- `CONTAINER_WORKDIR=/workspace`，容器內的工作目錄。`docker run -w` 會用到。
- `MODEL_DIR=/path/to/your/models`，Optional。主機上的模型目錄。會掛到容器內的 `${CONTAINER_MODEL_DIR}`。
- `DATA_DIR=/path/to/your/data`，Optional。主機上的資料目錄。會掛到容器內的 `${CONTAINER_DATA_DIR}`。
- `CONTAINER_SKILLS_DIR=/home/howard/.agents/skills`，Optional。容器內的 skills 掛載目錄。
- `CONTAINER_MODEL_DIR=/models`，Optional。容器內的模型掛載目錄。
- `CONTAINER_DATA_DIR=/data`，Optional。容器內的資料掛載目錄。

4. Enter the container:

```bash
docker exec -it "${CONTAINER_NAME}" bash
```

```bash
codex --dangerously-bypass-approvals-and-sandbox
```
