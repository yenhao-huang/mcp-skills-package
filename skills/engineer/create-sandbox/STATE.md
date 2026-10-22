# Create Sandbox State

Run ID: 20261022-sandbox-template-references
Instance: /home/howard/mcp-skills-package/skills/engineer/create-sandbox
Started: 2026-10-22T08:43:11.678Z
Scope: Normalize create-sandbox templates under references/template and add a second AGENTS.md line requiring dev and Git skills.

Last updated: 2026-10-22T08:43:11.678Z

| Step | Status | Evidence | Notes |
| --- | --- | --- | --- |
| 0. Define Scope | completed | User requested plural references/template path and a second agent instruction line. | Keep existing global-only configuration. |
| 1. Read Relevant Context | completed | Read skill-create workflow/layout/state rules, create-sandbox workflow/lifecycle/layout/state rules, current templates, and bootstrap template lookup. | Existing installer already supports multiline templates. |
| 2. Execute Workflow | completed | Moved AGENTS.md/CLAUDE.md into references/template, updated bootstrap TEMPLATE_DIR, skill/lifecycle/filetree references, and appended the second dev/Git guidance line. | Original repository-reading line and global-only setup preserved. |
| 3. Validate Result | completed | Mocked-Docker fresh install, rerun, existing-global upgrade preservation, exact two/one template lines, and install/remove/reinstall passed. Shell syntax, generic skill validation, old active-path search, and git diff --check passed. | No actual Docker build or running-container mutation. |
| 4. Handoff Summary | completed | Published cd6f009 and created/read back https://github.com/yenhao-huang/mcp-skills-package/pull/96, linked to issue #95. | PR open; review/merge and main verification pending. |
