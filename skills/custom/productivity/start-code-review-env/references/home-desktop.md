# Separate home desktop

Use this procedure when the agent runs on A and VS Code must open on home.
Home must have a logged-in graphical user, VS Code, Remote - SSH, and its own
working SSH alias for the project host. A's SSH config is not home's config.

Store machine-specific settings outside the published skill, at
`~/.config/start-code-review-env/desktop.json` on A (or an explicit user path):

```json
{
  "transport": "ssh",
  "ssh_alias": null,
  "platform": "windows",
  "desktop_user": null,
  "code_executable": null
}
```

Null fields are unconfigured, not defaults. Obtain the home SSH alias and
logged-in desktop identity from the user or verified environment; never guess
that the project alias is the home alias. Never request passwords/private keys
in chat. `platform` supports windows or macos. macOS can resolve the installed
Visual Studio Code app instead of requiring code_executable.

## Workflow

1. Read configuration, verify SSH access with BatchMode and a bounded connection
   timeout, identify home OS and logged-in graphical user, and locate VS Code.
   Preserve SSH host-key verification. A failed connection stops home mutations.
2. Prepare the target using open_workspace.py on A. Pass host/path as data,
   never interpolate user text into shell source. For PowerShell transport use
   UTF-16LE EncodedCommand with a serialized/base64 JSON payload, and invoke a
   verified executable with an argument array. For POSIX transport shell-quote
   each argument. SSH joins remote arguments into shell text: local argv alone
   does not protect remote quoting.
3. Windows: SSH execution alone does not establish an interactive desktop.
   Use Task Scheduler with the verified logged-in user's Interactive logon type
   and limited run level, never SYSTEM or a password-based background login.
   Create a uniquely named `StartCodeReviewEnv-<request-id>` on-demand task whose
   action is the verified Code.exe and correctly Windows-quoted arguments from
   desktop_argv (excluding its initial code token). Start the task and inspect
   Get-ScheduledTaskInfo/LastTaskResult and task state with a bounded poll.
   Do not overwrite an existing task, elevate permissions, or change login
   policies. If registration is denied, report it and provide the desktop
   command. Retain the task identity when completion cannot be established.
4. macOS: verify the SSH account owns the active desktop session. Invoke
   `/usr/bin/open -a 'Visual Studio Code' --args --new-window --remote
   ssh-remote+PROJECT_HOST REMOTE_PATH` using separately quoted arguments.
   If the desktop session is inaccessible, return the command for local use;
   do not use sudo or launch into another user's session.
5. Report submission separately from GUI evidence. Verify the opened host and
   folder through available desktop evidence or user confirmation. Do not loop
   indefinitely or retry in a way that opens duplicate windows.
6. Windows task cleanup: after its action finishes, unregister only this
   request's task (without closing VS Code); if still running or uncertain,
   retain it and record its name for later cleanup. Rollback removes that exact
   task and this request's temporary transport files only. Remove local desktop
   configuration only if created for setup, or restore its prior contents.

Current deployment status: no home SSH destination supplied; Windows interactive
launch and macOS desktop launch remain untested. Before claiming deployment
validated, exercise creation -> removal -> recreation on the actual target and
verify a real window. This reference describes the agent-executed transport;
the workspace helper alone does not implement the home connection.

Official references:
- https://learn.microsoft.com/en-us/windows/win32/taskschd/schtasks
- https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/new-scheduledtaskprincipal
- https://code.visualstudio.com/docs/remote/ssh
