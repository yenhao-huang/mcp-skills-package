# Environment

- Primary language: Python 3.9+ with standard library only.
- Runtime dependencies: Git, timezone data for Asia/Taipei, access to internal
  Gitea at 192.168.1.76:3000, and an existing Git credential helper entry.
- Frameworks/package manager: none required; do not install global packages.
- Service manager: none; this helper does not start a service or scheduler.
- Authentication: use `git credential fill` in memory with prompting disabled.
  Existing Git username/password or token-as-password works via HTTP Basic.
  Verify `/api/v1/user` succeeds before querying issues. Do not change helpers,
  scan other accounts for secrets, or provision credentials during a reminder.
- Scheduling requires a supported automation surface on a host with LAN access.
