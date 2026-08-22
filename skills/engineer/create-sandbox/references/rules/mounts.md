# Mount Rules

Use this reference before asking mount questions, validating host paths,
preparing SSH files, or handling Docker-in-Docker data and extra mounts.

## Required Mount Questions

The repo/workspace host path is a hard gate. A path is confirmed only when the
user explicitly provides the host path or explicitly approves a proposed host
path in the current conversation. Do not treat `cwd`, repository search
results, directory listings, an existing `.runtime/build_codex_sandbox.sh`,
`STATE.md`, or a project nickname such as "Pretrieval" as confirmation.

If the workspace host path is not confirmed, stop before any file write,
script update, permission validation, `.gitignore` edit, Docker command, or
prepared SSH copy. Mark the workflow step as `blocked` in `STATE.md` with the
missing workspace confirmation as evidence.

Before writing, updating, validating, or running a sandbox script, ask for:

- Repo/workspace mount: host path and container path. Default container path
  only after confirmation: `/workspace`.
- Model mount: host path and container path, or confirmation of no model mount.
  Default host path: `/mnt/share_data_78/howard/models`. Default container path
  only after confirmation: `/models`.
- SSH mount: host SSH directory or prepared SSH files, or confirmation of no SSH
  mount. Default container path only after confirmation:
  `${CONTAINER_HOME}/.ssh`.
- Data mount: host path and container path, or confirmation of no data mount.
  Default host path: `/mnt/share_data_78/howard/data`. Default container path
  only after confirmation: `/data`.
- Docker data: host directory for the internal daemon's persistent state.
  Default host path: `/mnt/share_data_78/howard/docker`. It is bind-mounted at
  the fixed container data root `/var/lib/docker`.
- Host Docker: whether to additionally expose the host daemon. It is disabled
  by default; when enabled, mount host `/var/run/docker.sock` to container
  `/var/run/host-docker.sock`.
- Extra mounts: any additional `host_path:container_path` or
  `host_path:container_path:ro` entries.

Use this concrete prompt when the request does not already provide explicit
mount answers:

```text
要建立 sandbox 前我需要先確認掛載設定：

1. workspace/repo 要掛哪個 host path？container 內路徑要用 `/workspace` 嗎？
2. model 要掛嗎？host path 預設 `/mnt/share_data_78/howard/models`，container 內路徑要用 `/models` 嗎？
3. SSH 要掛嗎？使用 host `~/.ssh` 複製必要 key 到 `.runtime/.ssh` 可以嗎？
4. data 要掛嗎？host path 預設 `/mnt/share_data_78/howard/data`，container 內路徑要用 `/data` 嗎？
5. Docker-in-Docker 資料要存在哪個 host path？預設 `/mnt/share_data_78/howard/docker`，container 內固定掛到 `/var/lib/docker`
6. 是否還要額外啟用 host Docker？若啟用，host `/var/run/docker.sock` 會掛到 container `/var/run/host-docker.sock`
7. 還有其他 extra mounts 嗎？格式：`/host/path:/container/path` 或 `/host/path:/container/path:ro`
```

When an interactive user-input menu is available, ask the Docker data question
as its own menu item. Offer `/mnt/share_data_78/howard/docker` as the
recommended default and allow a free-form custom host path; do not hide this
choice inside a combined mount summary.

Skills directories are not part of the standard sandbox mount questions and
should not be mounted unless the user explicitly provides one as an extra
mount.

If the user asks to proceed without answering, create only a configurable
script with empty `WORKSPACE_DIR`, `SSH_DIR`, and `EXTRA_MOUNTS`; use the
documented default `MODEL_DIR`, `DATA_DIR`, and `DIND_DATA_DIR`; and make the
script fail until `WORKSPACE_DIR` is set.

## Path Rules

- Do not infer the repo/workspace from `cwd`, parent directories, search
  results, existing scripts, old `STATE.md`, or project names; use only
  confirmed user input.
- Put generated sandbox scripts in the target project's `.runtime/` directory.
- Preserve existing `.gitignore` contents when adding `.runtime/`.
- Do not refer to old skill names when describing this skill. It is
  `create-sandbox`. Keep Docker image/container defaults unchanged unless the
  user explicitly asks to rename runtime resources.

## Mount Validation

- Check that each confirmed host path exists.
- Check that the repo/workspace host path is readable, writable, and
  executable/searchable.
- Check that model, SSH, data, and extra mount host paths are readable and
  executable/searchable; also check writability for every read-write mount.
- Run the sandbox with `--privileged` and bind-mount the confirmed
  `DIND_DATA_DIR` at `/var/lib/docker` for the internal daemon.
- Bind-mount the host Docker socket only when explicitly enabled, and expose
  it at `/var/run/host-docker.sock` rather than replacing the DinD socket.
- Keep `DIND_DOCKER_SOCK` inside the sandbox; default it to
  `/var/run/docker.sock` and set `DOCKER_HOST` to that internal Unix socket.
- If a path is missing, ask a correction question in this form:
  `repo 找不到，你想找的是不是 <candidate>?`, replacing `repo` with the mount
  label.
- If a path exists but lacks required permissions, ask whether copying the
  needed files into `.runtime/` is acceptable. Copy only after explicit
  confirmation.
- Generated scripts must fail fast with clear errors for missing paths or
  insufficient mount permissions.

## Existing Docker State Migration

Changing `DIND_DATA_DIR` for an existing sandbox is a migration, not a live
configuration edit:

- Stop the sandbox and its internal Docker daemon before copying state.
- Confirm the destination filesystem supports `overlay2`.
- Copy the complete current Docker data root while the daemon is stopped.
- Start the sandbox with the new bind mount and verify the storage driver,
  Docker root directory, images, containers, and volumes before removing the
  old copy.
- Never point two running Docker daemons at the same `DIND_DATA_DIR`.

## SSH Rules

- Prefer prepared `.runtime/.ssh` mounts over direct host home-directory mounts.
- Treat a user request to "mount host ssh" as permission to copy the required
  files from the confirmed host SSH directory into `.runtime/.ssh`, unless they
  explicitly ask for a direct Docker mount.
- Generated scripts should expose `HOST_SSH_DIR`, `SSH_DIR`, and
  `PREPARE_SSH_DIR=1` by default.
- Copy only `id_ed25519`, `id_ed25519.pub`, `known_hosts`, and
  `authorized_keys` when present.
- If `authorized_keys` is absent but `id_ed25519.pub` is present, use the public
  key as `authorized_keys`.
- Set strict permissions: `.runtime/.ssh` `700`, private key `600`, public key
  `644`, `known_hosts` `644`, and `authorized_keys` `600`.
- Mount the prepared SSH directory read-only at a staging path such as
  `/tmp/codex-sandbox-ssh`, then copy the allowed files into the container
  user's `${HOME}/.ssh` and apply strict Linux permissions there. Do not mount
  Windows/DrvFS SSH files directly at `${HOME}/.ssh`; their effective `0777`
  mode causes OpenSSH to reject private keys.
