# Add Tailscale Node State

Run ID: issue-86-home-public-key
Instance: documentation change
Started: 2026-10-22
Scope: Embed approved default home SSH public key; issue #86.
Inventory path:
Resolved home endpoint and configuration source:

Last updated: 1970-01-01T00:00:00Z

| Step | Status | Evidence | Notes |
| --- | --- | --- | --- |
| 0. Define Scope | completed | Issue #86; explicit user approval | |
| 1. Inspect Environment | completed | Existing skill, references, layout and repository instructions reviewed | |
| 2. Install Or Uninstall | skipped | Documentation-only change | No live lifecycle mutation |
| 3. Configure Connectivity | completed | Embedded approved public key, fingerprint, override rules, verified source restriction and scoped rollback | Instructions only |
| 4. Validate Result | blocked | Generic quick_validate.py passed; required layout checked; key fingerprint verified | Disposable SSH add -> rollback -> add and real-source login not run |
| 5. Handoff | pending | PR for issue #86 | Awaiting review and merge |

For home multi-node runs, add one row per approved node. Keep each direction
pending until tested from its actual source; an offline node is not a success.

| Node / Tailscale ID | SSH key fingerprints | Home -> node | Node -> home | Verified at | Managed changes / rollback |
| --- | --- | --- | --- | --- | --- |
