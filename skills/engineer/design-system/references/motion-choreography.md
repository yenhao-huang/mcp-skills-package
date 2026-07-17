# Motion Choreography

Use motion only when it communicates one of these ideas: spatial relationship,
continuity, cause and effect, data arrival, or deliberate delight. If the
message cannot be stated in one sentence, remove the animation.

## Priority

Implement only the transition types that apply, in this order of value:

1. Shared element: the same object persists across views.
2. Reveal: loading or placeholder content becomes real content.
3. List identity: existing items reorder or filter without losing identity.
4. State change: a panel, toast, row, or control enters or exits.
5. Route or section change: the user moves to a different place.

Background refresh and silent revalidation should not animate.

## Navigation semantics

| Navigation | Motion | Meaning |
| --- | --- | --- |
| Parent to child or list to detail | Directional slide | Encodes depth |
| Ordered previous/next | Directional slide | Encodes sequence |
| Sibling tabs or peer sections | Fade or cross-fade | Avoids false depth |
| Skeleton to content | Fade or short rise | Communicates arrival |
| Background refresh | None | Preserves continuity |

## Starting durations

| Interaction | Duration |
| --- | --- |
| Direct toggle | 100–200 ms |
| Route or section | 150–250 ms |
| Content reveal | 200–400 ms |
| Shared-element morph | 300–500 ms |

Entrances normally ease out, exits ease in, and positional moves ease in-out.
Adjust for distance, scale, and product tone, then validate with real content.

## Mechanics

- Animate `transform` and `opacity` where possible.
- Name transition properties explicitly; never use `transition: all`.
- Keep persistent navigation and toolbars outside route transition containers.
- Preserve element identity with stable keys and names.
- Never raster-scale text for a morph; cross-fade when typography changes.
- Reordering must retain keyboard focus and semantic reading order.
- Honor `prefers-reduced-motion` by removing travel, scale, blur, and long
  sequencing while preserving the final state.
- Interruption must settle cleanly. Rapid repeated navigation cannot leave
  stale overlays, disabled controls, or hidden content.

## Validation

Test keyboard navigation, back/forward navigation, rapid repeated actions,
slow data, reduced motion, narrow viewports, and screenshots during loading.
Motion is complete only when the interface remains understandable without it.

## Attribution

Adapted from the upstream `design-system` motion reference, which generalized
guidance from Vercel's Web Interface Guidelines and React View Transitions
material. Full provenance is recorded in `provenance.md`.
