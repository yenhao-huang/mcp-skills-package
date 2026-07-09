# Repo Create Environment Rules

Use this reference before writing `docs/rules/environment.md` for a target
repository.

## Decision Policy

- Read existing dependency files before choosing environment rules.
- Do not invent language versions, package managers, ports, credentials,
  service names, model paths, or dataset paths.
- If an environment decision is missing, record it as a user decision in the
  generated docs.

## Fields To Capture

Capture these when they are known:

```text
Primary languages:
Runtime versions:
Package managers:
Lockfiles:
Virtual environment:
Service manager:
Required services:
Secrets location:
Data/model storage:
Generated artifacts:
Validation commands:
```

## Validation

Prefer commands the repository already defines. If none exist, validate docs
with path checks and `git diff --check`.
