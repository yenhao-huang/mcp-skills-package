---
name: add-tailscale-node
description: Add or manage a Tailscale node inside a Linux container without enrolling its host. Use for Docker or LXC kernel networking, direct SSH and bidirectional tailnet connectivity, migration from userspace mode, or explicit userspace proxy setup and safe removal.
---

# Add Tailscale Node

Manage Tailscale inside a container without enrolling the container host in the
tailnet.

## Required Context

Read these files before acting:

- `references/rules/env.md`
- `references/rules/filetree.md`
- `references/rules/state-rules.md`
- `references/tailscale-container-workflow.md`

Reset `STATE.md` from `references/template/STATE.template.md` for a new run,
then record concrete evidence as each phase progresses.

## Workflow

1. Resolve the exact target container and runtime before mutation. If the user
   means the current container, inspect that environment; do not infer its
   boundary from an empty nested `docker ps` or create another container.
2. Confirm the desired direction: cluster to container, container to cluster,
   or both. Identify only the required protocols and ports.
3. Inspect the container before mutation: distro, init system, installed
   binaries, daemon state, `/dev/net/tun`, Linux capabilities, state path, and
   current Tailscale identity.
4. Prefer kernel networking for a new node and ordinary direct SSH. Follow
   the kernel setup and migration sections in the workflow reference. Verify
   TUN access and `NET_ADMIN`; preserve the existing node state and runtime
   configuration. If kernel mode is requested but unavailable, report the
   required runtime change rather than substituting userspace mode. Use the
   userspace proxy path only when requested or accepted by the user.
5. Verify current commands against official documentation, install only inside
   the target container, authenticate without exposing secrets, and configure
   only the required traffic. Record changed files, supervisor settings, and
   the matching rollback procedure in `STATE.md`.
6. For removal, first determine whether the user wants a disconnect, package
   uninstall with identity preserved, or complete removal. Treat state deletion
   and tailnet device deletion as separate destructive actions.
7. Validate both requested traffic directions with real application clients.
   For kernel mode, prove that `tailscale0` and policy routing exist in the
   application container and normal SSH works without a proxy. Confirm the
   host itself was not enrolled or exposed, and record evidence and limitations
   in `STATE.md`.

## Guardrails

- Do not install or authenticate Tailscale on the host unless explicitly asked.
- Do not use host networking for a container-only integration.
- Missing Docker device mappings or capabilities require a runtime change and
  usually container recreation. Prepare the exact change while preserving
  mounts, identity state, application configuration, and a recovery path; do not
  restart or recreate a live node merely to edit this skill.
- When changing the only remote access path, establish console/runtime access
  or another verified recovery channel before stopping `tailscaled`.
- Never print, persist in shell history, or commit an auth key. Prefer a secret
  file, orchestrator secret, or interactive login URL.
- Do not publish host ports unless the user explicitly requests host access.
- Never delete `/var/lib/tailscale/tailscaled.state`, a state volume, or the
  tailnet machine record without explicit confirmation of complete removal.
- Do not stop unrelated processes. Resolve the exact `tailscaled` PID or service
  unit before stopping it.

## Output

Report the selected networking mode, commands or changes made, connectivity
validation, host-isolation result, uninstall level if applicable, and any
restart or persistence limitation.
