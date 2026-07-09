---
name: loop-analysis
description: Produce fixed-format Traditional Chinese markdown analysis for ESG contest agent-loop runs with plan/dev/exp/reflect records. Use for Claude, generic agent-loop, or non-Codex controllers such as exp/claude_agent_loop and exp/agent_loop_st3_0612.
---

# Loop Analysis

Use this skill to analyze ESG contest loop controllers that are not necessarily
under `exp/codex_agent_loop`. For Codex-specific loops under
`exp/codex_agent_loop/loops/loopsNNN/`, prefer the existing
`codex-loop-analysis` skill.

## When To Use

Invoke when the user asks:

- `分析 loops X-Y`
- `整理 loop 觀察`
- `把 loop 寫到 observe`
- `分析 exp/claude_agent_loop`
- `分析 exp/agent_loop_st3_0612 loops`

Each loop is expected to have phase records:

```text
plans/
dev/
exp/
reflect/
```

If a phase file is missing, mark that loop `pending` or `incomplete`; do not
skip it.

## Resolve Inputs

Before writing, resolve:

1. **Loop range**: explicit start/end ids such as `001-010`.
2. **Source directory**: controller loop root, for example:
   - `exp/claude_agent_loop/loops/`
   - `exp/agent_loop_st3_0612/loops/`
   - `exp/agent_loop_controller/loops/`
3. **Output path**: default to:
   - `docs/plans/<controller>_loop_observe/loops_<start>_<end>_<stage>_analysis.md`
   - or the controller's existing observe directory if one already exists

If range or source directory is ambiguous, ask once. If only topic is missing,
infer a concise topic from the loop target stage/methods.

## References

For each loop, read available phase files. Prefer exact filenames but fall back
to any markdown under the phase directory:

- `plans/*.md`
- `dev/*.md`
- `exp/*.md`
- `reflect/*.md`

Also read once when available:

- controller README
- controller state JSON
- `docs/methods.md` when analysis involves promotion, current methods, or
  end-to-end cascade behavior

Trust on-disk records over memory.

## Environment

- Supported controller roots include `exp/claude_agent_loop/loops/`,
  `exp/agent_loop_st3_0612/loops/`, and
  `exp/agent_loop_controller/loops/`.
- Default output path:
  `docs/plans/<controller>_loop_observe/loops_<start>_<end>_<stage>_analysis.md`
  unless the controller already has an observe directory.
- Codex-specific loops under `exp/codex_agent_loop/loops/loopsNNN/` should use
  the existing `codex-loop-analysis` skill when available.

## Output Format

Always write these sections in this exact order:

```markdown
# <title>
## 0. TOC
## 1. Baseline vs Methods
## 2. Plan / Dev / Exp / Reflect 對齊狀況
## 3. Gate 通過 / 失敗總表
## 4. 下一步建議
## 5. 方法介紹
```

Use Traditional Chinese for headings and prose. Keep metric names, artifact
paths, variant names, and verdict words as written in the loop files.

Do not add prose before `## 0. TOC`.

### 0. TOC

Include a one-line scope note:

```markdown
範圍：loops 001-010、controller `exp/agent_loop_st3_0612`、Stage 3
(`evidence_quality`) on `<artifact or method context>`。
```

Then list links to sections 1-5.

### 1. Baseline vs Methods

Start with a compact baseline block:

- baseline artifact path
- weighted score if available
- all stage Macro-F1 scores available
- primary metric and target stage

Then one table sorted by improvement descending:

| Loop | Method family | Best variant | Primary metric | Delta vs baseline | Weighted | Verdict |
| --- | --- | --- | ---: | ---: | ---: | --- |

Rules:

- Use the best variant named in exp or reflect.
- Use the plan-declared primary metric when available.
- Use signed deltas.
- Use `-` when a metric is missing.
- Verdict comes from reflect: `accept`, `reject`, `defer`, or `pending`.

### 2. Plan / Dev / Exp / Reflect 對齊狀況

One row per loop:

| Loop | Planned method | Implemented method | 對齊 | 備註 |
| --- | --- | --- | --- | --- |

`對齊` must be one of:

- `aligned`
- `pivoted`
- `partial`
- `stale reflect`
- `incomplete`

Flag stale reflect files, duplicated records, or cases where a stage-specific
loop changes upstream/downstream cascade behavior.

### 3. Gate 通過 / 失敗總表

Use the gates from each plan. For Stage 3 integrated cascade loops, default to:

| Loop | ST3 gate | Weighted gate | ST1 non-regress | ST2 non-regress | ST4 non-regress | Cascade valid | Data-only | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Cell values:

- `PASS`
- `FAIL (<delta or reason>)`
- `-`

End with:

```text
總結：X / Y loops fully pass；A defer；B reject；C pending。
```

### 4. 下一步建議

Use the latest completed reflect record as the primary source. Provide 3-6
numbered recommendations. Mark items:

- **mandatory** when reflect makes it a hard requirement
- **fallback** when reflect frames it as secondary

If latest reflect is missing, use the previous completed reflect and say so.

### 5. 方法介紹

One subsection per loop:

```markdown
### Loop NNN - <method family>
```

Each subsection must use exactly these labels:

- **計畫家族**：planned method family, hypothesis, variants/ablations.
- **執行結果**：best variant, primary metric, weighted, changed-row diagnostics.
- **關鍵發現**：3-5 bullets from exp/reflect findings.
- **Verdict**：bold verdict plus one sentence explaining why.

Keep each subsection concise. Do not paste raw variant grids.

Optionally end Section 5 with `### 橫向觀察` only when there is a cross-loop
pattern not already clear from sections 1-3.

## Rules

Follow the hygiene rules below and the fixed output format exactly.

### Hygiene Rules

- Never invent numbers, thresholds, artifact paths, or verdicts.
- If exp/dev/reflect disagree, treat exp metrics as authoritative and flag the
  mismatch in Section 2.
- Explicitly flag benchmark-overfit risk for benchmark-specific tuning.
- For promotion decisions, verify that reflect checks every gate item before
  saying a method can update `docs/methods.md` or state JSON.
- Cite paths sparingly; do not dump large file listings.
- Do not run git commands unless explicitly asked.

## Workflow

1. Resolve loop range, source directory, and output path.
2. Read phase files for every loop.
3. Extract baseline, best variant, primary metric, weighted score, stage scores,
   changed rows, cascade/data-only status, and verdict.
4. Build Section 1 first.
5. Build Section 2 from phase comparison.
6. Build Section 3 from plan gates and exp/reflect evidence.
7. Build Section 4 from latest completed reflect.
8. Build Section 5 loop by loop.
9. Write the markdown file.
10. Report output path, loops analyzed, verdict counts, and the main unresolved
    issue.

## Output

Final responses should include:

- Output markdown path.
- Loop range and controller analyzed.
- Verdict counts.
- Main unresolved issue or next recommendation.
