# Provenance

- Upstream: https://github.com/NVIDIA/TensorRT-LLM/tree/34e19b3365e3b59fb00c924cbb1dc3ceb195f842/.claude/skills/perf-nsight-systems
- Upstream commit: `34e19b3365e3b59fb00c924cbb1dc3ceb195f842`
- Author: NVIDIA Corporation
- License: Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0)
- Imported: 2026-11-10 (issue #116)

## Unmodified Upstream Files

- `references/app-preparation.md`
- `references/cli-post-collection.md`
- `references/cli-profiling.md`
- `references/expert-systems.md`
- `references/nvtx-analysis.md`
- `references/recipes-dl.md`
- `references/stats-reports.md`

## Local Modifications

- `SKILL.md`: added a `## Local Rules` section that points to the repo-local
  rules and state files. Renamed `## Workflows` to `## Workflow` and added an ordered dispatcher; the upstream Workflows 1-5 are unchanged as subsections.
- Added repo-local layout files: `STATE.md`, `references/provenance.md`,
  `references/rules/{env,filetree,state-rules}.md`, and
  `references/template/STATE.template.md`.

## Updating

Re-download the upstream directory at a newer commit, re-apply the local
modifications above, and update the commit hash in this file.
