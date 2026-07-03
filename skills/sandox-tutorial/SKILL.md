---
name: sandox-tutorial
description: >
  Tutorial notes for installing custom skills, setting up MCP configuration, and
  preparing repository `AGENTS.md` environment rules. Use when the user asks for
  the local sandbox/skill/MCP setup tutorial, custom skill installation steps,
  or the AGENTS.md environment setup rule.
---

# Sandox Tutorial

Use this skill as local setup guidance for custom skills, MCP configuration, and
repository agent instructions.

## When To Use

Use this skill when the user asks to:

- Install or move the local `custom_skills` repository into `~/.agents/skills`.
- Review the local skill and MCP setup tutorial.
- Prepare AGENTS.md rules for environment setup and generation workflows.
- Document expected vLLM, llama-server, or MCP setup steps.

Do not use this skill when:

- The user asks to create or edit a specific skill; use `skill-creator`.
- The user asks to initialize MCP config directly; use `mcp-init`.
- The user asks to create a Codex sandbox; use `codex-sandbox`.

## Workflow

1. Identify which setup area the user needs: skills, environment, MCP, or
   AGENTS.md rules.
2. Provide or update only the relevant setup steps.
3. Prefer local paths and commands already documented in this skill.
4. For environment mutation, defer to the `dev` skill's
   `references/convention.md` before installing packages or changing runtimes.
5. Validate changed documentation by checking the edited file or command syntax
   when applicable.

## References

- Custom skills installation:
  `git clone git@github.com:yenhao-huang/custom_skills.git`,
  `mkdir ~/.agents`, then move `custom_skills/skills` to `~/.agents/skills`.
- MCP config is edited in `~/.codex/config.toml`; prefer using `mcp-init` for
  actual config edits.
- Shell environment changes are typically made in `~/.bashrc`.

## Environment

- Expected skill root: `~/.agents/skills`.
- Environment setup may include vLLM and GPU-enabled `llama-server`.
- Repository AGENTS.md should require reading the Dev skill convention before
  package or environment changes.

## Rules

- Keep this skill as tutorial guidance, not a deterministic installer.
- Do not mutate global environment, package managers, or runtime paths unless
  the user explicitly asks and the relevant environment rules have been read.
- Keep setup instructions local to the repository or user-level agent config.
- For retriever question generation (`gen_ques` or LLM generation runs), use the
  repo-local Ralph loop rather than stopping after the first failed attempt:
  `python core/cli/ralph_loop.py --config configs/ralph/gen_ques_for_retriever.json`.

## Output

Final responses should include:

- Which setup area was explained or changed.
- Commands or file paths involved.
- Validation performed, if any.
- Any missing prerequisite or unresolved environment assumption.
