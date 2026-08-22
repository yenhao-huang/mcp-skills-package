---
name: create-drone-ci
description: >
  Create, configure, validate, or repair Drone CI for a Git repository. Use
  when the user asks to add Drone CI, initialize `.ci`, start a Drone server or
  Docker runner, connect Drone to Gitea webhooks, create `.drone.yml`, define
  pipeline steps or triggers, or standardize CI docs, scripts, and tests.
---

# Create Drone CI

Create a repository-local Drone CI setup with infrastructure and task assets
organized under `.ci/`, while keeping Drone's canonical pipeline entry point at
the repository root as `.drone.yml`.

## Workflow

1. Identify the target repository, Git provider, public Drone URL, runner host,
   and whether the user wants scaffolding only or also wants services started.
2. Read `STATE.md`; for a new run, reset it from
   `references/template/STATE.template.md`.
3. Read the relevant references and mark the current step `in_progress` in
   `STATE.md` before changing the target repository.
4. Inspect the target repository's instructions, existing CI, language,
   tests, dirty status, remotes, and Docker/Compose conventions.
5. Create the repository only when requested. Never invent a remote URL,
   organization, credentials, ports, storage paths, or public callback URL.
6. Scaffold the baseline with:

   ```bash
   python3 references/scripts/scaffold_drone_ci.py --repo <repo-path>
   ```

   Add `--init-git` only when the target is not already a Git repository. Add
   `--with-dockerfiles` only when custom Drone images are actually required.
7. Replace the starter smoke command with the repository's real test command,
   then keep task scripts under `.ci/scripts/` and their tests under
   `.ci/tests/`.
8. Populate `.ci/drone/.env` locally from `.env.example`. Generate
   `DRONE_RPC_SECRET` securely and create the Git provider OAuth application;
   never commit secrets.
9. Validate static configuration before starting services. If the user asked
   to start them, run the checked-in Compose stack, inspect server and runner
   logs, authenticate to Drone, and activate the repository so Drone creates
   the provider webhook.
10. Update `STATE.md` with concrete evidence and report changed paths,
    validation, runtime status, and any manual OAuth or repository activation
    step that remains.

## References

- Read `references/drone-conventions.md` before choosing provider settings,
  server/runner topology, image policy, pipeline triggers, or Dockerfiles.
- Read `references/rules/filetree.md` before adding, moving, or removing skill
  or target-repository files.
- Read `references/rules/env.md` before creating `.env`, installing tools, or
  starting Drone services.
- Read `references/validation.md` before validating or starting the stack.
- Read `references/rules/state-rules.md` before updating `STATE.md`.

## Rules

- Use `.drone.yml`, not `.drone.ci`, unless the installed Drone server is
  explicitly configured with a non-default repository config path.
- Keep Server/Runner infrastructure in `.ci/drone/`, task documentation in
  `.ci/docs/`, task scripts in `.ci/scripts/`, and script tests in
  `.ci/tests/`.
- Use the official `drone/drone:2` and `drone/drone-runner-docker:1` images
  directly by default. A normal installation needs `docker pull` or
  `docker compose pull`, not a custom Drone image build.
- Create Dockerfiles only for a concrete extension such as an internal CA,
  approved plugin, or required diagnostic tool. Preserve the official Drone
  entrypoint and pin the resulting base image for production.
- Treat a Docker runner with `/var/run/docker.sock` as host-level trusted
  infrastructure. Do not enable untrusted repositories or privileged pipeline
  execution without explicit authorization.
- Do not start Docker, create OAuth applications, activate repositories,
  create webhooks, commit, or push unless the user's request authorizes that
  action.

## Output

Report:

- Repository and files created or changed.
- Pipeline steps and trigger conditions.
- Static validation and, when requested, Server/Runner runtime status.
- Git provider OAuth/webhook activation status.
- Remaining placeholders, secrets, or manual steps.
