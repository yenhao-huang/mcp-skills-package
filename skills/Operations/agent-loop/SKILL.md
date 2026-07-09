---
name: agent-loop
description: >
  Run a 4-phase agent loop for optimization tasks: plan, dev, exp, and reflect.
  Creates an independent timestamped workspace under exp/agent_loop/claude.
  Each phase is a separate Agent session with fresh context. Parallel subtasks
  within a phase are dispatched as concurrent subagents. Use when the user says
  "run agent loop on X", "optimize X with agent loop", "agent loop run X", or
  resumes a stalled loop with "resume loop" plus a workspace path.
---

# Agent Loop Skill

Orchestrates a structured 4-phase optimization loop.  
Every phase is an **independent Agent session** (fresh context window).  
Parallel subtasks within dev/exp are dispatched as **concurrent subagents**.

---

## When To Use

Use this skill when the user asks to:

- Run an agent loop for an optimization task.
- Optimize a method, benchmark, model, pipeline, or experiment with repeated
  plan/develop/experiment/reflect cycles.
- Resume a paused or stalled loop from `exp/agent_loop/claude/<timestamp>`.
- Run autonomous loop mode with `loop=<N>` or `--autonomous`.

Do not use this skill when:

- The user asks for a one-off code change, experiment, or analysis that does not
  need the full loop controller.
- The user asks for Codex-specific loop analysis; use the relevant analysis
  skill instead.
- The task has no measurable acceptance/rejection signal.

## Workflow

1. Parse invocation flags such as `resume`, `loop=<N>`, `--autonomous`, and
   `--resume-after=<Xh>`.
2. Run Step 0 task intake unless resuming an existing workspace.
3. Initialize or load the timestamped workspace and `state.json`.
4. Run the four phases in order: plan, dev, exp, reflect.
5. Use independent Agent sessions for every phase; use concurrent subagents only
   where the detailed phase rules allow it.
6. Synthesize phase outputs into canonical loop records.
7. Apply reflect verdicts to decide whether to promote, continue, defer, reject,
   or pause.
8. Run the usage watchdog at phase boundaries.
9. Report workspace, loop status, verdict, and next resume command.

## Invocation

```
/agent-loop <task description> [--resume-after=<Xh>]
/agent-loop resume exp/agent_loop/claude/<timestamp>
```

`--resume-after=<Xh>` — how long to sleep when session usage hits 80 % (e.g.
`--resume-after=2h`). Default: `1h`. Accepts integer hours only.

---

## Step 0 — Task intake

**Run this before any workspace or file is created.** Skip it only on
`resume <path>` (an existing run already has an agreed task spec).

### 0-A.0. Detect autonomous mode FIRST

Check the invocation prompt for either of these signals:

- `loop=<N>` anywhere in the prompt (e.g. `loop=100`, `loop=50`)
- `--autonomous` flag

If **either signal is present**, enter **autonomous mode**:

1. Do **not** ask the user anything.
2. Parse `target_loop` from `loop=<N>` in the prompt (or use `100` if
   `--autonomous` is given without a number).
3. Auto-fill the entire task spec from repo files (steps 0-A.1 and 0-A.3
   below), using only what can be read without user input.
4. Write the auto-filled spec to
   `$WORKSPACE/logs/autonomous_task_spec.md` before proceeding to Step 1.
5. Skip steps 0-A.2 entirely.

If **no signal is present**, proceed with the interactive flow (0-A.1 → 0-A.2
→ 0-A.3) as normal.

---

### 0-A.0b. Parse `--resume-after` (both modes)

Extract `--resume-after=<Xh>` from the invocation string.  
Convert to integer seconds: `resume_after_seconds = X * 3600`. Default: `3600`.  
Store it; carry it into state in Step 1-D.

---

### 0-A.1. Gather context (both modes)

Read the following before writing anything:

- `CLAUDE.md` / `AGENTS.md` — problem definition, data-use rules, promotion gate.
- `docs/methods.md` — current stage methods and end-to-end behavior.
- `docs/loops/agent_loop_state.json` — current baseline artifact and best
  metrics (the baseline the new loop must beat).
- Prior loop dirs (`docs/loops/loops*/` and any
  `exp/agent_loop/claude/*/loops/`) — what was already tried, so the new
  task is not a duplicate.

### 0-A.2. Confirm the task spec with the user (interactive mode only)

Present a short proposed task spec and ask the user to confirm or adjust. Use
the available structured user-input tool only when the current execution mode
provides one; otherwise ask concise plain-text questions. Cover, at minimum:

- **Objective / scope**: which stage(s) or metric is this loop optimizing, and
  what is the one method idea to try first.
- **Baseline**: the exact baseline artifact + its current weighted score and
  affected-stage Macro-F1 (cite `docs/loops/agent_loop_state.json`).
- **Primary + secondary metrics** and the **acceptance / rejection
  thresholds** (the `score_first_promote` gate values).
- **Data-use boundaries**: confirm only `data` is allowed as raw input and
  which fields stay forbidden (default to the CLAUDE.md problem definition
  unless the user overrides).
- **Target loop count** (`target_loop`) and how many loops to run now vs. stop
  for review.
- **Constraints**: time/compute budget, models/tools allowed, anything that
  must not change.

Do not proceed to Step 1 until the user has confirmed (or explicitly said
"use your defaults").

### 0-A.3. Record the agreed spec (both modes)

Write (or echo to user in interactive mode) the final task spec:

```
Task spec (confirmed / autonomous):
  Objective:   <…>
  Baseline:    <artifact> (weighted=<…>, ST<n>=<…>)
  Primary:     <metric>  accept ≥ <…>  reject < <…>
  Data-use:    input = data only; forbidden = <…>
  target_loop: <N>
  mode:        autonomous | interactive
```

In autonomous mode write this block to
`$WORKSPACE/logs/autonomous_task_spec.md`.

Carry these values into Step 1 (`state.json`: `task`, `target_loop`,
`best_artifact`) and into the Step 1-C plan-template customisation.

---

## Step 1 — Workspace initialisation

### 1-A. New loop

```bash
TIMESTAMP=$(date -u +%Y%m%dT%H%M%S)
WORKSPACE=exp/agent_loop/claude/$TIMESTAMP
mkdir -p $WORKSPACE/loops
mkdir -p $WORKSPACE/prompts
mkdir -p $WORKSPACE/logs
```

`WORKSPACE` is the root for this entire loop run. Record it and show it to the
user immediately:

```
Workspace: exp/agent_loop/claude/<timestamp>
```

### 1-B. Resume

If the user passed `resume <path>`, set `WORKSPACE=<path>` and skip to 1-D
(read existing `state.json`).

If `state["paused_for_usage"]` is `true`: clear it and reset the check timer:

```json
{ "paused_for_usage": false, "last_usage_check_at": "<now>" }
```

Then continue from `state["phase"]` as normal.

### 1-C. Write the 4 prompt templates

Create `$WORKSPACE/prompts/plan.md`, `develop.md`, `experiment.md`,
`reflect.md` using the **Canonical Prompt Templates** in the Reference section
at the bottom of this file.  
Customise each template's `## Task` block for the user's task description
before writing.

### 1-D. Initialise / load state

State file: `$WORKSPACE/state.json`

If it does not exist, write (using the task spec confirmed in Step 0):

```json
{
  "task":                   "<intake-confirmed task description>",
  "workspace":              "exp/agent_loop/claude/<timestamp>",
  "next_loop":              1,
  "target_loop":            "<intake-confirmed target_loop>",
  "phase":                  "plan",
  "current_loop":           null,
  "last_completed_loop":    0,
  "last_verdict":           "",
  "best_artifact":          "",
  "subtasks":               [],
  "usage_pause_threshold":  0.80,
  "resume_after_seconds":   "<from --resume-after, default 3600>",
  "last_usage_check_at":    null,
  "paused_for_usage":       false,
  "updated_at":             "<ISO-8601 UTC now>"
}
```

If it exists (resume), load it; `LOOP_ID = state["current_loop"] or
state["next_loop"]`.

### 1-E. Create loop directories

```
$WORKSPACE/loops/loops{NNN}/plans/
$WORKSPACE/loops/loops{NNN}/dev/
$WORKSPACE/loops/loops{NNN}/exp/
$WORKSPACE/loops/loops{NNN}/reflect/
```

where `NNN = f"{LOOP_ID:03d}"`.

Update state: `current_loop = LOOP_ID`, `updated_at = now()`.

---

## Step 2 — Plan phase

Spawn **one Agent**:

```
You are the plan agent for agent loop {LOOP_ID}.

Task: {task}
Workspace: {WORKSPACE}
Best artifact so far: {best_artifact or "none"}

Read before writing:
  {WORKSPACE}/prompts/plan.md          ← follow every rule here
  {WORKSPACE}/loops/loops*/plans/*.md  ← build novelty check from these

Write the plan to:
  {WORKSPACE}/loops/loops{NNN}/plans/{NNN}_agent_loop_plan.md

The plan MUST end with a fenced section:

## Parallel Subtasks
- id: <short_id>  phase: dev|exp|both  description: <one line>
(or "(none)" if the method has no parallelisable parts)

Write the file before finishing.
```

After the agent completes:
- Read the plan file.
- Parse `## Parallel Subtasks` → store list in `state["subtasks"]`.
- Update state: `phase = develop`, `updated_at = now()`.
- Show user: `"Plan done. Subtasks: {subtasks}"`.
- **Call [§ Usage Watchdog](#-usage-watchdog). If it pauses, stop.**

---

## Step 3 — Dev phase

### 3-A. No subtasks (or all `phase: exp`)

Spawn **one Agent**:

```
You are the dev agent for agent loop {LOOP_ID}.

Task: {task}
Workspace: {WORKSPACE}

Read:
  {WORKSPACE}/prompts/develop.md
  {WORKSPACE}/loops/loops{NNN}/plans/

Implement the plan. Use Edit, Write, Bash tools to make real file changes.
Write dev record to:
  {WORKSPACE}/loops/loops{NNN}/dev/{NNN}_agent_loop_dev.md

Record: every changed file, key decisions, data-use compliance.
Write the file before finishing.
```

### 3-B. Parallel subtasks (phase: dev or both)

In **one message**, spawn one Agent per subtask:

```
You are dev subagent for subtask [{id}] in agent loop {LOOP_ID}.

Subtask: {description}
Plan: {WORKSPACE}/loops/loops{NNN}/plans/

Read {WORKSPACE}/prompts/develop.md for conventions.

Implement ONLY this subtask. Use Edit, Write, Bash tools.
Write notes to:
  {WORKSPACE}/loops/loops{NNN}/dev/dev_{id}.md

Include: changed files, decisions, compliance.
Write the file before finishing.
```

Then spawn one **synthesis Agent**:

```
Read all files in {WORKSPACE}/loops/loops{NNN}/dev/.
Write merged dev record to:
  {WORKSPACE}/loops/loops{NNN}/dev/{NNN}_agent_loop_dev.md

List every subtask, every changed file, confirm data-use compliance.
```

Update state: `phase = experiment`, `updated_at = now()`.

**Call [§ Usage Watchdog](#-usage-watchdog). If it pauses, stop.**

---

## Step 4 — Experiment phase

### 4-A. No subtasks (or all `phase: dev`)

Spawn **one Agent**:

```
You are the experiment agent for agent loop {LOOP_ID}.

Task: {task}
Workspace: {WORKSPACE}

Read:
  {WORKSPACE}/prompts/experiment.md
  {WORKSPACE}/loops/loops{NNN}/plans/
  {WORKSPACE}/loops/loops{NNN}/dev/

Run experiments using Bash tool. Record ACTUAL results — do not fabricate.
Write experiment record to:
  {WORKSPACE}/loops/loops{NNN}/exp/{NNN}_agent_loop_exp.md

Include: every command run, real stdout/stderr, all metric values,
artifact paths, gate-check table.
Write the file before finishing.
```

### 4-B. Parallel variants (phase: exp or both)

In **one message**, spawn one Agent per subtask:

```
You are experiment subagent for variant [{id}] in agent loop {LOOP_ID}.

Variant: {description}
Plan: {WORKSPACE}/loops/loops{NNN}/plans/
Dev:  {WORKSPACE}/loops/loops{NNN}/dev/

Read {WORKSPACE}/prompts/experiment.md for eval conventions.

Run ONLY this variant via Bash tool. Record actual results.
Write to:
  {WORKSPACE}/loops/loops{NNN}/exp/exp_{id}.md

Include: exact command, real metrics, artifact path.
```

Then spawn one **synthesis Agent**:

```
Read all files in {WORKSPACE}/loops/loops{NNN}/exp/.
Write merged experiment record to:
  {WORKSPACE}/loops/loops{NNN}/exp/{NNN}_agent_loop_exp.md

Include: variant comparison table, best variant, all gate checks, artifact paths.
Follow format in {WORKSPACE}/prompts/experiment.md.
```

Update state: `phase = reflect`, `updated_at = now()`.

**Call [§ Usage Watchdog](#-usage-watchdog). If it pauses, stop.**

---

## Step 5 — Reflect phase

Spawn **one Agent**:

```
You are the reflect agent for agent loop {LOOP_ID}.

Workspace: {WORKSPACE}

Read:
  {WORKSPACE}/prompts/reflect.md
  {WORKSPACE}/loops/loops{NNN}/plans/
  {WORKSPACE}/loops/loops{NNN}/dev/
  {WORKSPACE}/loops/loops{NNN}/exp/

Evaluate the loop against every criterion in reflect.md.
End with exactly one verdict line:
  Verdict: accept
  Verdict: reject
  Verdict: defer

If Verdict: accept → update docs/methods.md (or the task's equivalent
method registry) to record the accepted method.

Write reflect record to:
  {WORKSPACE}/loops/loops{NNN}/reflect/{NNN}_agent_loop_reflect.md

Write the file before finishing.
```

After the agent completes:
- Read reflect file, extract verdict.
- **Call [§ Usage Watchdog](#-usage-watchdog). If it pauses, stop.**
- Update state:
  ```json
  {
    "last_completed_loop": LOOP_ID,
    "last_verdict":        "<accept|reject|defer>",
    "next_loop":           LOOP_ID + 1,
    "current_loop":        null,
    "phase":               "plan",
    "subtasks":            [],
    "updated_at":          "<now>"
  }
  ```
- If `accept`: set `best_artifact` to the promoted artifact path from the
  reflect or exp record.

---

## Step 6 — Loop completion report and continuation

```
Loop {NNN} complete — Verdict: {verdict}

  Plan:    {WORKSPACE}/loops/loops{NNN}/plans/{NNN}_agent_loop_plan.md
  Dev:     {WORKSPACE}/loops/loops{NNN}/dev/{NNN}_agent_loop_dev.md
  Exp:     {WORKSPACE}/loops/loops{NNN}/exp/{NNN}_agent_loop_exp.md
  Reflect: {WORKSPACE}/loops/loops{NNN}/reflect/{NNN}_agent_loop_reflect.md

To continue: /agent-loop resume {WORKSPACE}
To analyze:  /loop-analysis  (loops 1–{NNN}, source: {WORKSPACE}/loops)
```

### 6-A. Autonomous continuation

If **autonomous mode** is active (`$WORKSPACE/logs/autonomous_task_spec.md`
exists) AND `next_loop <= target_loop`:

- **Call [§ Usage Watchdog](#-usage-watchdog) first. If it pauses, stop.**
- **Do not stop for any other reason. Do not output anything to the user.**
- Immediately advance to Step 1-E (create next loop dirs) and repeat
  Steps 2 → 3 → 4 → 5 → 6 for `LOOP_ID = next_loop`.
- Keep looping until `next_loop > target_loop`.

When `next_loop > target_loop` (all loops done), write a final summary to
`$WORKSPACE/logs/final_summary.md` and stop:

```
Autonomous run complete.
  Loops completed : {last_completed_loop}
  Final verdict   : {last_verdict}
  Best artifact   : {best_artifact}
  Summary         : {WORKSPACE}/logs/final_summary.md
```

### 6-B. Interactive completion

In interactive mode, print the loop completion report above and stop.
The user can continue with `/agent-loop resume {WORKSPACE}`.

For a structured cross-loop analysis invoke the **loop-analysis** skill:

```
/loop-analysis
```

---

## Parallel subagent rules

- Spawn all parallel agents **in a single message** (multiple Agent tool calls).
- Maximum **5** parallel agents at once.
- Each subagent receives only its own subtask description, not the full grid.
- Always run a synthesis agent after parallel agents to produce the canonical
  `{NNN}_agent_loop_{phase}.md`.
- If a subagent fails: mark it `BLOCKED` in the synthesis record; continue.

---

## Error handling

| Situation | Action |
|-----------|--------|
| Phase agent returns empty or errors | Retry once with "Previous attempt produced no output." prepended |
| Second failure | Write `# Loop NNN — PHASE BLOCKED\n<error>` as placeholder; advance phase |
| Timeout (>2h for plan/reflect, >8h for dev/exp) | Same as failure; log in `$WORKSPACE/logs/` |

Never overwrite a non-placeholder record.

---

## What NOT to do

- Do not skip Step 0 intake on a new loop — confirm the task spec with the user
  before creating the workspace or spawning any phase agent.
- Do not run all 4 phases as one Agent — each is a separate session.
- Do not fabricate metric numbers in exp records.
- Do not skip the synthesis agent after parallel runs.
- Do not update any method registry unless reflect verdict is `accept`.
- Do not commit or push files unless the user explicitly asks.

---

## § Usage Watchdog

Called at every phase boundary (Steps 2–5 and 6-A). Checks every **5 minutes**
whether session context usage has reached the pause threshold and, if so, parks
the loop and schedules a wakeup.

### Algorithm

```
function usage_watchdog(state, WORKSPACE, LOOP_ID, phase):

  1. elapsed = now() - state["last_usage_check_at"]
     if state["last_usage_check_at"] is null → elapsed = ∞

  2. if elapsed < 300 s:
       return CONTINUE          # check interval not reached

  3. state["last_usage_check_at"] = now()   # reset timer

  4. Estimate session usage:
     a. COMPRESSION signal — if the conversation context shows
        "<system-reminder>…summarized…</system-reminder>" markers,
        treat this as ≥ 75 % usage.
     b. AGENT-CALL PROXY — agent_calls_this_session / 60 gives a rough
        fraction (60 calls ≈ full context for a long run).
     c. Use your own judgment: when this conversation is notably long
        (many summarization turns visible), err toward pausing.
     Take the maximum of all signals as `estimated_pct`.

  5. if estimated_pct < state["usage_pause_threshold"]:
       return CONTINUE

  6. # Threshold reached — pause
     timestamp = now_iso()
     resume_secs = state["resume_after_seconds"]   # default 3600
     resume_hrs  = resume_secs / 3600

     Write $WORKSPACE/logs/usage_pause_<timestamp>.md:
       # Usage Pause
       Loop  : {LOOP_ID}
       Phase : {phase}
       Usage : ~{estimated_pct*100:.0f}%
       Paused: {timestamp}
       Resume: {timestamp + resume_secs}  (in {resume_hrs:.1f} h)

     Update state:
       paused_for_usage = true
       updated_at       = now()

     Call ScheduleWakeup(
       delaySeconds = resume_secs,
       prompt       = "/agent-loop resume {WORKSPACE}",
       reason       = "session ~{estimated_pct*100:.0f}% — cooldown {resume_hrs:.1f} h"
     )

     Print: "⚠ Session usage ~{pct}%. Pausing after loop {LOOP_ID}/{phase}.
             Will resume in {resume_hrs:.1f} h via ScheduleWakeup."

     return PAUSED
```

### Notes

- The watchdog is **silent** when it skips (elapsed < 300 s or usage < threshold).
- On resume (`/agent-loop resume`), Step 1-B clears `paused_for_usage` and
  resets `last_usage_check_at` so the next check fires no sooner than 5 min later.
- If `ScheduleWakeup` is unavailable (non-`/loop` invocation), fall back to
  printing the resume command and stopping; the user must re-invoke manually.

---

## Environment

- New workspaces are created under `exp/agent_loop/claude/<timestamp>/`.
- Each workspace owns `state.json`, `prompts/`, `logs/`, and
  `loops/loopsNNN/{plans,dev,exp,reflect}/`.
- Phase prompts are written from `references/prompts/*.md`.
- Controller details and promotion helpers live in
  `references/controller_logic.md`.
- `--resume-after=<Xh>` defaults to `1h` and stores seconds in state.

## Rules

- Confirm the task spec before creating a new workspace unless autonomous mode
  is explicitly requested.
- Do not run the four phases in one Agent session.
- Do not skip synthesis after parallel subagents.
- Do not fabricate metric numbers or verdicts.
- Do not update method registries unless reflect verdict is `accept`.
- Do not commit or push files unless the user explicitly asks.

## Output

Final responses should include:

- Workspace path.
- Current loop id and phase status.
- Latest verdict and promoted artifact, if any.
- Validation or metric evidence.
- Resume command when the loop is paused or incomplete.

## References

| File | Content |
|------|---------|
| [`references/controller_logic.md`](references/controller_logic.md) | Python state machine, file naming, `parse_verdict`, `load_best_metrics`, `_run_promote` |
| [`references/prompts/plan.md`](references/prompts/plan.md) | Canonical template written to `$WORKSPACE/prompts/plan.md` |
| [`references/prompts/develop.md`](references/prompts/develop.md) | Canonical template written to `$WORKSPACE/prompts/develop.md` |
| [`references/prompts/experiment.md`](references/prompts/experiment.md) | Canonical template written to `$WORKSPACE/prompts/experiment.md` |
| [`references/prompts/reflect.md`](references/prompts/reflect.md) | Canonical template written to `$WORKSPACE/prompts/reflect.md` |
