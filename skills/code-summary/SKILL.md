---
name: code-summary
description: >
  Summarize and document a codebase. Use when the user asks for code summary,
  repository overview, system architecture, component flow, framework
  detection, technical stack, code line counts, repository statistics, or a
  Markdown report explaining how a project is structured.
---

# Code Summary

Use this skill to produce concise, source-backed repository summaries and
architecture reports.

## When To Use

Use this skill when the user asks to:

- Summarize a repository or explain how a codebase is structured.
- Produce a system architecture or onboarding report.
- Detect frameworks, runtimes, package managers, entrypoints, or deployment
  tooling.
- Trace a command, request, route, job, or workflow through the code.
- Count files, lines, languages, or repository statistics.

Do not use this skill when:

- The user asks for implementation changes rather than a summary.
- The answer can be given from one file without repository-level analysis.
- The task is a code review; use review posture instead.

## Workflow

1. Discover project shape with `rg --files` first, falling back to `find` only
   when needed.
2. Identify manifests, build files, lockfiles, framework config, Docker files,
   CI config, app entrypoints, CLIs, routes, jobs, and service workers.
3. Detect the technical stack from source-backed files such as `package.json`,
   `pyproject.toml`, `requirements*.txt`, `go.mod`, `Cargo.toml`, `pom.xml`,
   `build.gradle`, `.csproj`, `Gemfile`, `composer.json`, Dockerfiles, and CI
   workflows.
4. Trace architecture from user-facing entrypoints to orchestration/core modules
   and then to persistence, external services, tools, or adapters.
5. Collect statistics with `tokei` or `cloc` when available; otherwise use a
   transparent `find`/`wc` fallback.
6. Produce a Mermaid diagram when the output is a report or the user asks for
   architecture.
7. Write a Markdown report when the user names an output path; otherwise answer
   in chat.

## References

- Use exact file references for important claims.
- Use Mermaid `flowchart TD` or `flowchart LR` by default.
- Quote Mermaid labels containing `/`, `:`, `?`, `[]`, or other sensitive
  characters, for example `API["/api/ws WebSocket"]`.

## Environment

- Exclude generated/vendor directories unless the user explicitly wants full
  repository totals. Common exclusions: `.git`, `node_modules`, `dist`,
  `build`, `.venv`, `venv`, `__pycache__`, `.next`, `coverage`, and `target`.
- State exclusions in the report.

## Rules

- Separate confirmed facts from inference. Use `Inference:` where behavior is
  implied but not directly stated.
- Avoid overclaiming framework or architecture details without source evidence.
- Include frontend, backend, data/storage, infra/devops, test tooling, and
  lint/format tooling when present.
- Make Mermaid diagrams renderable.
- If the repository is huge, sample intelligently and explain what was
  excluded.

## Output

Final reports should usually include:

- `Overview`
- `Architecture Diagram`
- `Request / Command Flow`
- `Technical Stack`
- `Repository Statistics`
- `Key Components`
- `Open Questions / Risks`
