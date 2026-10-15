# Environment

- Primary language: Python 3.9+ standard library; deployed image uses Python 3.11.
- Dependencies: Git, OpenSSH client, CA certificates and Asia/Taipei timezone data.
  The Dockerfile installs OS packages inside the dedicated image, not the host.
- Runtime: Docker Compose on w78_pretrieval_tailscale; no model API required.
- Source service: existing Gitea at 192.168.1.76:3000.
- Destination: git@github.com:yenhao-huang/daily.git, main branch.
- Authentication: existing Git credential helper for Gitea, existing SSH identity
  and trusted known-hosts for GitHub. Verify user API before reading issue lists.
- Runtime secrets are read-only mounted files, never image layers or Git files.
- Persistent paths: externally configured state directory and user preferences
  directory. Preserve both across service restart/reinstall.
- See references/deploy/docker-compose.yml for service definition and
  references/schedule.md for lifecycle validation and rollback.
