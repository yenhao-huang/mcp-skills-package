---
name: design-system
description: >
  Define and enforce frontend design-system mechanics including tokens,
  typography, data presentation, loading stability, color semantics, and
  motion. Use when building or reviewing UI components, pages, dashboards,
  admin tools, or reusable design systems.
---

# Design System

Use this skill to turn an established visual direction into stable,
maintainable frontend rules. It governs implementation mechanics; it does not
choose a product's brand or aesthetic direction by itself.

## Workflow

1. Read `STATE.md`. Reset it from `references/template/STATE.template.md` for a
   new run, then mark the active step `in_progress`.
2. Read `references/rules/env.md` before assuming a framework, package manager,
   browser target, font source, or component library.
3. Inspect the existing UI, tokens, components, accessibility constraints, and
   loading behavior before proposing changes.
4. Read `references/design-system-rules.md` and define the smallest coherent
   token, typography, surface, semantic-color, data, and motion contracts.
5. If the UI includes meaningful navigation, list changes, reveals, or shared
   elements, also read `references/motion-choreography.md`.
6. Implement within the target project's conventions. Prefer additions and
   migrations over breaking token or component changes.
7. Validate responsive behavior, keyboard access, contrast, reduced motion,
   loading states, and layout stability in proportion to the change.
8. Record concrete validation evidence in `STATE.md` before handoff.

## Rules

- Use semantic tokens; do not scatter raw colors, spacing, radii, or timings.
- Keep persistent chrome stable while data, errors, and loading states change.
- Use tabular numerals for metrics, identifiers, timestamps, and aligned data.
- Motion must communicate state or spatial relationships and honor
  `prefers-reduced-motion`.
- Treat upstream examples as guidance, not as permission to override the local
  product, accessibility, performance, or dependency constraints.
- Do not add packages, hosted fonts, or external services without confirming
  the target project's environment rules and user authority.

## Provenance

This maintained adaptation is derived from
`connerkward/ckw-design-skill/design-system` through the
`sickn33/agentic-awesome-skills` catalog. See `references/provenance.md` and
`references/LICENSE.txt`.
