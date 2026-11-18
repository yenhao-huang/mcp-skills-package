# Proposal

## Why

Issue #126 requests the 3brown1blue Manim skill in the content-producer category. The package currently provides slides and prose skills but lacks this source-backed explainer-video workflow.

## What Changes

- Add a discoverable `manim` skill adapted from AmitSubhash/3brown1blue.
- Bundle pinned upstream rules, audience/domain profiles, templates and helpers with attribution.
- Add required workflow state and environment/layout rules; expose paths that survive categorized and flat installs.
- Add catalog documentation and validation evidence without installing into personal agent directories.

## Capabilities

### New Capabilities

- `manim-content-production`: discover, plan, author and validate Manim explainer videos using packaged resources.

### Modified Capabilities

None.

## Impact

Adds `skills/content-producer/manim/` and a README catalog entry. No runtime service, scheduler, global package, or upstream repository is modified. Linked issue: https://github.com/yenhao-huang/mcp-skills-package/issues/126.
