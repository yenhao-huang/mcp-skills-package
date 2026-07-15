# Environment Rules

Primary language: Markdown instructions
Runtime version: Git 2.x and GitHub CLI 2.x
Package manager: None
Frameworks: GitHub REST/GraphQL API through `gh`
Service manager: None
Required services: GitHub access with permission to push the head branch and
create or edit pull requests

- Verify `gh auth status` before GitHub mutations and never print tokens.
- Do not install or reconfigure Git, `gh`, credential helpers, or SSH settings
  without user approval.
- Stop on authentication or authorization failure and report the exact failed
  operation.
