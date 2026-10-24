# Start Deer State

Run ID: publish-start-deer-20261024
Instance: skills/custom/productivity/start-deer
Started: 2026-10-24
Scope: Publish a portable DeerFlow paper-research skill. Issue: https://github.com/yenhao-huang/mcp-skills-package/issues/102

| Step | Status | Evidence |
| --- | --- | --- |
| 0. Define Scope | completed | User requested publication in yenhao-huang/mcp-skills-package; issue #102 defines acceptance. |
| 1. Read Relevant Context | completed | Read current AGENTS.md and skill-create category, filetree, workflow, environment and state rules; base main, branch feat/start-deer-paper-research. |
| 2. Execute Workflow | completed | Bundled corpus/runner/renderer, portable launcher and managed runtime install/remove helper; no local papers, auth state or absolute user paths. |
| 3. Validate Result | completed | Generic validator, Ruff and diff checks passed. Eight offline synthetic tests passed on the first fresh runtime (30.338s) and again after removal/reinstall (25.233s); both include real single/multi DeerFlow graphs. |
| 4. Handoff Summary | in_progress | Prepare focused commit and PR linked to #102; merging into main requires maintainer authorization. |

## Runtime lifecycle evidence

Isolated target: `.runtime/start-deer-validation/runtime` on Windows/Python 3.12.13. Source was the existing local upstream Git mirror at the fixed revision; dependencies used the existing uv cache. No model API calls or original research papers were needed.

1. `python references/scripts/setup_runtime.py install --workspace <target> --upstream-source <local-mirror>` completed; marker ready, upstream fixed SHA and real factory/PDF imports passed. Running `test_start_deer.py` with `START_DEER_TEST_RUNTIME=<target>` passed all eight tests.
2. `python references/scripts/setup_runtime.py remove --workspace <target>` completed; target absence and an unchanged sentinel alongside the runtime were asserted. The helper refused unmarked or unrelated-file targets in the test suite.
3. The same install command recreated the previously absent target; imports and all eight offline tests passed again. Logs are in the local ignored `.runtime/start-deer-validation/` directory. No runtime files, PDFs, credentials or generated reports are staged.

Validation command: `<runtime-python> references/scripts/test_start_deer.py`, with `START_DEER_TEST_RUNTIME` and a writable `START_DEER_TEST_TEMP`. Each synthetic job was launched from a different cwd. Linux/macOS execution and live research quality were not retested for this publication.
