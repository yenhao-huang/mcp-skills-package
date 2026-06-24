# Canonical Prompt — reflect.md

Written to `$WORKSPACE/prompts/reflect.md` during Step 1-C.  
Replace `{TASK}` with the user's task description before writing.

```markdown
# Reflect Phase

## Task
{TASK}

## Your job
Evaluate loop {loop_id} and decide whether to promote the result.

## Required reading
- loops/loops{loop_id}/plans/
- loops/loops{loop_id}/dev/
- loops/loops{loop_id}/exp/
- docs/methods.md (or equivalent) — check if it needs updating

## Evaluation checklist
Answer each item explicitly (yes/no + evidence):

1. Did the primary metric exceed the acceptance threshold?
2. Did the blind/test metric exceed its threshold?
3. Is the generalization gap within the allowed limit?
4. Is the method data-use compliant (runtime uses only allowed fields)?
5. Was blind/test data excluded from tuning and rule design (split discipline)?
6. Does the method introduce a genuinely new family vs prior loops?
7. Does docs/methods.md (or equivalent) need updating?
8. What should the next loop try? (concrete, specific advice)

## Verdict
End with exactly one of:
  Verdict: accept
  Verdict: reject
  Verdict: defer

If `accept` → also update the method registry (docs/methods.md or equivalent).

## Output rules
- Raw markdown only. Start with `# Loop {loop_id} — Reflect`.
- No preamble, no fence.
- Write the record file before finishing.
```
