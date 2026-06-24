# Canonical Prompt — develop.md

Written to `$WORKSPACE/prompts/develop.md` during Step 1-C.  
Replace `{TASK}` with the user's task description before writing.

```markdown
# Develop Phase

## Task
{TASK}

## Your job
Implement the plan for loop {loop_id}.

## Required reading
- Any AGENTS.md or CLAUDE.md in the working repository
- loops/loops{loop_id}/plans/

## Implementation rules
- Use Edit, Write, and Bash tools to make ACTUAL file changes.
- Runtime data-use rule: use only the allowed input fields defined in the plan.
- Tuning/threshold search must use only the dev split (never the blind/test split).

## Dev record
After implementing, write a dev record. Include:
- Every changed or created file and the key changes made
- Design decisions and trade-offs
- How dev/blind split discipline was maintained
- Data-use compliance notes
- Any blocked items

## Output rules
- Raw markdown only. Start with `# Loop {loop_id} — Dev`.
- No preamble, no fence.
- Use the Edit, Write, and Bash tools to implement the changes before writing the record.
- The development record (markdown) must be the last thing you output.
- Write the record file before finishing.
```
