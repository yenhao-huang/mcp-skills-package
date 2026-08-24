---
name: tailscale-in-container
description: Install, start, integrate, diagnose, validate, stop, or uninstall Tailscale inside an existing Docker or LXC container while keeping the host out of the tailnet. Use for container-to-cluster connectivity, userspace networking, /dev/net/tun capability checks, Tailscale Serve, proxy access, and safe removal or complete cleanup.
---

# Tailscale In Container

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

1. Establish whether the target is Docker, Podman, LXC, or Kubernetes and
   whether it is already running.
2. Confirm the desired direction: cluster to container, container to cluster,
   or both. Identify only the required protocols and ports.
3. Inspect the container before mutation: distro, init system, installed
   binaries, daemon state, `/dev/net/tun`, Linux capabilities, state path, and
   current Tailscale identity.
4. For installation, verify the current commands against official Tailscale
   documentation, install only inside the container, choose kernel or
   userspace mode, authenticate without exposing secrets, and configure the
   minimum required path.
5. For removal, first determine whether the user wants a disconnect, package
   uninstall with identity preserved, or complete removal. Treat state deletion
   and tailnet device deletion as separate destructive actions.
6. Validate the requested traffic path and confirm the host itself was not
   enrolled or exposed.

## Guardrails

- Do not install or authenticate Tailscale on the host unless explicitly asked.
- Do not use host networking for a container-only integration.
- A running container cannot gain new Docker capabilities or devices. If it
  lacks `/dev/net/tun` or `NET_ADMIN`, use userspace mode or explain that
  transparent Layer 3 networking requires container recreation.
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
