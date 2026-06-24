# Canonical Prompt — experiment.md

Written to `$WORKSPACE/prompts/experiment.md` during Step 1-C.  
Replace `{TASK}` with the user's task description before writing.

```markdown
# Experiment Phase

## Task
{TASK}

## Your job
Run the experiments defined in the plan for loop {loop_id}.

## Required reading
- loops/loops{loop_id}/plans/
- loops/loops{loop_id}/dev/

## Protocol
1. Run the method on the dev split. Report primary metric + per-class breakdown.
2. Run the SAME method (no re-tuning) on the blind/test split.
3. Compute generalization gap = dev metric − blind metric.
4. Check against acceptance thresholds from the plan.
5. If the experiment cannot run, record the exact blocker.

## Experiment record
Write a record. Include:
- Every command run (exact, copy-pasteable)
- Real stdout/stderr excerpts (not fabricated)
- All metric values for every variant
- Artifact paths
- Gate-check table (pass / fail / Δ for each threshold)

## Output rules
- Raw markdown only. Start with `# Loop {loop_id} — Experiment`.
- No preamble, no fence.
- Use the Bash tool to run experiment commands. Record ACTUAL stdout/stderr and
  real metric values — do not fabricate numbers.
- The experiment record (markdown) must be the last thing you output.
- Write the record file before finishing.
```
