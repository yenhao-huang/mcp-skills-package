---
name: frontend-slides
description: Create or revise self-contained HTML slide decks and export PDFs using the bundled frontend-slides design references. Use for presentations, slide styling, PowerPoint conversion, and HTML-to-PDF delivery; preserve the calling workflow's content and publication contract.
license: MIT
---

# Frontend slides

Shared presentation skill for content production. Read
[provenance](references/SOURCE.md) and the [upstream guide](references/guide.md).
The upstream material is pinned; no network fetch is needed to read it.
Paths and command examples in that guide are relative to references/; from
the skill root use references/scripts/ for its optional executable helpers.

## Workflow

1. Read the source content, caller's output contract and existing approved deck.
   Read [environment rules](references/rules/env.md). For a new design, establish
   audience, density and visual direction using the guide. Reuse an approved
   design without repeating questions already answered by the caller.
2. Read [HTML architecture](references/html-template.md),
   [viewport CSS](references/viewport-base.css) and relevant
   [animation patterns](references/animation-patterns.md). Choose and read only
   the needed style references. If prose needs editing, apply `$humanizer`
   before rendering and recheck every factual claim against the source.
3. Generate or edit the single-file HTML at a fixed 1920×1080 stage. Preserve
   source links, metadata, factual uncertainty and required section/page order.
   Embed the final content's font glyphs, retain licenses, and keep runtime
   assets self-contained when the caller requires offline output.
4. Render in the existing browser toolchain. Check desktop and phone bounds,
   panel overlap, navigation and reduced motion. Export requested PDFs with a
   Chromium PDF API after fonts load; preserve selectable text and source links.
   Use one slide per page, print backgrounds, and reveal all slides for print.
   Inspect the PDF, page count, extracted text and links before delivery.
5. Record source revision, artifact paths and actual validation in STATE.md,
   following [state rules](references/rules/state-rules.md). Deliver HTML/PDF
   as requested. Publishing or hosting needs authorization from the user or
   calling workflow; a request to make slides alone does not authorize deployment.

## Caller contracts and optional helpers

The caller's language, headings, exact output filenames, page count, evidence
rules and publication limits override generic design/export suggestions. For
ExecuTorch PM this includes its two-page topic contract and no community writes.
Avoid rendering workflow notes or template names as slide content.

The upstream guide contains optional scripts in references/scripts/. They may
install packages, download browsers or deploy externally; do not automatically
run them as part of reading the skill. Prefer the existing environment and the
PDF API above. The upstream screenshot exporter cannot satisfy a requirement
for selectable PDF text. This skill does not install a service or alter schedules.

In categorized package installs, `$humanizer` is the sibling
[humanizer skill](../humanizer/SKILL.md). In flat installs, resolve it by name
beside this skill; install both skill folders when prose editing is requested.
