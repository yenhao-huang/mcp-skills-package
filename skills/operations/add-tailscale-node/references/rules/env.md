# Environment Rules

## Runtime

Primary language: POSIX-compatible shell commands
Runtime version: Linux container userspace supported by the installed Tailscale release
Package manager: Existing container package manager only
Frameworks: Docker, Podman, LXC, or Kubernetes as detected
Service manager: Existing init or supervisor; otherwise a clearly labeled temporary daemon process
Required services: Tailscale coordination service and the user's existing cluster endpoint

## Home Multi-Node Context

- Home is an existing configurable SSH endpoint, currently defaulting to
  `user@100.88.157.6` on Windows. Explicit user input overrides workspace inventory
  fields, which override template defaults; verify identity before changes.
- Windows home operations use native OpenSSH and administrator PowerShell for
  protected key files, ACLs and firewall changes. Linux nodes use their existing
  SSH server and package/service manager. Do not assume home always runs Windows.
- Exchange only SSH public keys. Tailscale membership and keys do not replace
  OpenSSH account authorization. Record both directional login results per node.

## Rules

- Inspect `/etc/os-release`, PID 1, runtime metadata, networking devices, and
  installed commands before choosing a path.
- Do not install dependencies globally on the host.
- Verify time-sensitive install, Serve, and uninstall syntax against official
  Tailscale documentation before mutation.
- Do not invent container names, service ports, auth keys, state volumes, or
  tailnet policy selectors.
- Treat Docker or orchestrator configuration as the source of truth for
  persistent integration. A manual daemon inside a running container is
  temporary unless the container already has a supervisor and persistent state.
- Kernel mode needs an accessible `/dev/net/tun` character device and effective
  `NET_ADMIN` in the application's network namespace. Verify `NET_RAW` for
  ordinary ICMP tools; do not grant broad `--privileged` access as a shortcut.
- `TS_USERSPACE=false` configures the official image's `containerboot` entrypoint.
  For a directly managed daemon, change its actual arguments to `--tun=tailscale0`;
  an environment variable alone does not reconfigure a running `tailscaled`.
- Never expose secrets in command output, logs, committed files, or responses.
