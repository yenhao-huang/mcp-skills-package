# Environment

The workspace helper requires Python 3 standard library. Home requires desktop
VS Code, Remote - SSH and a working project SSH alias. No packages are
auto-installed. Read the add-tailscale-node home inventory/defaults referenced
by SKILL.md to identify home, then inspect the actual execution environment;
this skill can run either on home or on a remote machine.

On home, use the active desktop session directly. From a remote machine, use
home's resolved SSH account and the interactive launch procedure in
`../home-desktop.md`. Remote cached .vscode-server binaries, DISPLAY or an IPC
socket do not prove they control home. Do not pick arbitrary sockets from /tmp.
The helper's --launch performs only local CLI/session checks, not home identity
resolution or SSH transport; choose the route before invoking it.

Check the project alias on home. The optional desktop.json caches launch details;
it is neither required to discover home nor a replacement for the current
add-tailscale-node inventory. Preserve SSH host-key checks and existing user
configuration. No Tailscale or SSH reconfiguration is needed to open a window.

Official references:
- https://code.visualstudio.com/docs/remote/ssh
- https://code.visualstudio.com/docs/configure/command-line
