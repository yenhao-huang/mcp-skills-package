# Template Reference

Use reference files for details that are useful only after the skill triggers.
Keep each reference focused so Codex can load one file instead of the entire
skill knowledge base.

## Domain Rules

- Replace this with rules that must be followed for this skill's domain.
- Prefer concrete constraints over broad advice.
- Include exceptions only when they affect implementation or validation.

## File Map

| Area | Path | Notes |
| --- | --- | --- |
| Primary implementation | `path/to/file.py` | Replace with the main file or module. |
| Tests | `tests/path/test_file.py` | Replace with the focused validation target. |
| Config | `configs/example.yaml` | Replace with config touched by this skill. |

## Workflow Details

1. Replace this with domain-specific steps that are too long for `SKILL.md`.
2. Include commands only when they are stable and reusable.
3. Put fragile or deterministic logic into `scripts/` instead of prose.

## Validation Checklist

- Run the smallest relevant test or smoke command.
- Record the exact command and result in `STATE.md`.
- If validation cannot run, record the blocker and the best static check.
