# Create Skill State

This file is a reusable per-run template. Copy it to `STATE.md` before starting
a new execution.

Run ID: executorch-branch-naming-20261106
Instance: skill-branch-naming
Started: 2026-11-06T07:05:21.819929+00:00
Scope: Require fix/<issue-id>-<short-description> for ExecuTorch development branches.

Last updated: 2026-11-06T07:09:17.544153+00:00

| Step | Status | Evidence | Notes |
| --- | --- | --- | --- |
| 0. Define Scope | completed | User requested naming rule and migration of agent/fix branches. | Local changes authorized. |
| 1. Read Relevant Context | completed | Read package README, AGENTS.md, skill-create, skill-creator, and executorch-dev policies. | Open PR source renaming closes PRs per GitHub documentation. |
| 2. Execute Workflow | completed | Source and installed Codex/Claude entrypoints now require fix/<issue-id>-<short-description>; local issue branches renamed with HEAD/diff/untracked-content preservation verified. | Local scope only; legacy remote PR heads preserved. |
| 3. Validate Result | completed | quick_validate.py passed for source, Codex and Claude copies using /data/venv_et_batch2026/bin/python; git diff --check passed; existing required layout retained. | /opt/python lacked PyYAML; no packages installed. No runtime installation workflow added. |
| 4. Handoff Summary | in_progress | User explicitly authorized skill publication; issue https://github.com/yenhao-huang/mcp-skills-package/issues/114 and PR https://github.com/yenhao-huang/mcp-skills-package/pull/115 verified open. Task branch push read back via git ls-remote. | Publication completed; source delivery awaits verified merge into main. Merge has not been authorized. Existing ExecuTorch remote branches and PRs remain unchanged. |
