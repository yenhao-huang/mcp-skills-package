# Design System Rules

These rules adapt the upstream `design-system` guidance for maintained use.
Apply them after understanding the target product's audience, visual direction,
framework, and existing component conventions.

## Token architecture

Define a small semantic vocabulary before styling components:

- Foreground: primary, secondary, muted, inverse, disabled.
- Background: base, raised, inset, overlay.
- Border: subtle, default, emphasis, focus.
- Brand: primary action and product identity.
- Semantic: success, warning, destructive, information.
- Space: one documented rhythm, preferably derived from a small base unit.
- Shape: a limited radius and elevation scale.
- Motion: named durations and easings tied to interaction types.

Components consume semantic tokens instead of arbitrary literals. If a token
changes meaning across themes, keep its semantic name stable and change only
its value. Add new tokens when a genuinely new meaning appears; do not create a
token for each isolated component.

## Typography and data

- Make hierarchy visible through size, weight, spacing, and line height.
- Keep body copy readable at the target viewport and language.
- Reserve monospace and `font-variant-numeric: tabular-nums` for values that
  benefit from alignment: metrics, identifiers, timestamps, and code.
- Right-align comparable numeric table columns and keep units explicit.
- Use consistent precision and missing-value notation across dashboards.
- Do not rely on font weight or color alone to communicate status.

Self-host fonts when the product permits it. Prioritize only the faces and
weights used above the fold, reserve layout space, and avoid visible reflow.
Never hide essential text indefinitely while waiting for a font; any visibility
gate needs a short safety timeout and a readable fallback.

## Loading and layout stability

Every asynchronous region defines four deliberate states:

1. Initial or loading.
2. Populated.
3. Empty.
4. Error or unavailable.

Skeletons should trace the final layout rather than use generic spinners.
Reserve media dimensions with `aspect-ratio`, width/height, or a fixed container
so late content does not shift the page. Below-the-fold media may load lazily;
critical content must not compete with non-critical preloads.

Persistent chrome—navigation, toolbars, filters, status bars—must not change
height when copy or data changes. Constrain transient status text to its
reserved region and use truncation with an accessible full-value mechanism
when necessary.

## Color semantics and contrast

- Gray establishes hierarchy; chroma communicates action, status, selection,
  and identity.
- Keep one meaning per semantic color across charts, badges, alerts, and rows.
- Never use color as the only signal. Pair it with text, iconography, pattern,
  or position.
- Interactive states gain prominence through contrast, outline, or shape; they
  must not look disabled on hover or focus.
- Design with perceptual contrast in mind and verify the project's required
  WCAG threshold as the compliance gate.
- Check every semantic pairing in light, dark, high-contrast, selected,
  disabled, hover, focus, warning, and destructive states where applicable.

## Surfaces, borders, and nested shape

Use elevation sparingly. A border or spacing change is often clearer and less
expensive than another shadow. Nested rounded elements should look concentric:
the child radius cannot exceed the parent radius and should account for the gap
between them.

Do not add gradients, noise, blur, or glass effects by habit. Each effect needs
a product-specific reason and must preserve contrast, performance, and state
legibility.

## Responsive composition

- Start from information priority, not a desktop grid that is merely stacked.
- Keep primary actions and current status visible at narrow widths.
- Tables need an explicit small-screen policy: horizontal containment,
  prioritized columns, row details, or a purpose-built card view.
- Define breakpoints around content failure, not device brand names.
- Preserve focus order and reading order when layout regions move.
- Test dense, empty, long-label, translated, error, and loading cases.

For layout-heavy work, pair this skill with a spatial-composition or UX-review
skill if one is available. Do not assume an optional companion skill exists.

## Motion

The default is no animation. Add motion only when it communicates continuity,
spatial relationship, cause and effect, data arrival, or a deliberate moment of
delight. Animate compositor-friendly properties such as `transform` and
`opacity`; avoid `transition: all` and layout-property animation.

Use `references/motion-choreography.md` when more than a single local
micro-interaction is involved.

## Delivery checklist

- [ ] Tokens cover every introduced color, space, shape, type, and timing.
- [ ] Components expose stable variants instead of page-specific exceptions.
- [ ] Loading, empty, error, and populated states preserve layout.
- [ ] Metrics use consistent units, precision, alignment, and missing values.
- [ ] Keyboard navigation and visible focus work in visual order.
- [ ] Contrast and non-color status cues pass the project gate.
- [ ] Motion communicates a change and respects reduced-motion preferences.
- [ ] Narrow, medium, and wide layouts have been exercised.
- [ ] No new dependency or remote asset was introduced without approval.
