# Runtime Mount Permissions

## Problem

When creating an ArcticTraining sandbox, the script initially mounted host paths
directly:

- `/home/howard/.agents/skills` -> `${CONTAINER_HOME}/.agents/skills`
- `/home/howard/.ssh` -> `${CONTAINER_HOME}/.ssh:ro`

Local `test -r` / `test -x` checks passed for the current user, but Docker daemon
mount creation failed:

```text
error while creating mount source path '/home/howard/.agents/skills': mkdir /home/howard/.agents: permission denied
error while creating mount source path '/home/howard/.ssh': mkdir /home/howard/.ssh: permission denied
```

The issue is that validating the current user's access to the original path is
not enough. Docker must be able to mount the source path from its own host
namespace and permission context.

On `wingene-78`, `/home` is mounted from NFS while `/tmp2` is local ext4:

```text
/home  192.168.1.81:/home  nfs4
/tmp2  /dev/nvme0n1p1      ext4
```

This means Docker can fail to stat or create bind source paths under
`/home/howard/*`, even when the `howard` login shell can read them. A useful
diagnostic pattern is:

```text
docker run --rm -v /home/howard/.ssh:/host-ssh alpine ls -la /host-ssh
# may fail with: error while creating mount source path ... permission denied

docker run --rm -v /tmp2/<project>/.runtime/.ssh:/host-ssh alpine ls -la /host-ssh
# should succeed when the project runtime directory is local and accessible
```

## Fix Used

Prepare project-local runtime copies and mount those instead:

- `${PROJECT_DIR}/.runtime/skills` -> `${CONTAINER_HOME}/.agents/skills`
- `${PROJECT_DIR}/.runtime/.ssh` -> `${CONTAINER_HOME}/.ssh:ro`

For SSH, copy only the prepared files used by the sandbox:

- `id_ed25519`
- `id_ed25519.pub`
- `known_hosts`
- `authorized_keys`

Then apply strict permissions:

```text
.runtime/.ssh      700
id_ed25519         600
id_ed25519.pub     644
known_hosts        644
authorized_keys    600
```

## Recommendation

When generating project-local sandbox scripts, prefer `.runtime` mount sources
for SSH and skills if direct Docker mounting of home-directory paths may fail.
Validation should check the actual paths that Docker will mount, not only the
original source paths.
