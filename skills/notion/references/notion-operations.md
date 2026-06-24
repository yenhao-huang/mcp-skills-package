# Notion Operations

Use the Notion MCP tools for workspace operations. Fetch before writes, and keep
updates narrowly scoped.

## Resolve A Target

1. Check `references/page-registry.md` for an exact alias, URL, or ID.
2. If no registry match exists, search Notion with the user's title or keywords.
3. Fetch likely matches to confirm title, parent context, and content shape.
4. If more than one plausible match remains, ask the user for the exact page.

## Page Reads

- Use `notion_fetch` for known page URLs/IDs.
- Use `include_discussions: true` when the user asks about comments,
  discussions, review state, or unresolved feedback.
- Summarize large pages by structure first, then content. Avoid copying long
  passages into the chat.

## Page Writes

- Always fetch the page before `update_page`.
- Use `insert_content` for additions, `update_content` for precise edits, and
  `update_properties` for metadata changes.
- Use `replace_content` only when the user asks to replace the whole page.
- If `replace_content` would delete child pages or databases, report the affected
  items and ask before proceeding.
- For external page content, keep Notion Markdown syntax conservative. If syntax
  is uncertain, fetch `notion://docs/enhanced-markdown-spec` before writing.

## Database Work

- If the user provides a database URL, fetch it before creating pages or views.
- Use the returned `collection://...` data source ID for database page creation,
  schema updates, queries, and linked views.
- Match exact property names from fetched schema.
- Split special property values as required by the Notion tool descriptions,
  especially date, place, checkbox, and user-defined `id` or `url` properties.

## Comments

- Use page-level comments for general feedback.
- Use `selection_with_ellipsis` only when the user identifies exact content or
  fetch output provides a unique snippet.
- Use `discussion_id` only to reply to an existing thread.

## Registry Maintenance

After a successful Notion operation, update `references/page-registry.md` when:

- A page should be remembered as commonly used.
- A URL, page ID, database ID, data source ID, or alias was newly discovered.
- A page role, schema note, or update rule changed.

Record validation evidence in `STATE.md`, including the fetch/search/update tool
used and the page/database identifier.
