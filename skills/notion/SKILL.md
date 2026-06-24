---
name: notion
description: Manage the user's commonly used Notion pages. Use when the user asks to find, fetch, summarize, update, organize, comment on, duplicate, move, or maintain a registry of frequent Notion pages, including phrases like Notion page, common pages, 常用 Notion, workspace pages, page registry, database, or data source.
---

# Notion Page Manager

Use this skill to manage the user's frequently used Notion pages and keep a
small local registry of important page URLs, IDs, roles, and update rules.

## When To Use

Use this skill when the user asks to:

- Open, find, fetch, summarize, update, comment on, duplicate, or move a Notion
  page they use often.
- Maintain a list of commonly used Notion pages, databases, or data sources.
- Create, update, or query Notion pages while preserving a reliable local map of
  page names to IDs/URLs.
- Work with Notion databases, views, templates, comments, or page content.

Do not use this skill when:

- The task is only general writing and does not involve Notion.
- The user provides all needed Notion content inline and no page operation is
  required.
- The operation is purely about local Markdown files.

## Workflow

1. Read the user's request and identify the target page, database, or registry
   action.
2. Read `STATE.md`; for a new run, reset it from
   `references/template/STATE.template.md`.
3. Read `references/page-registry.md` to resolve known aliases, URLs, IDs,
   ownership notes, and safe update rules.
4. If the target is unknown, use Notion search/fetch tools before asking the
   user. Ask only when multiple plausible pages remain.
5. For Notion page writes, fetch the current page first. For database page
   writes, fetch the database or data source schema first.
6. Apply the smallest change that satisfies the request. Preserve unrelated
   page content and child pages/databases.
7. Update `references/page-registry.md` when a new frequent page is identified
   or when an existing ID/URL/role changes.
8. Validate by fetching the changed page, database, data source, comments, or
   registry entry.
9. Record outcome and evidence in `STATE.md`.

## References

- Read `references/page-registry.md` before resolving page aliases or deciding
  whether a page is one of the user's common pages.
- Read `references/notion-operations.md` before writing pages, changing database
  schemas, manipulating views, or working with comments.
- Use `references/template/STATE.template.md` to reset `STATE.md` for a new run.

## Rules

- Prefer exact Notion IDs or URLs from the registry over semantic search.
- Do not overwrite full page content unless the user explicitly asks for a full
  replacement.
- Before `replace_content`, preserve child pages and databases with their exact
  tags from fetch output. If deletion is required, stop and ask.
- For comments, use page-level comments unless the user identifies a specific
  content selection or discussion.
- Keep the registry concise. Add only pages the user identifies as recurring or
  pages that become operationally important during a task.
- Use absolute dates when recording time-sensitive page notes.

## Output

Final responses should include:

- Which Notion page/database was touched or investigated.
- What changed, or what was found.
- Validation performed.
- Any unresolved ambiguity or permission limitation.
