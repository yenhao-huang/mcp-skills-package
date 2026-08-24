# Environment Rules

## Runtime

Primary language: POSIX-compatible shell commands
Runtime version: Linux container userspace supported by the installed Tailscale release
Package manager: Existing container package manager only
Frameworks: Docker, Podman, LXC, or Kubernetes as detected
Service manager: Existing init or supervisor; otherwise a clearly labeled temporary daemon process
Required services: Tailscale coordination service and the user's existing cluster endpoint

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
- Never expose secrets in command output, logs, committed files, or responses.
