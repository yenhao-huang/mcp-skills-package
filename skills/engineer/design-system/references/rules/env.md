# Environment Rules

Read the target project's environment and repository instructions before
choosing or changing implementation technology.

```text
Primary language: Inherit from the target frontend project
Runtime version: Inherit from the target project
Package manager: Use the target project's locked package manager
Frameworks: Framework-agnostic; preserve the existing UI framework
Service manager: None required by this skill
Required services: None
```

- Do not install packages, fonts, icon libraries, or component systems merely
  to apply these design rules.
- Prefer existing tokens, components, dependencies, and build tooling.
- Validate using the target project's declared formatter, type checker, tests,
  accessibility checks, visual tests, and browser targets.
- Treat remote fonts, images, analytics, and design services as external
  dependencies requiring explicit project support and user authority.
