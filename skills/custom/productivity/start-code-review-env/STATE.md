# Start code review environment state

Run: 2026-10-19 home-aware routing, issue #64
Instance: Codex on the PRetrieval remote node
Scope: resolve home from add-tailscale-node; open locally on home or via SSH from a remote node.
Issue: https://github.com/yenhao-huang/mcp-skills-package/issues/64
Implementation: completed
Validation: completed for changed instructions, registry and workspace generation;
full cross-platform GUI deployment validation remains untested.
Publication: pending PR review/merge; no main-branch completion claimed.

## Changes

- Home identity/account/port now come from add-tailscale-node and the selected
  inventory. Optional desktop.json is a verified cache, not a prerequisite.
- Compare the current machine with home before choosing direct desktop launch
  or SSH transport. Preserve Windows Interactive/Limited and macOS owner checks.
- Correct the PRetrieval project alias and verify equivalent aliases on home.
- Remove fixed headless/unconfigured assumptions; record routing and connection
  evidence separately from visual GUI verification.

## Validation evidence

- `/opt/python/bin/python3 /home/howard/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/custom/productivity/start-code-review-env`: passed.
  System python3 lacked PyYAML; reused existing /opt/python (PyYAML 6.0.3),
  installed no dependencies.
- Required skill layout, category, Workflow section and add-tailscale-node
  relative link checked: passed.
- Python standard-library subprocess smoke checks of open_workspace.py: corrected
  PRetrieval default and URI, unchanged ExecuTorch default, verified host override,
  space-containing path as one argv element, relative/traversal rejection, and
  refusal to overwrite a different existing workspace: passed.
- Isolated temporary workspace create -> unlink only generated workspace ->
  recreate: passed, identical contents restored. No desktop windows opened by
  these validation checks.
- `git diff --check`: passed.

## Existing live evidence and limits

Earlier in this conversation the user-confirmed home account successfully ran
an Interactive/Limited Windows task; exit 0/Ready was observed and only that task
was removed. Remote SSH initially timed out, then resolved the same window's
project authority; workspace metadata identified the requested PRetrieval folder.
Evidence is stored locally in /tmp/start-code-review-env-64bo91dl/.
This is not a screenshot, a repeated desktop launch lifecycle, or a macOS/direct
home validation. This documentation update does not reinstall services, change
SSH credentials, or reopen/close the user's current windows for testing.
