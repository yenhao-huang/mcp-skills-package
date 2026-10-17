---
name: start-code-review-env
description: Open the project or worktree discussed in the current conversation in desktop VS Code over Remote SSH, including a separate home desktop reached from the agent machine. Use for start-code-review-env executorch, start-code-review-env pretrieval, or opening the current project for review. Opening alone does not request a code audit.
---

# Start code review environment

Resolve the directory at runtime. `references/projects.json` maps project families
only to SSH aliases resolved on the desktop:

| Project | Project SSH host |
| --- | --- |
| executorch | w78_sideproject_tailscale |
| pretrieval | w78_sideproject_pretrieval |

The machine running this chat (A), the desktop running VS Code (home), and the
project SSH host are separate roles. Never substitute one role for another.

## Workflow

1. Identify the project family and target from the latest explicit user request,
   then the active conversation's project/worktree or PR checkout. Resolve the
   absolute directory from that evidence. A bare directory name needs a verified
   parent path. A PR URL alone does not establish a checkout location. Use cwd
   only when it is verified to belong to the requested project on the target
   machine. Never use a previous run's STATE.md, generated workspace, or historical
   example as a default directory. Ask for the path if evidence is absent or
   ambiguous; do not silently open a different project.
2. Choose the project host from the mapping, with an explicit user host override
   taking priority. Verify directory existence and repository identity on the
   project machine when accessible; otherwise label the target unverified.
   Check git status without switching branches or resetting changes. For
   ExecuTorch, discussing embedding-bag-review selects that checkout only while
   it is the active target. PRetrieval may select any current checkout/worktree
   on w78_sideproject_pretrieval; its root is not preconfigured.
3. Read references/rules/env.md. Determine which desktop should open. For home
   reached by SSH, read references/home-desktop.md and the user's local desktop
   config. Do not treat a code CLI on A as proof it controls home. If home access
   is missing, still prepare the workspace and report the missing configuration.
4. Run references/scripts/open_workspace.py PROJECT --path ABSOLUTE_PATH
   --output-dir NEW_OUTPUT_DIRECTORY. The path is required even for known
   projects. Add --host only for an explicit override. Use a new per-request
   output directory so different worktrees of the same project do not collide.
   With a verified local desktop or inherited live VS Code bridge, add --launch.
   For a separate home desktop, send the resulting desktop argument array using
   references/home-desktop.md instead; --launch itself does not SSH to home.
5. Validate the generated URI's host and directory. Distinguish prepared,
   launch_requested, launch_failed, and visually verified GUI. A successful CLI
   or task submission is not proof that VS Code connected. If home is unavailable,
   return the workspace and desktop command without claiming a window opened.
6. Record runtime target, evidence source, project host, desktop host, branch,
   launch mode/status and remaining blockers in STATE.md. Opening does not
   authorize code edits, reviews, commits, pushes, or community messages.

Closing the window reverses opening; remove only the generated workspace to
remove the artifact. Do not modify project files or SSH credentials as part of
opening. Keep generated files outside reviewed repositories.
