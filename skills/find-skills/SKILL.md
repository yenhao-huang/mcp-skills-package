---
name: find-skills
description: >
  Help users discover and install agent skills when they ask questions like
  "how do I do X", "find a skill for X", "is there a skill that can...", or
  express interest in extending capabilities. Use when the user is looking for
  functionality that might exist as an installable skill.
---

# Find Skills

Use this skill to search the open agent skills ecosystem and recommend or
install relevant skills.

## When To Use

Use this skill when the user asks to:

- Find a skill for a specific task or domain.
- Check whether a specialized capability exists as an installable skill.
- Extend agent capabilities with tools, templates, workflows, or domain
  knowledge.
- Install or update a discovered skill.

Do not use this skill when:

- The task is clearly solvable directly and the user did not ask about skills.
- The user asks to create a new local skill; use `skill-creator` instead.
- You cannot verify the quality of a recommended skill.

## Workflow

1. Clarify the domain, concrete task, and whether a skill likely exists.
2. Check the skills ecosystem and popular sources first.
3. Search with specific keywords using `npx skills find <query>` when needed.
4. Verify quality before recommending: install count, source reputation, and
   repository trust signals.
5. Present a small set of options with name, purpose, install count/source when
   available, install command, and link.
6. If the user chooses one, install it with the Skills CLI.
7. If no suitable skill exists, say so and offer to help directly or create a
   custom skill.

## References

- Browse skills at `https://skills.sh/`.
- Use `npx skills find [query]` to search.
- Use `npx skills add <owner/repo@skill> -g -y` to install globally after user
  approval.
- Use `npx skills check` and `npx skills update` for update workflows.

## Environment

- The Skills CLI command is `npx skills`.
- Common search categories include web development, testing, DevOps,
  documentation, code quality, design, productivity, automation, and git.

## Rules

- Do not recommend a skill based solely on search result text.
- Prefer official or well-known sources such as `vercel-labs`, `anthropics`, or
  `microsoft` when quality is comparable.
- Treat skills with very low installs or weak repository signals as risky.
- Use specific search terms; try alternatives such as `deploy`, `deployment`,
  and `ci-cd` when needed.
- Do not install a skill unless the user asks you to proceed.

## Output

Final responses should include:

- Recommended skill names and what each does.
- Install command for the chosen or recommended skill.
- Link to learn more when available.
- Any quality caveat or reason no skill was found.
