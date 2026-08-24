# Hermes Langfuse Integration

Apply this reference only after Langfuse is running and the target Langfuse
project has valid API keys.

## Select The Hermes Runtime

- Native CLI: Hermes runs directly on the host.
- Docker: Hermes runs through its own Compose services.
- Windows installer: Hermes commonly uses an isolated `uv` virtual
  environment that cannot see system Python packages.

Record the runtime before changing packages, environment files, URLs, or
services.

## Install And Enable The Plugin

Prefer Hermes' supported installer so the Langfuse SDK enters Hermes' actual
environment:

```text
hermes tools
```

Select Langfuse Observability, then enable and inspect the plugin:

```bash
hermes plugins enable observability/langfuse
hermes plugins list
```

For a Windows installer where automation is necessary, locate the environment
that contains Hermes' `pyvenv.cfg`, then target its interpreter explicitly:

```cmd
dir "%LOCALAPPDATA%\hermes" /s /b | findstr /i "pyvenv.cfg"
uv pip install --python "<venv-root>\Scripts\python.exe" langfuse
"<venv-root>\Scripts\python.exe" -c "from langfuse import Langfuse; print('ok')"
```

Do not use system `pip install langfuse` as proof for an isolated Hermes venv.
An enabled plugin only proves the configuration switch is on; it does not prove
the SDK import succeeded.

## Configure Hermes

Write the variables to Hermes' own environment file:

- macOS/Linux: `~/.hermes/.env`
- Windows: `%USERPROFILE%\.hermes\.env`

Do not place them at `~/.env`, `%USERPROFILE%\.env`, or `%APPDATA%`.

```dotenv
HERMES_LANGFUSE_PUBLIC_KEY=<pk-lf-value>
HERMES_LANGFUSE_SECRET_KEY=<sk-lf-value>
HERMES_LANGFUSE_BASE_URL=http://127.0.0.1:3000
HERMES_LANGFUSE_ENV=local
```

The public and secret keys must match the selected Langfuse project and use
the expected `pk-lf-` and `sk-lf-` prefixes. Omitting the base URL sends to the
Langfuse cloud default instead of the local deployment.

Optional variables include `HERMES_LANGFUSE_RELEASE`,
`HERMES_LANGFUSE_SAMPLE_RATE`, `HERMES_LANGFUSE_MAX_CHARS`, and
`HERMES_LANGFUSE_DEBUG`. Preserve existing values unless the user requests a
change.

## Select The Base URL

- Native Hermes on the same host: `http://127.0.0.1:3000`.
- Hermes container using host networking: `http://127.0.0.1:3000`.
- Docker Desktop bridge networking on Windows: validate access from inside the
  container and use `http://host.docker.internal:3000` when loopback points to
  the container itself.

Do not join unrelated Compose projects to a shared network unless inspection
shows that topology is required.

## Apply And Validate

A native one-shot command reads configuration in a new process and normally
needs no separate restart:

```bash
hermes plugins list
hermes chat -q "hello"
```

For a long-running native daemon, restart only that daemon. For Docker Hermes,
restart the exact runtime service after confirming its Compose file and mount:

```bash
docker compose restart gateway
```

Then open the Langfuse project and verify that a new Hermes turn trace arrived.
If no trace appears, check in this order:

1. the plugin is enabled;
2. the SDK imports from Hermes' actual interpreter;
3. the `.env` path is the one Hermes reads;
4. key prefixes, key/project match, and local base URL are correct;
5. Hermes logs for placeholder credentials or client initialization errors.

The plugin can fail open when the SDK import is unavailable, so the absence of
an error message does not prove successful initialization.

## Disable Or Roll Back Hermes Integration

Disable the same plugin that was enabled:

```bash
hermes plugins disable observability/langfuse
```

Restore the pre-change Hermes `.env` exactly, or remove only the
`HERMES_LANGFUSE_*` entries added during this run. Do not delete unrelated
Hermes configuration. Remove the SDK from Hermes' environment only if it was
installed solely for this integration and the user explicitly requests
package removal.
