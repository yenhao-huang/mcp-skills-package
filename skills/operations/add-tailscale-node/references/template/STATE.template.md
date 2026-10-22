# Add Tailscale Node State

Run ID:
Instance:
Started:
Scope:
Inventory path:
Resolved home endpoint and configuration source:

Last updated: 1970-01-01T00:00:00Z

| Step | Status | Evidence | Notes |
| --- | --- | --- | --- |
| 0. Define Scope | pending |  |  |
| 1. Inspect Environment | pending |  |  |
| 2. Install Or Uninstall | pending |  |  |
| 3. Configure Connectivity | pending |  |  |
| 4. Validate Result | pending |  |  |
| 5. Handoff | pending |  |  |

For home multi-node runs, add one row per approved node. Keep each direction
pending until tested from its actual source; an offline node is not a success.

| Node / Tailscale ID | SSH key fingerprints | Home -> node | Node -> home | Verified at | Managed changes / rollback |
| --- | --- | --- | --- | --- | --- |

## Required connectivity evidence

Enrollment result / node ID / addresses:
Resolved peer and configuration source:
Required application, accounts and ports:

| Direction | Source -> destination / account / port | Result (passed / failed / untested) | Command, exit status and identity evidence | Observed cause or unknown | Next action / missing access |
| --- | --- | --- | --- | --- | --- |
| Peer -> node | | untested | | | |
| Node -> peer | | untested | | | |

Keep overall connectivity incomplete until all required directions pass.
Never store secrets or credential-bearing login URLs here.
