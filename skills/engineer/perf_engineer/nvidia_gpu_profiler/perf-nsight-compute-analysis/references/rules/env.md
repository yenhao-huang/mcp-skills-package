# Environment Rules

Primary language: Markdown instructions; shell and Python commands run against the profiled workload
Runtime version: NVIDIA Nsight Compute CLI (`ncu`) from the installed CUDA Toolkit, or the binary in `$NCU`
Package manager: None for the skill itself; use the target project's `.venv` for any Python helpers
Frameworks: Optional Triton/cuTile/CuTeDSL JIT kernels; optional `ncu_report` Python module for programmatic analysis
Service manager: None
Required services: An NVIDIA GPU visible to the current environment

- Verify the tool with `ncu -v` before profiling. If it is missing, report it;
  do not install the CUDA Toolkit or Nsight packages without user approval.
- `ncu` may need `sudo`, `CAP_SYS_ADMIN`, or `--privileged` for GPU
  counters. Ask before escalating privileges or changing container
  capabilities or driver settings, such as non-admin counter access.
- Install optional Python dependencies only into the target project's `.venv`,
  never globally.
- Write profile reports (`.nsys-rep`, `.ncu-rep`, exports) into the target
  project or a scratch directory, not into this skill directory.
