# Design Workflow Reference

## Resolve The Skill Directory

Set the task-specific variable to the directory containing this skill's
`SKILL.md`:

```bash
UI_UX_SKILL_DIR="<directory-containing-this-SKILL.md>"
```

Prefix Python commands with `PYTHONDONTWRITEBYTECODE=1` so searches do not
leave generated cache files in the maintained skill package.

## Generate A Design System

Use this for a new application, page family, landing page, dashboard, or major
visual redesign:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 "$UI_UX_SKILL_DIR/references/scripts/search.py" \
  "<product-type> <industry> <audience> <style-keywords>" \
  --design-system --project-name "<project-name>" --format markdown
```

The output combines product, style, color, landing-page, typography, and
reasoning data. Reconcile it with the existing brand and product constraints.

## Search A Domain

```bash
PYTHONDONTWRITEBYTECODE=1 python3 "$UI_UX_SKILL_DIR/references/scripts/search.py" \
  "<specific-query>" --domain <domain> --max-results 3
```

| Domain | Use it for |
| --- | --- |
| `product` | Product-type patterns and overall direction |
| `style` | Visual styles, effects, compatibility, and complexity |
| `color` | Product-specific palettes and contrast-aware roles |
| `typography` | Font pairings, mood, and legibility |
| `landing` | Page sections, CTA placement, and conversion structure |
| `chart` | Data relationships, chart types, and accessible alternatives |
| `ux` | Accessibility, touch, navigation, animation, and feedback |
| `web` | Semantic HTML, forms, focus, ARIA, and performance |
| `react` | React and Next.js performance patterns |
| `icons` | Icon semantics and consistent library usage |
| `prompt` | Implementation keywords and style prompts |

Omit `--domain` only when automatic domain detection is acceptable. Prefer an
explicit domain for deterministic work.

## Search A Stack

```bash
PYTHONDONTWRITEBYTECODE=1 python3 "$UI_UX_SKILL_DIR/references/scripts/search.py" \
  "<implementation-concern>" --stack <stack> --max-results 3
```

Available stacks are `html-tailwind`, `react`, `nextjs`, `vue`, `nuxtjs`,
`nuxt-ui`, `svelte`, `swiftui`, `react-native`, `flutter`, and `shadcn`.
Use the repository's actual stack; use `html-tailwind` only for a new generic
web prototype without a declared framework.

## Synthesis Rules

1. Start from user tasks and information hierarchy, not decoration.
2. Map recommendations to existing tokens and components.
3. Define responsive behavior and empty, loading, error, disabled, and success
   states before polishing motion.
4. Match chart type to the relationship in the data. Provide a table or text
   alternative when a chart is not independently accessible.
5. Prefer familiar interaction patterns and visible labels over hidden or
   icon-only controls.
6. When search results conflict, prioritize accessibility, platform
   conventions, repository rules, and measured usability.

## Delivery Checklist

- Semantic structure and heading order are meaningful.
- Keyboard order follows the visual and task order.
- Interactive elements have visible focus and adequate target size.
- Text and essential controls meet applicable contrast requirements.
- Color is not the only state indicator.
- Images have appropriate alternative text; decorative images are ignored by
  assistive technology.
- Forms have persistent labels and actionable validation messages.
- Motion respects `prefers-reduced-motion` or platform equivalents.
- Loading, empty, error, disabled, and success states are handled.
- Layout works at representative phone, tablet, laptop, and wide-screen sizes.
- Content is not hidden behind fixed elements and does not overflow
  horizontally.
- Hover, focus, and active states do not cause layout shift.
- Icons come from a consistent family and have accessible names when needed.
- The rendered interface is inspected in both supported color schemes.
