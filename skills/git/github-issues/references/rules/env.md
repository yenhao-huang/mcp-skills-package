# Environment Rules

Primary language: Markdown instructions
Runtime version: GitHub CLI 2.x or a compatible GitHub MCP server
Package manager: None
Frameworks: GitHub REST/GraphQL API and Model Context Protocol
Service manager: None
Required services: GitHub access with repository-appropriate permissions

- Prefer existing GitHub MCP configuration for supported operations.
- Use `gh auth status` before CLI or REST mutations; never print auth tokens.
- Do not install or reconfigure `gh` without user approval.
- Stop and report the exact missing permission when GitHub rejects an action.
