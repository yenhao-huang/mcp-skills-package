---
name: skill-create
description: >
  Use this template when creating a new Codex skill. Replace this description
  with clear trigger conditions: what the skill does, when to use it, and any
  domain-specific keywords that should activate it.
---

# Create Skill

Use this file for the essential workflow only. Keep detailed schemas, long
examples, API notes, and domain references in `references/` so they are loaded
only when needed.

## When To Use

Use this skill when the user asks to:

- Replace this bullet with a concrete task this skill supports.
- Replace this bullet with another trigger phrase or workflow.
- Replace this bullet with domain-specific language that should activate the skill.

Do not use this skill when:

- The task is unrelated to the skill domain.
- A simpler built-in answer is enough.
- The user is asking only for general discussion and no specialized workflow is needed.

## Workflow

1. Read the user's request and identify the exact scope.
2. Read `STATE.md`; if this is a new run, reset it from
   `references/template/STATE.template.md`.
3. Load only the relevant files from `references/`.
4. Mark the current step `in_progress` in `STATE.md`.
5. Perform the work using the repository's existing conventions.
6. Validate the result with the smallest command that proves the change.
7. Mark the step `completed`, `blocked`, or `skipped` in `STATE.md` with evidence.

## References

- Read `references/example.md` when you need the example domain rules, file map,
  or validation checklist.
- Read `references/rules/env.md` before installing packages, starting services,
  choosing frameworks, or assuming a runtime language.
- Read `references/rules/filetree.md` before adding, moving, or removing files
  in a skill directory.
- Read `references/rules/state-rules.md` when the workflow uses `STATE.md`
  or needs explicit per-run progress tracking.
- Use `references/scripts/` for reference code that should be read or adapted,
  not executed as the skill's primary deterministic tooling.
- Add more reference files for large details instead of expanding this file.

## Environment

Follow `references/rules/env.md` for package management, service definitions,
framework choices, and programming language expectations. If the repository
does not define the required environment, tell the user what is missing before
making assumptions.

## Rules

### State Rules

Keep state rules small in `SKILL.md`. Use `STATE.md` as per-run working state,
reset it from `references/template/STATE.template.md` for new executions, and
read `references/rules/state-rules.md` for status values, hard guards, and
update rules.

Minimum contract:

- `STATE.md` is per-run working state.
- `references/template/STATE.template.md` is the reset source for new runs.
- Do not claim a step is complete unless `STATE.md` was updated with evidence.

### Reference Rules

- Keep `SKILL.md` focused on trigger conditions and core workflow.
- Follow `references/rules/env.md` before changing environment assumptions.
- Follow `references/rules/filetree.md` for the expected skill directory layout.
- Put detailed domain rules in `references/`.
- Put reusable rules in `references/rules/`.
- Put skill/state templates in `references/template/`.
- Put reference code examples in `references/scripts/`; use top-level
  `scripts/` only for deterministic tools the agent should run directly.
- Load only the reference files needed for the current request.

## Output

Final responses should include:

- What changed or what was investigated.
- Validation command and result.
- Any blocker or remaining risk.
