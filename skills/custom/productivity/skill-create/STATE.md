# Create Skill State

Run ID: 20261110-nvidia-gpu-profiler-skills
Instance: `skills/engineer/perf_engineer/nvidia_gpu_profiler/{perf-nsight-systems,perf-nsight-compute-analysis}`
Started: 2026-11-10T00:00:00Z
Scope: Vendor NVIDIA's Apache-2.0 `perf-nsight-systems` (nsys) and `perf-nsight-compute-analysis` (ncu) skills from NVIDIA/TensorRT-LLM@34e19b3 into a new `engineer/perf_engineer/nvidia_gpu_profiler` group (issue #116).

Last updated: 2026-11-10T00:00:00Z

| Step | Status | Evidence | Notes |
| --- | --- | --- | --- |
| 0. Define Scope | completed | User requested adding both skills to `engineer/perf_engineer/nvidia_gpu_profiler/`; issue #116 defines acceptance criteria. | Upstream pinned to commit `34e19b3365e3b59fb00c924cbb1dc3ceb195f842`. |
| 1. Read Relevant Context | completed | Read repo AGENTS.md, skill-create SKILL.md, and categories/filetree/workflow/env/state-rules references on `origin/main`; scanned upstream content for unsafe commands. | Upstream content is generic nsys/ncu guidance; nothing in it is TensorRT-LLM-specific. |
| 2. Execute Workflow | completed | Copied all 17 upstream files; added STATE.md, references/provenance.md, references/rules/{env,filetree,state-rules}.md, and references/template/STATE.template.md per skill; registered the group in categories.md and filetree.md. | SKILL.md edits: `## Local Rules` section; nsys `## Workflows` → `## Workflow` plus an ordered dispatcher; ncu frontmatter `tags`/`compatibility` moved under `metadata`. All edits are listed in provenance.md. |
| 3. Validate Result | completed | `quick_validate.py` printed `Skill is valid!` for both skills; required-file check, one `## Workflow` heading each, globally unique `name:`, and `git diff --cached --check` passed. | No install/rollback lifecycle is added, so the reversibility check does not apply. |
| 4. Handoff Summary | blocked | Local commit on branch `feat/116-nvidia-gpu-profiler-skills`. | `git push` was denied by the session permission policy, so no PR exists yet. Completion requires push, a PR linked to #116, merge, and verification on `main`. |
