# Filetree Rules

Use this reference before adding, moving, or removing files in this skill.

## Layout

```text
skills/engineer/perf_engineer/nvidia_gpu_profiler/perf-nsight-compute-analysis/
├── SKILL.md
├── STATE.md
└── references/
    ├── advanced-profiling.md
    ├── bottleneck-guide.md
    ├── cli-reference.md
    ├── memory-analysis.md
    ├── metrics-guide.md
    ├── python-report-api.md
    ├── roofline-analysis.md
    ├── sections-guide.md
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
