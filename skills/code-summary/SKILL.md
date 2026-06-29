---
name: code-summary
description: Summarize and document a codebase. Use when the user asks for code summary, repository overview, system architecture, component flow, framework detection, technical stack, code line counts, repository statistics, or a Markdown report explaining how a project is structured.
---

# Code Summary

## Workflow

Produce a concise, source-backed codebase summary. Prefer editing or creating a
Markdown report when the user names an output path; otherwise answer in chat.

1. Discover project shape.
   - List top-level files and directories.
   - Identify package manifests, build files, lockfiles, framework config, Docker files, CI config, and app entrypoints.
   - Prefer `rg --files`; if unavailable, use `find`.

2. Detect frameworks and technical stack.
   - Inspect manifests such as `package.json`, `pyproject.toml`, `requirements*.txt`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle`, `.csproj`, `Gemfile`, `composer.json`, `Dockerfile`, and CI workflows.
   - Separate confirmed facts from inference. Cite the files that prove each framework or runtime.
   - Include frontend, backend, data/storage, infra/devops, test tooling, and lint/format tooling when present.

3. Trace the architecture.
   - Find user-facing entrypoints first: CLI commands, web routes, desktop entrypoints, message handlers, service workers, daemons, or scheduled jobs.
   - Follow the path from entrypoint to orchestration/core modules and then to external services, persistence, tools, or adapters.
   - Use exact file references for important claims. Include line spans when the task asks for a trace or when precision matters.

4. Draw architecture diagrams.
   - Use Mermaid by default.
   - Include at least one high-level `flowchart TD` or `flowchart LR`.
   - Quote labels that contain `/`, `:`, `?`, `[]`, or other Mermaid-sensitive characters, e.g. `API["/api/ws WebSocket"]`.
   - Show major components, data/control flow, and external boundaries.
   - If the user asks "when I do X, which components are involved", add a sequence-style or flow diagram for that specific path.

5. Collect statistics.
   - Report code line counts, file counts, and language breakdown.
   - Prefer `tokei` or `cloc` if installed.
   - If unavailable, use a transparent fallback such as:

```bash
find . -path './.git' -prune -o -path './node_modules' -prune -o -type f \
  | sed 's#^\./##' \
  | awk -F. 'NF>1 {ext=$NF; count[ext]++} END {for (e in count) print e, count[e]}'
```

```bash
find . -path './.git' -prune -o -path './node_modules' -prune -o -type f \
  \( -name '*.py' -o -name '*.ts' -o -name '*.tsx' -o -name '*.js' -o -name '*.jsx' -o -name '*.go' -o -name '*.rs' -o -name '*.java' \) \
  -print0 | xargs -0 wc -l
```

   - Exclude generated/vendor directories unless the user explicitly wants full repository totals. Common exclusions: `.git`, `node_modules`, `dist`, `build`, `.venv`, `venv`, `__pycache__`, `.next`, `coverage`, `target`.
   - State exclusions in the report.

6. Write the summary.
   - Recommended sections:
     - `# System Architecture` or `# Codebase Summary`
     - `## Overview`
     - `## Architecture Diagram`
     - `## Request / Command Flow`
     - `## Technical Stack`
     - `## Repository Statistics`
     - `## Key Components`
     - `## Open Questions / Risks`
   - Keep the report useful for engineers who need to onboard quickly.
   - Avoid overclaiming. Use `Inference:` where the code implies behavior but does not state it directly.

## Output Quality Bar

- Use source-backed claims for architecture and framework detection.
- Make the diagram renderable Mermaid; avoid unquoted labels with leading `/`.
- Distinguish frontend, backend, orchestration, persistence, external APIs, tools, and deployment.
- Include enough statistics to answer "how large is this codebase" without dumping raw command output.
- If a repository is huge, sample intelligently and explain what was excluded.
