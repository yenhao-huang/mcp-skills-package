# W78 daily publication

The user selected `w78_pretrieval_tailscale` and authorized publishing reports
to `git@github.com:yenhao-huang/daily.git`, branch `main`, under
`wingene/pretrieval/`. Cadence is **08:30 Asia/Taipei**, replacing 04:00.
No Codex automation, ChatGPT desktop session or model API is needed to run it.
The W78 sandbox and its Docker daemon must remain available.

## Deploy

Use `references/deploy/docker-compose.yml` as the source of truth. Copy the
reviewed skill to a stable deployment directory before using Compose; do not
bind production to an ephemeral worktree. Record source commit/content hash.

Prepare an operator-owned env file outside Git containing only absolute paths:

```dotenv
RUN_UID=1016
RUN_GID=1016
NOTICE_STATE_DIR=/data/deployments/pretrieval-notice/state
NOTICE_PREFERENCES_DIR=/home/howard/.config/pretrieval-notice
GITEA_CREDENTIAL_FILE=/home/howard/.git-credentials
GITHUB_SSH_KEY=/home/howard/.ssh/id_ed25519
GITHUB_KNOWN_HOSTS=/home/howard/.ssh/known_hosts
```

These values describe the verified W78 environment. On another host, inspect
its UID/GID and existing authorized credential paths rather than assuming them.
Create the state/preferences directories as the runtime UID. Do not reset an
existing preferences file. The credential file must contain the existing Gitea
Git credential; the SSH key must already have write access to daily and the
known-hosts file must already trust github.com. Do not print or copy secrets
into the image. The image build context is the skill directory only.

For example, with the stable skill under `/data/deployments/pretrieval-notice/skill`:

```bash
docker compose --env-file /data/deployments/pretrieval-notice/compose.env -p pretrieval-notice -f /data/deployments/pretrieval-notice/skill/references/deploy/docker-compose.yml up -d --build
```

Compose uses `restart: unless-stopped`, a non-root user, a read-only root
filesystem, dropped capabilities, a small temporary clone volume, bounded
logs, and read-only credential/preferences mounts. It publishes no ports and
does not install or change Tailscale on either the host or existing sandbox.

## Verify and publish immediately

Use the same Compose command prefix for these operations:

- `ps`: expect `notice` running and healthy.
- `logs --tail 30 notice`: publication paths or sanitized error classes only.
- `exec -T notice python3 /app/references/scripts/notice.py --preferences /preferences/preferences.json report`:
  preview and verify live Gitea connectivity.
- `exec -T notice python3 /app/references/scripts/publish.py once`:
  publish one report immediately without changing the daily scheduled slot.
- Read `${NOTICE_STATE_DIR}/scheduler.json` for `next_run`, `heartbeat` and
  `last_error`; `next_run` includes `+08:00`.
- Read `last-published.json` for the verified published path, and open
  `https://github.com/yenhao-huang/daily/blob/main/<path>`.

The publisher verifies pushed file contents via a new clone before marking
success. Updating priority preferences on the host takes effect next run.

## Report filenames

New reports use `wingene/pretrieval/NNNNNN_YYYY-MM-DD_HHMMSS.md`. With an empty
prefixed archive, the first ID is `999999`; each subsequent report uses the
minimum existing six-digit ID minus one, preserving leading zeros. For example:

```text
999997_2026-10-17_083000.md
999998_2026-10-16_083000.md
999999_2026-10-15_083000.md
```

The publisher scans a fresh clone on each push attempt. If a concurrent writer
publishes another report first, the rejected push retries against the new
remote minimum instead of reusing its consumed ID. At `000000`, a new report
fails without wrapping or renumbering; identical already-published reports can
still be verified and reused.

`pending.json` retains the original timestamp-only filename as the retry key
and the exact rendered report. Before allocating an ID, resolve that timestamp
against both prefixed and legacy filenames. An identical existing report is
returned unchanged; different contents or multiple files for the same timestamp
are rejected. This also recovers a successful push whose reply was lost, even
if newer reports have since been published. `last-published.json` records the
actual remote `path` and prefixed `filename` after successful verification (or
the unchanged legacy filename when recovering an older report).

This update does not rename historical files or change saved priorities,
cron/Compose settings or slot timestamps. For newest-first ordering across the
whole existing archive, coordinate a separately reviewed one-time migration of
legacy timestamp-only files before deploying the new naming policy. Seed that
migration from oldest to newest at `999999`, then count down, update affected
links, and keep any already-prefixed IDs unchanged. Do not blindly prepend IDs
to mixed layouts: prepare a collision-free mapping first. Legacy files remain
readable for retry compatibility; a mixed legacy/prefixed archive is not claimed
to be globally chronological. No archive migration is performed by `once` or
`serve`.

## Scheduling and failure semantics

- First start chooses the next future 08:30; use `once` for an immediate sample.
- Persist `next_run` and a heartbeat every minute. If stopped across one or
  more slots, catch up the latest due slot instead of flooding historical days.
- Save the rendered report and its timestamp-only retry filename to `pending.json` before pushing.
  Push conflicts retry up to three times with fresh checkouts. Persistent
  failures retain the pending report and retry on the next 60-second tick.
- An existing identical report with the same timestamp confirms a previously
  successful uncertain push; reuse its exact remote filename and ID. Different
  contents at that timestamp are never overwritten.
- Query failure publishes the fixed failure-format report (exception type only),
  with unknown counts. This is a delivered failure notification, not a successful
  query. The next normal query is the next daily slot or an explicit manual run.
- `run.lock` serializes publications; `scheduler.lock` prevents duplicate
  schedulers sharing state. Health fails on a stale heartbeat or publish error.
- Credentials remain externally managed. A failed publish cannot notify via
  GitHub; inspect service health/logs and `pending.json` until access is restored.

## Stop, rollback, and reinstall

For the same named Compose project and file:

- Pause: `stop notice`; resume: `start notice`.
- Uninstall the service: `down --remove-orphans`. This removes only this project's
  container/network and keeps bind-mounted state, priorities and credentials.
- Restore a previous version by restoring its stable skill copy/image, then
  `up -d --build`. Inspect health and next_run afterward.
- Reinstall: `up -d --build` using the preserved paths. Published Markdown files
  remain historical records; uninstall does not revert Git commits.
- Do not remove credentials, preferences or report history during rollback.
  Remove the dedicated image only after no service uses it.

Validate `up -> down -> up` in a distinct Compose project and state directory.
At each install verify running process, live query and scheduler next_run; after
`down`, verify the test container/network are gone. For the second install use
fresh test scheduler state to prove it does not depend on the first run.
