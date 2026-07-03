# Mount Rules

Use this reference before asking mount questions, validating host paths,
preparing SSH files, or handling Docker socket and extra mounts.

## Required Mount Questions

Before writing, updating, or running a sandbox script, ask for:

- Repo/workspace mount: host path and container path. Default container path
  only after confirmation: `/workspace`.
- Model mount: host path and container path, or confirmation of no model mount.
  Default container path only after confirmation: `/models`.
- SSH mount: host SSH directory or prepared SSH files, or confirmation of no SSH
  mount. Default container path only after confirmation:
  `${CONTAINER_HOME}/.ssh`.
- Data mount: host path and container path, or confirmation of no data mount.
  Default container path only after confirmation: `/data`.
- Docker socket: whether to mount `/var/run/docker.sock` to
  `/var/run/docker.sock`; set `DOCKER_SOCK=''` to disable.
- Extra mounts: any additional `host_path:container_path` or
  `host_path:container_path:ro` entries.

Skills directories are not part of the standard sandbox mount questions and
should not be mounted unless the user explicitly provides one as an extra
mount.

If the user asks to proceed without answering, create only a configurable script
with empty `WORKSPACE_DIR`, `MODEL_DIR`, `SSH_DIR`, `DATA_DIR`, and
`EXTRA_MOUNTS`; include configurable `DOCKER_SOCK` and
`CONTAINER_DOCKER_SOCK`; and make the script fail until `WORKSPACE_DIR` is set.

## Path Rules

- Do not infer the repo/workspace from `cwd`, parent directories, or search
  results; use only confirmed user input.
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
- If Docker socket mounting is confirmed, check that `DOCKER_SOCK` exists, is a
  socket, and is readable and writable by the current user.
- Add the Docker socket's numeric group id to `docker run` with
  `--group-add "$(stat -c '%g' "${DOCKER_SOCK}")"` when the socket is mounted.
- If a path is missing, ask a correction question in this form:
  `repo 找不到，你想找的是不是 <candidate>?`, replacing `repo` with the mount
  label.
- If a path exists but lacks required permissions, ask whether copying the
  needed files into `.runtime/` is acceptable. Copy only after explicit
  confirmation.
- Generated scripts must fail fast with clear errors for missing paths or
  insufficient mount permissions.

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
- Mount prepared SSH directories read-write so the sandbox user can update
  `known_hosts`, SSH config, and other per-user SSH state.
