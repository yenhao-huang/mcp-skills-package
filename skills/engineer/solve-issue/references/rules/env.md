# Environment Rules

- Use the target repository's documented toolchain, package manager, runtime,
  and service definitions; do not introduce a replacement environment merely
  to solve the issue.
- Read repository instructions and dependency manifests before installing or
  upgrading packages.
- Use an existing project-local virtual environment when Python dependencies
  are required. Do not install packages globally.
- Do not invent service names, ports, credentials, or environment variables.
- Confirm GitHub CLI authentication before relying on `gh` for remote writes.
- Never expose tokens, credentials, private keys, or sensitive issue content in
  command output, commits, pull requests, or work notes.
