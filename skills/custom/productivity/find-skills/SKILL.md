---
name: find-skills
description: Discover and recommend installable agent skills from managed skill libraries. Use when a user asks to find, compare, or install a skill, asks whether a skill exists for a task, or wants to extend agent capabilities with a reusable workflow.
---

# Find Skills

Search managed skill registries before recommending installable skills.

## Workflow

1. Define the user's task, target agent/host, environment, and constraints.
2. Read `references/skill-registry.md` and search every enabled registry in
   priority order. Do not start with an unregistered ecosystem search.
3. Expand the query with task nouns, verbs, platform names, and close synonyms.
4. Inspect each plausible candidate using
   `references/rules/candidate-review.md`; catalog text alone is insufficient.
5. Rank only candidates that fit the task and clearly report provenance,
   host compatibility, risk, license, install method, and caveats.
6. If managed registries have no suitable result or are unavailable, follow
   the documented fallback and label fallback results as such.
7. Install only after explicit user approval. Preview the exact, pinned install
   first when the source supports a dry run.

## State

For a new discovery run, reset `STATE.md` from
`references/template/STATE.template.md`, then follow
`references/rules/state-rules.md`.

## Rules

- Never recommend from a title or search snippet alone.
- Treat catalog risk and quality metadata as evidence, not a trust guarantee.
- Do not infer a third-party skill's license from an aggregator repository.
- Do not invent install counts, compatibility, provenance, or maintenance
  signals that the source does not publish.
- Keep recommendations small and explain why each candidate fits.
- Do not install, update, or execute discovered content without user approval.

## Output

Return the query scope, registries searched, recommended skill IDs and links,
fit rationale, provenance, host support, risk/license findings, a pinned preview
or install command when available, and any fallback or unresolved caveat.
