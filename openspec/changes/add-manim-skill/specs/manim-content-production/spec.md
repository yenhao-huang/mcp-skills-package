## Purpose
Provide a discoverable Manim skill for creating explainer videos from topics, equations and research papers using portable bundled resources.

## ADDED Requirements

### Requirement: Discoverable content production skill
The package SHALL expose a uniquely named `manim` skill in the content-producer category with an ordered workflow and reusable state template.

#### Scenario: Install the package
- **WHEN** the existing package installer runs in a fresh project
- **THEN** Codex and Claude receive the Manim skill and its bundled resources without a new installer rule

### Requirement: Portable attributed resources
The skill SHALL preserve upstream attribution and provide resolvable local references in both categorized and flat skill installations.

#### Scenario: Read bundled guidance
- **WHEN** an agent follows a bundled Markdown resource link
- **THEN** the linked resource exists within the skill or is an explicitly external source

### Requirement: Evidence-based production workflow
The skill SHALL guide agents through scoping, environment preflight, scene planning, authoring, rendering and visual inspection, and report missing runtime dependencies without claiming a successful render.

#### Scenario: Runtime is unavailable
- **WHEN** Manim or a required rendering dependency is unavailable
- **THEN** the agent reports the missing dependency and distinguishes prepared source from validated video

#### Scenario: Deliver rendered video
- **WHEN** the agent reports a completed video
- **THEN** delivery includes the source and rendered artifact paths, visual inspection findings and any remaining limitations
