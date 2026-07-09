---
name: skill-create
description: Create or update repository-local Codex skills under .codex/skills. Use when the user asks to create a skill, update a SKILL.md, change skill metadata, add skill references/rules/templates, validate skill behavior, or fix a skill's required layout.
---

# Create Skill

Use this skill to create and maintain repo-local Codex skills. In this
repository, a valid skill has a stricter layout than the generic system skill
initializer creates by default.

## Workflow

1. Read the user's request and identify the exact skill name, purpose, and
   target directory.
2. Read `STATE.md`; for a new run, reset it from
   `references/template/STATE.template.md`.
3. Read the required references:
   - `references/rules/categories.md` before choosing a target directory or
     moving an existing skill.
   - `references/rules/filetree.md` before adding, moving, or removing files in
     any skill directory.
   - `references/rules/env.md` before installing packages, starting services,
     choosing frameworks, or assuming runtime details.
   - `references/rules/state-rules.md` before changing any `STATE.md`.
4. Mark the current step `in_progress` in `STATE.md` before editing.
5. Create or update the skill under the category selected from
   `references/rules/categories.md`, using the local required layout from
   `references/rules/filetree.md`.
6. Validate with both checks:
   - Generic skill validation, when available:
     `/home/howard/.codex/skills/.system/skill-creator/scripts/quick_validate.py`
   - Local layout validation:
     `skills/Custom/Productivity/skill-create/scripts/validate_skill_layout.py <skill-dir>`
7. Mark the workflow step `completed`, `blocked`, or `skipped` in `STATE.md`
   with concrete evidence.

## Conflict Rule

If a generic system initializer or external template conflicts with
`references/rules/filetree.md`, the repo-local filetree rule wins. Do not stop
after generic validation passes; the local layout validator must also pass.

## Skill Layout Contract

Every newly created or substantially updated repo-local skill must include:

- `SKILL.md`
- `STATE.md`
- `agents/openai.yaml`
- `references/example.md`
- `references/rules/filetree.md`
- `references/rules/env.md`
- `references/rules/state-rules.md`
- `references/template/STATE.template.md`

Additional domain references are allowed under `references/`. Runnable helper
scripts belong in top-level `scripts/` only when deterministic execution is
part of the skill workflow.

## Reference Rules

- Keep `SKILL.md` focused on trigger conditions, core workflow, and short
  guardrails.
- Put detailed domain behavior in `references/`.
- Put reusable operating rules in `references/rules/`.
- Put state templates in `references/template/`.
- Keep skill directories under the approved category taxonomy.
- Load only the reference files needed for the current request.
- Do not add README, changelog, installation guide, or quick-reference files
  unless the user explicitly asks for user-facing documentation.

## Output

Final responses should include:

- What skill files changed.
- Which validation commands passed.
- Whether the target skill now satisfies the local required layout.
- Any blocker or remaining risk.
