# Environment

Requires Python 3 standard library for workspace generation. Desktop requires
VS Code, Remote - SSH and an existing SSH alias. No packages are auto-installed.
This Codex shell is a headless remote container: no DISPLAY, no PATH code and
no inherited VSCODE_IPC_HOOK_CLI. Cached .vscode-server binaries alone cannot
open a desktop window. Never pick arbitrary IPC socket files from /tmp.

Official references:
- https://code.visualstudio.com/docs/remote/ssh
- https://code.visualstudio.com/docs/configure/command-line

For a separate Windows/macOS home desktop, follow ../home-desktop.md.
Home access is not configured; do not infer it from the project SSH alias.
