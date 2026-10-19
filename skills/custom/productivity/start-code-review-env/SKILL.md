---
name: start-code-review-env
description: Open the current project or worktree in desktop VS Code on home, directly when running on home or over SSH from a remote machine. Resolve home through add-tailscale-node. Use for start-code-review-env executorch, start-code-review-env pretrieval, or opening the current project for review. Opening alone does not request a code audit.
---

# Start code review environment

The VS Code window belongs on **home**. The machine running this chat (A), home,
and the project SSH host are separate roles, even when two roles share a machine.
Use desktop VS Code; do not substitute code-server or VS Code Web.

Resolve home using [add-tailscale-node](../../../operations/add-tailscale-node/SKILL.md)
and its `references/home-multi-node.md` and
`references/template/home-nodes.template.yaml`. Read these from the current skill
package (or the installed add-tailscale-node skill), not an old runtime STATE.md.
They are the source of home machine/account defaults; do not duplicate those
values here or infer the SSH account from the account on A.

`references/projects.json` supplies preferred **project** SSH aliases on home:

| Project | Project SSH host |
| --- | --- |
| executorch | w78_sideproject_tailscale |
| pretrieval | w78_pretrieval_tailscale |

## Workflow

1. Identify the project family and target from the latest explicit user request,
   then the active conversation's project/worktree or PR checkout. Resolve the
   absolute directory from that evidence. A bare directory name needs a verified
   parent path. A PR URL alone does not establish a checkout location. Use cwd
   only when it is verified to belong to the requested project on the target
   machine. Never use a previous run's STATE.md, generated workspace, or historical
   example as a default directory. Ask for the path if evidence is absent or
   ambiguous; do not silently open a different project.
2. Resolve home host, SSH account, port and machine identity using the
   add-tailscale-node home reference: explicit user values, then the selected
   private inventory, then its documented defaults, field by field. Verify the
   node using `tailscale status --json` and compare A's local identity with home.
   The operating system, local username, or presence of a code CLI alone does
   not prove A is home. If the required skill/inventory is missing, locate its
   current source before asking for information already recorded there.
3. Read `references/rules/env.md` and `references/home-desktop.md`. Choose the
   launch route from the verified identity:
   - **A is home:** open desktop VS Code directly in the active user's session;
     do not SSH back to home. If the shell is noninteractive, use the local
     interactive-session procedure in the home reference.
   - **A is remote:** connect to the resolved home account over SSH and use the
     home reference's interactive desktop procedure. A local code CLI or IPC
     socket on A is not a substitute for this route.
   A missing optional `desktop.json` is not a blocker when the inventory and
   endpoint inspection supply the needed values.
4. Resolve the project alias from explicit user input or `references/projects.json`.
   Inspect its effective SSH configuration **on home** and verify the intended
   project machine and directory when accessible. If a preferred alias is absent,
   an existing alias may be used only after verifying it reaches the same intended
   node/account and checkout; record that substitution. Do not edit SSH config.
   Check git status without switching branches or resetting changes. A known
   directory on A is not proof it exists on a different project machine.
5. Run `references/scripts/open_workspace.py PROJECT --path ABSOLUTE_PATH
   --output-dir NEW_OUTPUT_DIRECTORY`. Add `--host VERIFIED_ALIAS` for an explicit
   override or a verified equivalent alias from step 4. Use a new per-request
   output directory so different worktrees do not collide. On home, execute the
   returned `desktop_argv` with the verified desktop executable, or use `--launch`
   when its local CLI/session checks apply. From a remote machine, send the
   resulting argument array over SSH using `references/home-desktop.md`;
   `--launch` itself does not SSH to home.
6. Validate the workspace URI's project host and directory. Distinguish prepared,
   launch_requested, launch_failed, connection verified through logs, and visually
   verified GUI. CLI/task success alone does not prove a connected VS Code window.
   If home access fails, retain the workspace and report the specific connection
   failure; do not guess alternate accounts or open another environment.
7. Record the home resolution sources, A/home identity comparison, project
   host/path, observed branch, launch route/status and remaining blockers in
   STATE.md. Opening does not authorize code edits, reviews, commits, pushes,
   SSH credential changes, or community messages.

Closing the window reverses opening; remove only the generated workspace to
remove the artifact. Keep generated files outside reviewed repositories.
