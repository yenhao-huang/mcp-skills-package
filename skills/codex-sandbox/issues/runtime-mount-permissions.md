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

## Fix Used

Prepare project-local runtime copies and mount those instead:

- `${PROJECT_DIR}/.runtime/skills` -> `${CONTAINER_HOME}/.agents/skills`
- `${PROJECT_DIR}/.runtime/.ssh` -> `${CONTAINER_HOME}/.ssh:ro`

For SSH, copy only the prepared files used by the sandbox:

- `id_ed25519`
- `id_ed25519.pub`
- `known_hosts`

Then apply strict permissions:

```text
.runtime/.ssh      700
id_ed25519         600
id_ed25519.pub     644
known_hosts        644
```

## Recommendation

When generating project-local sandbox scripts, prefer `.runtime` mount sources
for SSH and skills if direct Docker mounting of home-directory paths may fail.
Validation should check the actual paths that Docker will mount, not only the
original source paths.
