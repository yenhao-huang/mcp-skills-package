# Create Skill State

This file is a reusable per-run template. Copy it to `STATE.md` before starting
a new execution.

Run ID: issue-76-content-producer
Instance: content-producer integration
Started: 2026-10-20T08:44:42.300120+00:00
Scope: Shared Humanizer/frontend-slides and both PM prose workflows.

Last updated: 2026-10-20T08:44:42.300120+00:00

| Step | Status | Evidence | Notes |
| --- | --- | --- | --- |
| 0. Define Scope | completed | GitHub issue 76; user requested content-producer and both PM integrations. | |
| 1. Read Relevant Context | completed | AGENTS.md, skill-create rules, upstream licenses, PM contracts and renderer inspected. | |
| 2. Execute Workflow | completed | Shared skills, PM integration and catalog; source provenance retained. | No live deployment. |
| 3. Validate Result | completed | Four generic validators and required-layout/link checks passed; 80 moved frontend vendor files and the Humanizer guide match source bytes; flat dependency resolution and success/empty/failure report checks passed; 15 PRetrieval tests passed; shell/JS syntax checks passed. | Browser smoke unavailable: missing libglib. |
| 4. Handoff Summary | in_progress | Issue 76; preparing linked PR. | Merge requires authorization per AGENTS.md. |
