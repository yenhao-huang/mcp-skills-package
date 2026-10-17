---
name: code-review
description: Open the project or worktree currently discussed in VS Code over Remote SSH. Use for "code review executorch", "打開 vscode review", or requests to open the current project for review. Opening alone does not request an automated code audit or code changes.
---

# Code review workspace

Default SSH host alias: `w78_sideproject_tailscale` (resolved by the user's desktop SSH config).
Use the user's desktop VS Code with Remote - SSH, not a GUI installed on the remote server.

## Workflow

1. Resolve the project and absolute worktree path from the latest explicit user
   target, then the current chat's PR/worktree, then references/projects.json.
   The registry is a fallback, never override newer conversation context. For
   `code review executorch` in this conversation the target is
   `/workspace/executorch-worktrees/embedding-bag-review`. Inspect `git status
   --short --branch` if the same remote filesystem is accessible. Do not switch
   branches or reset changes. Ask only if multiple targets remain ambiguous.
2. Read references/rules/env.md. Determine where tools execute: desktop or remote
   container. Use a verified desktop launch tool if available. Otherwise use a
   desktop `code` CLI, or an inherited working `VSCODE_IPC_HOOK_CLI` bridge to an
   already connected client. Do not guess another user's IPC socket or conclude
   desktop VS Code is absent merely because a remote shell lacks `code`.
3. Run references/scripts/open_workspace.py PROJECT --path ABSOLUTE_PATH
   --output-dir OUTPUT_DIRECTORY --launch. It creates a .code-workspace with the
   remote URI and attempts a launch only when the environment supports it.
   With a desktop tool, run the returned argument array on the desktop instead.
   The SSH alias and Remote - SSH extension must exist on that desktop; do not
   rewrite SSH config, keys or install extensions without a request.
4. Verify the target path/host in the generated workspace and inspect launch
   return status. A successful CLI request means launch requested, not proof of
   SSH connection or rendered GUI. Report GUI success only with actual desktop
   evidence. If unavailable, give the workspace file and exact desktop command;
   explicitly say automatic opening was unavailable. Do not substitute Codex's
   own file panel for VS Code.
5. Record target/branch, launch mode and evidence in STATE.md. This invocation
   opens a review workspace only. No edits, commits, pushes, PR reviews, community
   messages or automated audit are implied. If the user separately requests
   code review findings, inspect the specified diff after resolving the project.

Desktop command example:

```sh
code --new-window --remote ssh-remote+w78_sideproject_tailscale /workspace/executorch-worktrees/embedding-bag-review
```

Keep outputs outside the code repository unless requested. The workspace file
can be copied to the desktop and opened in VS Code. Closing its window reverses
opening; delete only the generated workspace file to remove the launch artifact.
