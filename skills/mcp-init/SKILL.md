---
name: mcp-init
description: >
  Initialize or repair OpenAI Codex MCP configuration for Jina MCP, Firecrawl
  MCP, Hugging Face MCP, and Git MCP. Use when the user asks to set up MCP
  servers, add Jina/Firecrawl/Hugging Face/Git MCP to Codex, bootstrap
  `~/.codex/config.toml`, refresh MCP server blocks, or create a repeatable
  local MCP initialization workflow.
---

# MCP Init

Use this skill to configure Codex MCP servers in
`${CODEX_HOME:-$HOME/.codex}/config.toml`.

## When To Use

Use this skill when the user asks to:

- Set up, initialize, or repair Codex MCP configuration.
- Add or refresh Jina, Firecrawl, Hugging Face, or Git MCP server blocks.
- Bootstrap `~/.codex/config.toml`.
- Bind Git MCP to a specific repository.
- Validate MCP config syntax or configured server names.

Do not use this skill when:

- The user is asking about MCP concepts only and no local config change is
  needed.
- The request targets a non-Codex MCP client unless the user explicitly wants
  compatible config guidance.
- The user wants secrets hardcoded; discourage this unless explicitly required.

## Workflow

1. Resolve the target config path; default to
   `${CODEX_HOME:-$HOME/.codex}/config.toml`.
2. Check whether `npx` is available for Firecrawl and `uvx` is available for Git.
3. Use `scripts/init_mcp_config.py` to merge or replace managed MCP blocks. The
   script creates a timestamped `.bak` before writing.
4. Ask for API keys only if the user wants connectivity validation. For config
   creation, use env var names without seeing secret values.
5. Verify the config parses as TOML.
6. Report the configured MCP server names and any missing runtime or env var.

## References

- Use `scripts/init_mcp_config.py` as the canonical deterministic tool.
- Useful command:
  `python /home/howard/.codex/skills/mcp-init/scripts/init_mcp_config.py`
- Use `--config <path>` for a non-default config.
- Use `--git-repository <repo>` to bind Git MCP to a repository.
- Use `--dry-run` to print the merged config without writing.

## Environment

- `jina`: remote MCP at `https://mcp.jina.ai/v1`, authenticated by
  `JINA_API_KEY` through `bearer_token_env_var`.
- `firecrawl`: local stdio server launched with `npx -y firecrawl-mcp`, reading
  `FIRECRAWL_API_KEY` from the Codex process environment.
- `huggingface`: remote MCP at `https://huggingface.co/mcp`, authenticated by
  `HF_TOKEN` through `bearer_token_env_var`.
- `git`: local stdio server launched with `uvx mcp-server-git`, optionally with
  `--repository`.

## Rules

- Never hardcode API keys unless the user explicitly asks.
- Prefer environment variables and tell the user which variables to export
  before starting Codex.
- Do not hide missing `npx` or `uvx` behind fallback installs; report the exact
  missing runtime.
- Prefer binding Git MCP to the current project when the user wants a narrow
  repository scope.

## Output

Final responses should include:

- Config path changed or inspected.
- Backup path when a write occurred.
- Server names configured.
- Validation command and result.
- Missing runtimes or environment variables, if any.
