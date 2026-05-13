---
name: mcp-init
description: Initialize or repair OpenAI Codex MCP configuration for Jina MCP, Firecrawl MCP, Hugging Face MCP, and Git MCP. Use when the user asks to set up MCP servers, add Jina/Firecrawl/Hugging Face/Git MCP to Codex, bootstrap ~/.codex/config.toml, refresh MCP server blocks, or create a repeatable local MCP initialization workflow.
---

# MCP Init

## Overview

Use this skill to configure `~/.codex/config.toml` with four MCP servers:

- `jina`: remote Jina MCP at `https://mcp.jina.ai/v1`, authenticated with `JINA_API_KEY` through `bearer_token_env_var`.
- `firecrawl`: local stdio server launched with `npx -y firecrawl-mcp`, expecting `FIRECRAWL_API_KEY` in the Codex process environment.
- `huggingface`: remote Hugging Face MCP at `https://huggingface.co/mcp`, authenticated with `HF_TOKEN` through `bearer_token_env_var`.
- `git`: local stdio server launched with `uvx mcp-server-git`; optionally bind it to a specific repository with `--repository`.

Never hardcode API keys into config unless the user explicitly asks. Prefer environment variables and tell the user to export them before starting Codex.

## Workflow

1. Inspect the target Codex config path. Default to `${CODEX_HOME:-$HOME/.codex}/config.toml`.
2. Check whether `npx` is available for Firecrawl and `uvx` is available for Git. If missing, report the exact missing runtime and do not hide it with fallback installs.
3. Use `scripts/init_mcp_config.py` to merge or replace the managed MCP blocks. The script creates a timestamped `.bak` before modifying the config.
4. Ask for API keys only if the user wants you to validate connectivity. For configuration only, use `JINA_API_KEY`, `FIRECRAWL_API_KEY`, and `HF_TOKEN` variable names without seeing the secret values.
5. After editing, verify the config parses as TOML and show the server names that were configured.

## Script Usage

Run from any working directory:

```bash
python /home/howard/.codex/skills/mcp-init/scripts/init_mcp_config.py
```

Useful options:

```bash
python /home/howard/.codex/skills/mcp-init/scripts/init_mcp_config.py \
  --config /home/howard/.codex/config.toml \
  --git-repository /path/to/repo
```

Use `--dry-run` to print the merged config without writing:

```bash
python /home/howard/.codex/skills/mcp-init/scripts/init_mcp_config.py --dry-run
```

## Expected Config Blocks

The managed output should look like this:

```toml
[mcp_servers.jina]
url = "https://mcp.jina.ai/v1"
bearer_token_env_var = "JINA_API_KEY"
startup_timeout_sec = 120
tool_timeout_sec = 600

[mcp_servers.firecrawl]
command = "npx"
args = ["-y", "firecrawl-mcp"]
startup_timeout_sec = 120
tool_timeout_sec = 600

[mcp_servers.huggingface]
url = "https://huggingface.co/mcp"
bearer_token_env_var = "HF_TOKEN"
startup_timeout_sec = 120
tool_timeout_sec = 600

[mcp_servers.git]
command = "uvx"
args = ["mcp-server-git"]
startup_timeout_sec = 120
tool_timeout_sec = 600
```

When `--git-repository` is supplied, the Git args become:

```toml
args = ["mcp-server-git", "--repository", "/path/to/repo"]
```

## Notes

- Firecrawl's MCP server reads `FIRECRAWL_API_KEY` from its process environment. If Codex is launched from a shell, export the variable before starting Codex.
- Jina can use Codex's `bearer_token_env_var` support for remote HTTP MCP servers, so do not put the token in the URL or headers.
- Hugging Face can use Codex's `bearer_token_env_var` support for remote HTTP MCP servers. Export `HF_TOKEN` before starting Codex.
- Git MCP can mutate repositories. Prefer binding it to the current project with `--git-repository` when the user wants a narrow scope.
