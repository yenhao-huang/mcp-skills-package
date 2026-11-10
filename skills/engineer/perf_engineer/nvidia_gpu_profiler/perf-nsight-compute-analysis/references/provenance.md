# Provenance

- Upstream: https://github.com/NVIDIA/TensorRT-LLM/tree/34e19b3365e3b59fb00c924cbb1dc3ceb195f842/.claude/skills/perf-nsight-compute-analysis
- Upstream commit: `34e19b3365e3b59fb00c924cbb1dc3ceb195f842`
- Author: NVIDIA Corporation
- License: Apache-2.0 (https://www.apache.org/licenses/LICENSE-2.0)
- Imported: 2026-11-10 (issue #116)

## Unmodified Upstream Files

- `references/advanced-profiling.md`
- `references/bottleneck-guide.md`
- `references/cli-reference.md`
- `references/memory-analysis.md`
- `references/metrics-guide.md`
- `references/python-report-api.md`
- `references/roofline-analysis.md`
- `references/sections-guide.md`

## Local Modifications

- `SKILL.md`: added a `## Local Rules` section that points to the repo-local
  rules and state files. The upstream `## Workflow` section is unchanged.
- `SKILL.md` frontmatter: moved the top-level `tags` and `compatibility` keys
  under `metadata` to pass the repo validator. The values are unchanged.
- Added repo-local layout files: `STATE.md`, `references/provenance.md`,
  `references/rules/{env,filetree,state-rules}.md`, and
  `references/template/STATE.template.md`.

## Updating

Re-download the upstream directory at a newer commit, re-apply the local
modifications above, and update the commit hash in this file.
