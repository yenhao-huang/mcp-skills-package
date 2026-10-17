---
name: add-tailscale-node
description: Add or manage a Linux container Tailscale node and connect it bidirectionally to a configurable home machine. Use for home multi-node SSH, Docker or LXC kernel networking, public-key exchange, userspace migration, or explicit proxy setup and safe removal without enrolling the container host.
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

For home multi-node setup, read `references/home-multi-node.md` and use
`references/template/home-nodes.template.yaml` as the non-secret inventory.
The current home default is `user@100.88.157.6`; it is an overridable connection
setting, never a fixed identity or an instruction to alter that machine.

## Workflow

1. Resolve the exact target container and runtime before mutation. If the user
   means the current container, inspect that environment; do not infer its
   boundary from an empty nested `docker ps` or create another container.
2. Confirm the desired direction: cluster to container, container to cluster,
   or both. Identify only the required protocols and ports.
   For home multi-node requests, resolve home from explicit user input, then
   the selected inventory, then the default. Adding a node in this mode includes
   both home -> node and node -> home SSH; follow the home reference to exchange
   public keys, update exact peer allowlists and validate each direction.
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
- Tailnet membership or online status alone does not approve a peer for home SSH.
  Preserve existing approved peers, restrict additions to the requested nodes,
  and never transfer private keys or treat Tailscale node keys as SSH keys.

## Output

Report the selected networking mode, commands or changes made, connectivity
validation, host-isolation result, uninstall level if applicable, and any
restart or persistence limitation.
For home multi-node runs, also report the resolved home endpoint and a per-node
matrix of both SSH directions, public-key fingerprints, pending/offline nodes,
and the inventory and rollback paths.
