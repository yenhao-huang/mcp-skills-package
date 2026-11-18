# Design

## Context
See proposal.md for motivation. The upstream skill is embedded in a Python CLI package, while this repository distributes skill directories to Codex and Claude. This repository requires state, layout and environment references.

## Goals / Non-Goals
Preserve the upstream explanation-design guidance, audience/domain profiles, templates, helpers and visual references with a fixed source revision. The integration does not install the CLI, Manim, providers or personal agent configuration.

## Decisions
- Keep the upstream `manim` skill name in `content-producer`; existing directory discovery already supports it, avoiding installer changes.
- Add a concise local entry point and retain upstream guidance in references/guide.md. A CLI-only wrapper would omit the directly usable agent instructions.
- Move scripts into references/scripts and templates into references/template; rewrite local links and examples to match. Store reference stills in assets, with the demo as a copyable template.
- Preserve MIT attribution and record the source commit and adaptation details in references/SOURCE.md.
- Require runtime preflight and real video inspection before claiming successful rendering. Syntax and packaging checks establish only package integrity.

## Risks / Trade-offs
- Optional upstream narration examples depend on the separately installed CLI and external providers → document the boundary and avoid automatic installation or credentials.
- Manim and FFmpeg are unavailable on the packaging host → validate syntax, references, helper argument handling and isolated installation; explicitly report rendering as untested.
- Upstream examples may depend on Manim versions → preserve provenance so later updates can be reviewed.

## Migration Plan
The normal package installer discovers the new directory. Test installation, removal of only the installed skill, and reinstallation in a disposable fixture. Removing the new directory and catalog row rolls back this addition; no runtime configuration changes are required.
