# Separate home desktop

Use this procedure after resolving home through add-tailscale-node as described
in SKILL.md. Read its selected private inventory and verify the current home node,
SSH account and port; do not infer them from A's username or project SSH alias.
Use that skill only as the source of inventory and identity checks here: opening
VS Code does not run its Tailscale installation, key exchange or firewall workflow.

Home needs a logged-in graphical user, desktop VS Code, Remote - SSH and a
working SSH alias for the project host. Inspect these on home.

## Local Or Remote Launch

- **A is home:** invoke the verified desktop VS Code executable directly with
  `desktop_argv[1:]` in the active user's graphical session. Do not SSH to self.
  A Windows SSH/background session on home still needs the Interactive/Limited
  task below, run locally. On macOS, use the local `open` command below after
  verifying the session owner.
- **A is remote:** SSH to home's resolved account/host/port with BatchMode,
  strict host-key checking and a bounded timeout. Verify the returned machine
  and account before any desktop action. Run the Windows/macOS procedure below
  through that connection, not through A's local VS Code installation.

Optional machine-specific launch settings may be cached outside this repository
at `~/.config/start-code-review-env/desktop.json` (or a user-selected path).
This file is not a prerequisite. Discover the OS, logged-in desktop user and
VS Code executable through the verified local or SSH session when absent.
Cached endpoints/accounts must agree with the resolved inventory and node
identity; stale values do not override the inventory. An explicitly selected
user configuration remains an explicit override. Never store passwords or
private keys, and never guess another account after authentication fails.

## Workflow

1. Verify the resolved home identity and active graphical user using the selected
   route above. Locate VS Code and Remote - SSH. From a remote A, first verify
   SSH access using the resolved account and port; a failed connection stops
   home mutations. Record reachability, authentication and desktop readiness
   separately so an SSH login failure is not reported as missing configuration.
2. Prepare the target using open_workspace.py on A after checking the project
   alias on home. Pass host/path as data,
   never interpolate user text into shell source. For PowerShell transport use
   UTF-16LE EncodedCommand with a serialized/base64 JSON payload, and invoke a
   verified executable with an argument array. For POSIX transport shell-quote
   each argument. SSH joins remote arguments into shell text: local argv alone
   does not protect remote quoting.
3. Windows (remote SSH or a local noninteractive shell): a background process
   alone does not establish an interactive desktop.
   Use Task Scheduler with the verified logged-in user's Interactive logon type
   and limited run level, never SYSTEM or a password-based background login.
   Create a uniquely named `StartCodeReviewEnv-<request-id>` on-demand task whose
   action is the verified Code.exe and correctly Windows-quoted arguments from
   desktop_argv (excluding its initial code token). Start the task and inspect
   Get-ScheduledTaskInfo/LastTaskResult and task state with a bounded poll.
   Do not overwrite an existing task, elevate permissions, or change login
   policies. If registration is denied, report it and provide the desktop
   command. Retain the task identity when completion cannot be established.
4. macOS: verify the invoking account owns the active desktop session. Invoke
   `/usr/bin/open -a 'Visual Studio Code' --args --new-window --remote
   ssh-remote+PROJECT_HOST REMOTE_PATH` using separately quoted arguments.
   If the desktop session is inaccessible, return the command for local use;
   do not use sudo or launch into another user's session.
5. Report submission separately from GUI evidence. Verify the opened host and
   folder through available desktop evidence or user confirmation. With an
   existing VS Code process, the new window's logs may be under an older process
   log directory; inspect recently modified window/Remote SSH logs and workspace
   metadata rather than only the newest empty log directory. If SSH times out
   during initial server setup, check the same window for subsequent resolution
   before retrying. Do not loop indefinitely or open duplicate windows.
6. Windows task cleanup: after its action finishes, unregister only this
   request's task (without closing VS Code); if still running or uncertain,
   retain it and record its name for later cleanup. Rollback removes that exact
   task and this request's temporary transport files only. Remove local desktop
   configuration only if created for setup, or restore its prior contents.

Validation is per run and platform. Workspace creation alone does not validate
SSH or GUI launch. Record observed session/task/connection evidence and leave
untested launch routes explicit; do not treat historical STATE.md blockers as
current machine configuration.

Official references:
- https://learn.microsoft.com/en-us/windows/win32/taskschd/schtasks
- https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/new-scheduledtaskprincipal
- https://code.visualstudio.com/docs/remote/ssh
