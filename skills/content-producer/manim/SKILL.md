---
name: manim
description: Create Manim mathematical animations, equation derivations, research-paper explainer videos and 3D visualizations. Use for requests such as 3Blue1Brown-style animation, animate this equation, or explain this paper visually. Includes scene planning, audience/domain guidance, templates, rendering and visual review.
---

# Manim explainer videos

Adapted from [AmitSubhash/3brown1blue](https://github.com/AmitSubhash/3brown1blue).
See [source and license](references/SOURCE.md). Use Manim Community Edition by
default; choose ManimGL only when the task needs it. This skill can be used
directly by an agent without installing the upstream CLI.

Resolve all bundled paths from this `SKILL.md` directory, including when installed
as a flat `manim/` directory. Copy templates and helpers into the user's chosen
project before editing; run render commands from that project, not the skill.

## Workflow

1. **Read context and initialize state.** Read [STATE.md](STATE.md),
   [state rules](references/rules/state-rules.md),
   [layout](references/rules/filetree.md) and
   [environment](references/rules/env.md). For a new run, reset state from the
   [template](references/template/STATE.template.md). Record the requested topic,
   equation or paper, target audience, duration, output directory and constraints.
   Read the supplied paper before explaining it; distinguish its results from
   illustrative examples. Ask only for inputs that materially block the work.
2. **Check the environment.** Follow the environment preflight, recording the
   interpreter, Manim version and required tools. If rendering is unavailable,
   report the missing dependency and prepare source/plans where possible; mark
   rendering blocked. Do not treat syntax checks as a successful render.
3. **Plan the explanation.** Read
   [explanation design](references/rules/explanation-design.md) and
   [pedagogy](references/rules/pedagogy-checklist.md). Choose relevant
   [audience and domain profiles](references/profiles.md). For multi-scene videos,
   use [scene planning](references/rules/scene-planning.md) and write a numbered
   scene plan with each scene's question, visual change, narration and duration.
   Verify the planned claims and equations against the source before coding.
4. **Author the scenes.** Read the gotchas and select technical references from
   the [Manim guide](references/guide.md). Copy
   [style.py](references/template/style.py) beside the scene files; adapt the
   [equation](references/template/equation_explainer.py) or
   [paper](references/template/paper_explainer.py) starter when relevant.
   [safe_manim.py](references/scripts/safe_manim.py) supplies optional wrappers.
   Use [production-quality checks](references/rules/production-quality.md) and
   compile the source with the project interpreter before rendering.
5. **Render and inspect.** Render a low-quality preview using
   `manim -ql scene.py SceneName`, or copy and invoke
   [render_scene.sh](references/scripts/render_scene.sh) with
   `bash render_scene.sh scene.py SceneName l`. Inspect the actual video for
   correctness, clipping, readable equations, timing and transitions. Fix issues
   before rendering final quality. For multi-scene work, name files in intended
   order and use [concat_scenes.sh](references/scripts/concat_scenes.sh) if needed.
   It overwrites `final_<quality>.mp4`; use a fresh output directory or preserve
   existing results first. Its concat list does not support apostrophes in paths.
6. **Audit and deliver.** With FFmpeg available, use
   [audit_video.sh](references/scripts/audit_video.sh) to extract review frames:
   `bash audit_video.sh /path/to/project 1080p60` (use the rendered quality).
   Confirm frame files exist and inspect them; the helper's exit status does not
   prove visual quality or successful extraction. Check the final video and any
   narration sync. Update state with source/video paths, commands, findings and
   remaining limitations. Deliver the artifacts and an accurate validation summary.

## Reference selection

- [Manim guide](references/guide.md): core API, equations, animation, 3D,
  rendering, design patterns and troubleshooting. Read relevant sections only.
- [Audience and domain profiles](references/profiles.md): tune technical depth
  and examples to the intended viewer.
- [Designing Math visuals](references/designing-math.md): three bundled example
  stills and a copyable demo.
- [Voiceover](references/rules/voiceover.md) and
  [Remotion integration](references/rules/remotion-integration.md): optional
  extensions. Check their dependencies separately; the upstream CLI, speech
  providers, credentials and Remotion are not bundled in this skill.

The entry workflow and environment rules govern setup. Installation commands in
upstream tutorials are reference examples, not automatic setup instructions.
