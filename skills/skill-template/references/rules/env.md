# Environment Rules

Use this reference before installing packages, starting services, choosing a
framework, or assuming a runtime language.

## Package Management

- Use `.venv` as the local Python package environment when the skill or project
  needs Python dependencies.
- If `.venv` does not exist and Python dependencies are required, tell the user
  the environment is missing before installing packages or running dependency
  commands.
- Do not install packages globally.
- Prefer the repository's existing dependency files, such as `requirements.txt`,
  `pyproject.toml`, `package.json`, or lockfiles, over ad hoc installs.

## Service Management

- Use `docker-compose.yml` as the source of truth for local services.
- If a required service is not defined in `docker-compose.yml`, tell the user
  which service is missing and what the workflow expected.
- Do not invent service names, ports, credentials, or volumes when the
  repository does not define them.
- If multiple compose files exist, identify the relevant one before starting or
  modifying services.

## Frameworks And Languages

- Record the expected programming language for the skill here when creating a
  concrete skill from this template.
- Record the expected framework or runtime here when the workflow depends on
  one, such as FastAPI, React, Next.js, PyTorch, SQLAlchemy, or Alembic.
- If the repository does not clearly declare the expected language or
  framework, tell the user before choosing one.
- Prefer existing project frameworks and patterns over introducing new ones.

## Template Fields To Fill

When adapting this template, replace these placeholders:

```text
Primary language:
Runtime version:
Package manager:
Frameworks:
Service manager:
Required services:
```
