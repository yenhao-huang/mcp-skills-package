# Reference — Controller Logic

Python implementation this skill replicates in Agent-tool form.  
Use it to understand state transitions, file naming, and phase sequencing.

```python
# ── Constants ────────────────────────────────────────────────────────────────
PHASES = ["plan", "develop", "experiment", "reflect"]
DAY_TIMEOUT_SECONDS = 24 * 60 * 60


# ── Naming helpers ────────────────────────────────────────────────────────────
def loop_name(loop_id: int) -> str:
    return f"loops{loop_id:03d}"


# ── State helpers ─────────────────────────────────────────────────────────────
def default_state(start: int, end: int, best_artifact: str) -> dict:
    return {
        "next_loop":           start,
        "target_loop":         end,
        "phase":               "plan",
        "current_loop":        None,
        "last_completed_loop": start - 1,
        "best_artifact":       best_artifact,
        "last_verdict":        "",
        "updated_at":          now(),   # ISO-8601 UTC
    }


def load_or_init_state(state_path, resume, start, end, best_artifact):
    if state_path.exists() and resume:
        state = load_json(state_path)
        state.setdefault("target_loop", end)
        state.setdefault("best_artifact", best_artifact)
        return state
    return default_state(start, end, best_artifact)


def update_state(state_path, state, **updates):
    state.update(updates)
    state["updated_at"] = now()
    save_json(state_path, state)
    return state


# ── Directory helpers ─────────────────────────────────────────────────────────
def ensure_loop_dirs(loops_dir, loop_id):
    for name in ["plans", "dev", "exp", "reflect"]:
        (loops_dir / loop_name(loop_id) / name).mkdir(parents=True, exist_ok=True)


# ── Phase file naming ─────────────────────────────────────────────────────────
PHASE_FILES = {
    "plan":       ("plans",   "agent_loop_plan"),
    "develop":    ("dev",     "agent_loop_dev"),
    "experiment": ("exp",     "agent_loop_exp"),
    "reflect":    ("reflect", "agent_loop_reflect"),
}

def phase_record_path(loops_dir, loop_id, phase):
    subdir, stem = PHASE_FILES[phase]
    return loops_dir / loop_name(loop_id) / subdir / f"{loop_id:03d}_{stem}.md"


# ── Prior plan index (novelty context for plan prompt) ────────────────────────
def prior_plan_index(loops_dir, max_chars=12000):
    paths = sorted(loops_dir.glob("loops[0-9][0-9][0-9]/plans/*.md"))
    lines = []
    for path in paths:
        content = path.read_text(encoding="utf-8")
        heading = next((l.strip() for l in content.splitlines() if l.strip()), "")
        novelty = next((l.strip() for l in content.splitlines()
                        if "Novelty Check" in l), "")
        lines.append(f"- {path}: {heading} {novelty}".strip())
    text = "\n".join(lines)
    return text[-max_chars:] if len(text) > max_chars else text


# ── Strip markdown fences from Claude output ──────────────────────────────────
def strip_fences(text):
    stripped = text.strip()
    for lang in ("markdown", "md", ""):
        fence = f"```{lang}\n" if lang else "```\n"
        if stripped.startswith(fence) and stripped.endswith("```"):
            return stripped[len(fence):-3].strip()
    return stripped


# ── Verdict parsing (used after reflect) ─────────────────────────────────────
def parse_verdict(text):
    for line in reversed(text.splitlines()):
        low = line.strip().lower()
        if low.startswith("verdict:"):
            for v in ("accept", "reject", "defer"):
                if v in low:
                    return v
    return "unknown"


# ── Dynamic baseline metrics (injected into plan prompt) ─────────────────────
def load_best_metrics(best_artifact: str) -> str:
    path = ROOT / best_artifact
    if not path.exists():
        return "(best_artifact not found)"
    try:
        data = load_json(path)
        metrics = {
            "weighted_score": data.get("weighted_score", data.get("score")),
            "per_task": data.get("per_task", {}),
        }
        return json.dumps(metrics, ensure_ascii=False, indent=2)
    except Exception:
        return "(could not parse best_artifact)"


# ── Auto-promote on accept verdict ───────────────────────────────────────────
def _run_promote(args, loop_id):
    loop_path = loop_dir(loop_id)
    prompt = (
        f"Read docs/methods.md and all files under {loop_path.relative_to(ROOT)}. "
        f"Update docs/methods.md to document the accepted method change for loop {loop_id:03d}. "
        f"Follow the existing format exactly. Write the file."
    )
    log_path = args.log_dir / loop_name(loop_id) / "promote.log"
    code, _ = run_command(claude_command(prompt), prompt, 3600, log_path, args.dry_run)
    if code != 0:
        print(f"[warn] promote step failed for loop {loop_id:03d}; see {log_path}")


# ── Phase transition ──────────────────────────────────────────────────────────
def next_phase(phase):
    idx = PHASES.index(phase)
    return "complete" if idx == len(PHASES) - 1 else PHASES[idx + 1]


# ── Main loop (single iteration) ─────────────────────────────────────────────
def run_once(state, workspace):
    loop_id = int(state.get("current_loop") or state["next_loop"])
    if loop_id > int(state["target_loop"]):
        return False   # all loops done

    phase = state["phase"]
    if phase == "complete":
        update_state(..., last_completed_loop=loop_id,
                     next_loop=loop_id+1, current_loop=None, phase="plan")
        return True

    ensure_loop_dirs(workspace / "loops", loop_id)
    update_state(..., current_loop=loop_id, phase=phase)

    # In the skill, this is replaced by spawning an Agent for each phase.
    run_phase_via_agent(workspace, loop_id, phase)

    # After reflect: parse verdict and optionally promote
    if phase == "reflect":
        output = read_phase_record(workspace, loop_id, phase)
        verdict = parse_verdict(output)
        print(f"reflect verdict: {verdict}")
        if verdict == "accept":
            _run_promote(args, loop_id)
        update_state(..., last_verdict=verdict)

    update_state(..., phase=next_phase(phase))
    return True
```
