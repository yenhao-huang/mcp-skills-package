---
name: lanfuse-install
description: Install, configure, validate, integrate, stop, reinstall, or uninstall a local self-hosted Langfuse deployment with Docker Compose, including Hermes observability setup. Use for Langfuse local deployment, first-run initialization, Docker Compose troubleshooting, Hermes Langfuse traces, Windows Hermes venv issues, and safe Langfuse cleanup.
---

# Lanfuse Install

Manage a local Langfuse deployment and optional Hermes observability integration
without exposing secrets or deleting persistent data unexpectedly.

## Required Context

Read these files before acting:

- `references/rules/env.md`
- `references/rules/filetree.md`
- `references/rules/state-rules.md`
- `references/langfuse-installation.md`
- `references/hermes-integration.md` when Hermes is in scope

Reset `STATE.md` from `references/template/STATE.template.md` for a new run,
then record concrete evidence as each phase progresses.

## Workflow

1. Identify the target OS, Langfuse directory, Docker Compose file, requested
   operation, and whether Hermes runs natively or in Docker. Inspect existing
   containers, volumes, `.env` files, and project data before mutation.
2. For installation, follow `references/langfuse-installation.md`: clone or
   reuse the exact Langfuse checkout, prepare first-run initialization values
   and unique secrets outside version control, review the checked-in Compose
   file, then start its services.
3. Validate the deployment with Compose service state, container health and
   logs, the local HTTP endpoint, and an authenticated UI check. Do not infer
   initialization success only from running containers.
4. When Hermes integration is requested, follow
   `references/hermes-integration.md`: install the SDK in Hermes' actual
   environment, enable the plugin, write variables to the exact Hermes `.env`
   path, select the URL for the runtime topology, restart only when required,
   and prove that a new trace arrives.
5. For rollback, distinguish stop-only, container removal with data retained,
   volume deletion, image deletion, and checkout deletion. Require explicit
   confirmation before deleting volumes, credentials, or the checkout.
6. When validating this reversible workflow, use a disposable target and run
   the exact lifecycle `install -> rollback/uninstall -> install again` from
   `references/langfuse-installation.md`. Record commands and observable
   assertions in `STATE.md`; if it cannot run safely, mark validation blocked.
7. Report the checkout path, Compose project, service and endpoint checks,
   Hermes trace evidence when applicable, retained or removed state, and any
   remaining manual login or credential action.

## Guardrails

- Treat the checked-out `docker-compose.yml` as the service source of truth.
- Never commit `.env`, API keys, passwords, salts, or generated encryption
  material. Redact them from logs and state evidence.
- Initialization variables only affect a genuinely empty database. Use the
  Langfuse UI for keys and users after initialization.
- Do not replace user-modified Compose files or `.env` files without approval.
- `docker compose down` preserves named volumes; `docker compose down -v` does
  not. Require explicit confirmation before using `-v`.
- Resolve and display the exact checkout path before deleting it. Never use an
  unresolved variable, broad glob, home directory, or workspace root.
- Do not rebuild or restart Hermes when a native one-shot invocation will
  reload configuration automatically.

## Output

Report actions performed, validation results, the lifecycle phase reached,
data preservation or deletion decisions, and any blocked runtime check.
