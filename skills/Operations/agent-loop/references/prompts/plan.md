# Canonical Prompt — plan.md

Written to `$WORKSPACE/prompts/plan.md` during Step 1-C.  
Replace `{TASK}` with the intake-confirmed task spec (Step 0) before writing.

```markdown
# Plan Phase

## Task
{TASK}

## Your job
Write a method-level plan for loop {loop_id} (target: {target_loop}).

## Required reading
- Any AGENTS.md or CLAUDE.md in the working repository
- docs/methods.md (or equivalent method registry) if it exists
- All prior plans: loops/loops*/plans/*.md (build a Novelty Check)

Current best_artifact metrics (auto-loaded):
{best_metrics}

## Plan requirements
1. One distinct method family — not just a hyperparameter point.
2. Multiple variants or ablations inside this loop.
3. **Novelty Check**: name the closest prior loop and the method-level difference.
4. Baseline, primary metric, secondary metrics.
5. Acceptance and rejection thresholds (score_first_promote gate).
6. Data-use boundaries (what inputs are allowed at runtime).
7. Failure modes and abandonment criteria.
8. A `## Parallel Subtasks` section at the end listing parallelisable parts
   (format: `- id: X  phase: dev|exp|both  description: …`), or `(none)`.

## Output rules
- Raw markdown only. Start with `# Loop {loop_id} — …`.
- No preamble, no fence, no commentary outside the plan content.
- Write the file before finishing.
```
