# Dedicated runtime

Requirements: Python 3.12+, Git, uv. No global package installation, Docker or web services are needed. The helper provisions a Python 3.12 `.venv` and the upstream checkout at fixed commit `d0d66d62fae2b7cc9fb0fb814df3403397ae8831` in a **new**, dedicated workspace. It installs upstream harness/extension-api dependencies plus PyMuPDF 2.0; transitive dependency versions are resolved at install time, not claimed as a frozen cross-platform lock.

Before running dependency installation, tell the user if no suitable environment exists. Use an already available system Python to provision it:

```text
python <skill-dir>/references/scripts/setup_runtime.py install --workspace <new-runtime-dir>
```

Installation writes only `<runtime>/.start-deer-runtime.json`, `<runtime>/external/deer-flow` and `<runtime>/.venv`. Success requires actual DeerFlow/PDF imports. An installation failure retains its marker for diagnosis; it is not silently overwritten on retry. `--upstream-source` supports a local Git mirror for offline testing; the commit remains fixed.

Then run the launcher with `<runtime>/.venv/Scripts/python.exe` on Windows or `<runtime>/.venv/bin/python` on POSIX. Pass `--framework-root <runtime>` or set `DEER_RESEARCH_ROOT`. Existing research-project runtimes can be used explicitly without reprovisioning. The skill's integration modules are bundled; `core/` from a separate project is not required.

Authentication: normal Codex login, optionally located with `CODEX_AUTH_PATH`. The upstream provider reads it directly. `RESEARCH_MODEL` overrides the model. If a model is rejected, inspect available model information rather than inventing access or endlessly retrying. API mode reads `RESEARCH_API_KEY` (or `OPENAI_API_KEY`), `RESEARCH_MODEL` (or `OPENAI_MODEL`) and optional `RESEARCH_BASE_URL` (default official OpenAI API URL) from the supplied env file.

## Roll back this runtime

For a directory created by this helper:

```text
python <skill-dir>/references/scripts/setup_runtime.py remove --workspace <same-runtime-dir>
```

The helper validates the ownership marker, checks for unrelated files and checkout changes, rejects linked/junction roots and removes only the managed runtime. It refuses unmarked existing installations. Keep papers and results **outside** this directory; move user-created files out before removal if it refuses. A subsequent install into the now-absent directory provisions from scratch. Do not delete a reused runtime belonging to another project.

This rollback removes runtime files only. It does not alter Codex credentials, shared uv caches, original PDFs, research jobs elsewhere or already transmitted provider requests. Research jobs are retained intentionally; removing them is a separate user-directed file operation.

## Offline verification

Run `references/scripts/test_start_deer.py` using the runtime Python. Set `START_DEER_TEST_RUNTIME` to the runtime root to include real single/multi DeerFlow protocol jobs; otherwise those two tests are explicitly skipped. `START_DEER_TEST_TEMP` optionally selects a writable directory for disposable synthetic PDFs/jobs. No real papers, credentials or provider calls are required.

For changes to provisioning, validate in a disposable workspace: install, run the offline tests, remove, assert the runtime is absent and a neighboring sentinel is unchanged, install again and rerun the tests. Record the actual commands and results in STATE.md. Do not use an existing user environment as the rollback target.
