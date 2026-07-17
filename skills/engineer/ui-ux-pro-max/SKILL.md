---
name: ui-ux-pro-max
description: Design and review accessible, responsive web or mobile interfaces with a searchable UI/UX knowledge base. Use for page or component design, dashboard and landing-page UX, visual direction, color and typography selection, design-system recommendations, chart selection, frontend stack guidance, or UI quality reviews.
---

# UI/UX Pro Max

Use the bundled offline search tools and data to turn product context into a
coherent design direction, then validate the implemented interface. Treat
search output as recommendations, not as a substitute for inspecting the
existing product, codebase, or accessibility requirements.

## Workflow

1. Identify the product type, users, primary task, target surface, visual
   direction, implementation stack, and constraints. Preserve an existing
   design system unless the user asks to replace it.
2. Read `references/design-workflow.md` for domain selection, command syntax,
   and the delivery checklist.
3. For a new product or visual direction, generate a design-system proposal
   before implementation. For a focused review or small change, search only
   the relevant domains and existing stack.
4. Run targeted searches for accessibility, interaction, layout, charts, or
   implementation guidance when they affect the task.
5. Synthesize the results with repository conventions. Do not copy conflicting
   recommendations blindly.
6. Implement or review the interface, then verify responsive behavior,
   keyboard navigation, focus visibility, contrast, motion preferences,
   loading and error states, and absence of horizontal overflow.

## Search Tool

Resolve `UI_UX_SKILL_DIR` to the directory containing this `SKILL.md` before
running commands. The tools use only Python's standard library and bundled CSV
data.

```bash
UI_UX_SKILL_DIR="<directory-containing-this-SKILL.md>"
PYTHONDONTWRITEBYTECODE=1 python3 "$UI_UX_SKILL_DIR/references/scripts/search.py" \
  "SaaS model evaluation dashboard" --design-system --format markdown
```

Supplement a proposal with a domain or stack search:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 "$UI_UX_SKILL_DIR/references/scripts/search.py" \
  "accessible benchmark comparison chart" --domain chart

PYTHONDONTWRITEBYTECODE=1 python3 "$UI_UX_SKILL_DIR/references/scripts/search.py" \
  "responsive data table loading error states" --stack react
```

## Guardrails

- Accessibility and interaction correctness outrank visual novelty.
- Verify claims against the current code and rendered result.
- Do not install packages merely to run the bundled search tool.
- Do not fetch fonts, icons, or other assets without considering repository
  policy, licensing, privacy, and offline requirements.
- Use one consistent icon family; do not use emoji as interface icons.
- Never rely on color alone to communicate state.
- Prefer project-native components, tokens, and patterns over introducing a
  parallel design system.

For provenance, imported revisions, and licensing, read
`references/provenance.md` when maintaining or redistributing this skill.
