# Filetree Rules

Use this reference before adding, moving, or removing files in this skill.

## Layout

```text
skills/engineer/perf_engineer/nvidia_gpu_profiler/perf-nsight-systems/
├── SKILL.md
├── STATE.md
└── references/
    ├── app-preparation.md
    ├── cli-post-collection.md
    ├── cli-profiling.md
    ├── expert-systems.md
    ├── nvtx-analysis.md
    ├── recipes-dl.md
    ├── stats-reports.md
    ├── provenance.md
    ├── rules/
    │   ├── env.md
    │   ├── filetree.md
    │   └── state-rules.md
    └── template/
        └── STATE.template.md
```

## Rules

- Topic references under `references/*.md` are vendored from upstream; see
  `references/provenance.md` and record every local change there.
- Keep repo-local operating rules in `references/rules/` and state templates in
  `references/template/`.
- Do not add README, changelog, `agents/`, or top-level `scripts/` files.
- Do not commit generated profile reports or `__pycache__/`.
