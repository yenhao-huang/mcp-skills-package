# Validation evidence

Date: 2026-11-18. Branch: agent/fix-126. Related issue: #126.

## Source review

Imported all 51 upstream skill resources from commit
`fd9bf9c69ac33519acc00dc7faa21bd14b241e54`, plus its MIT license. Reviewed every
textual adaptation against that checkout; changes are limited to the guide,
relative resource paths and the demo's adjacent style import. All four helpers,
three image assets and the license match upstream bytes. Source provenance and
adaptations are recorded in the skill's references/SOURCE.md.

## Checks performed

- Generic skill validator: `python quick_validate.py skills/content-producer/manim`
  passed. Used the system skill-creator validator with PyYAML 6.0.3 in a disposable
  virtual environment; system Python was not modified.
- Required layout, unique `name: manim`, workflow heading and catalog path passed.
  The skill contains 60 files, including 27 upstream rules plus 3 package rules,
  4 audience profiles and 7 domain profiles.
- Resolved all 82 local Markdown links and verified they stay inside the skill.
  Repeated this check for categorized Codex/Claude installs and a flat `manim/`
  copy. All targets exist.
- Parsed all five Python files with `ast.parse` and checked all three shell
  helpers with `bash -n`: passed.
- Exercised missing-project, missing-media and invalid-quality failures for
  audit/concatenation, plus missing render arguments: all 7 cases failed with
  expected messages. A stub Manim executable verified quoted filename forwarding,
  quality/scene arguments and propagation of a nonzero renderer exit code.
  This stub test does not validate rendering.
- Ran the existing `init.sh` unchanged in a temporary fixture containing this
  skill and empty hooks/utils, then removed only its installed directories,
  reinstalled and repeated installation. Both Codex and Claude copies matched
  every source file; unrelated sentinel files survived. No personal installation
  was changed. This verifies the new payload, not every existing package skill.
- `openspec validate add-manim-skill --strict`: passed.
- `git diff --check` and staged diff checks: passed.

## Limitations

Manim, FFmpeg, ffprobe, LaTeX and dvisvgm are absent on this host. Actual video
rendering, LaTeX output, media concatenation, frame extraction, narration and visual
quality were not tested. Optional upstream CLI and provider integration were not
installed or tested. The skill requires these checks in the target runtime before
an agent claims delivery of a validated video.

## Changed files and handoff

- `skills/content-producer/manim/`: attributed resources and package workflow.
- `README.md`: skill catalog row.
- `openspec/config.yaml` and this change directory: required plan and evidence.

The requested handoff is an open PR; review, merge and subsequent archive are
pending and are not part of the validation results above.
