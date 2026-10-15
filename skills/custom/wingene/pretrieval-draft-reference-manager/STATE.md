# Draft Reference Manager State

Run ID: issue-43-frontend-skill
Instance: W78 (192.168.1.78), existing draft-reference A/B
Started: 2026-10-15 Asia/Taipei
Scope: Add matching frontends; document deployment and mount paths.
Issue: https://github.com/yenhao-huang/mcp-skills-package/issues/43
Branch: agent/fix-43

| Step | Status | Evidence |
| --- | --- | --- |
| Context | completed | Read repository/skill rules; verified A/B receipts, live mounts and free ports 28179/28279. |
| Implementation | completed | Frontend-only Compose helper, topology/mount/version/lifecycle guides, required layout and README entry. |
| Runtime validation | completed | A and B install → remove only frontend → reinstall passed; homepage, JS/CSS, proxied API health and nginx config verified. |
| Local validation | completed | 12 stdlib unit tests, generic skill validator, required files and relative Markdown links passed. Independent four-scenario review findings fixed and re-review converged. |
| Delivery | in_progress | [PR #44](https://github.com/yenhao-huang/mcp-skills-package/pull/44) opened from agent/fix-43 to main; publication on main awaits merge authorization. |

## Runtime evidence

Core/frontend source: `42378d059669b8297390151fe71c871791c2628d`.
Frontend image: `sha256:780674e82c8d96c7043ea82038f932cac17b1b4a3570a3b640fd3ced3c19c64a`.
A: http://192.168.1.78:28179 → API 28178.
B: http://192.168.1.78:28279 → API 28278.

W78 evidence directory: `/mnt/share_data_78/howard/data/deployments/issue-708/`:
`frontend-build.log`, `frontend-image.json`, `frontend-acceptance.json`.
Per-instance frontend files: `../pretrieval-draft-reference-{a,b}/frontend/`.
The runtime evidence records different first/second frontend container IDs and
verifies every preexisting running container retained its ID and StartedAt.

Commands exercised on each frontend-only Compose: `config --quiet`,
`up -d --wait --pull never`, `down`, `up -d --wait --pull never`, and `nginx -t`.
External LAN requests also returned 200: `/`, `/assets/index-CSKSU_IQ.js`
(application/javascript), `/assets/index-l0CMOtf2.css` (text/css), `/api/health`
(application/json, status ok). No API/database/shared service restart occurred.

Local commands:

```bash
python3 -B -m unittest discover -s skills/custom/wingene/pretrieval-draft-reference-manager/references/scripts -p 'test_*.py' -v
/opt/python/bin/python /home/howard/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/custom/wingene/pretrieval-draft-reference-manager
git diff --check
```

## Limits

Existing core A/B were retained; this run does not claim a new core deployment
lifecycle, database version rollback, heavy concurrent benchmark, or full-corpus
Drone run. Prior #709 concurrency/readiness/template/cleanup findings remain
explicitly documented, not repaired by this frontend/skill task. Permanent data
deletion is irreversible and requires the requested instance scope.

Final helper was also exercised against both live instances: actual frontend/API
image provenance passed; existing frontends were correctly rejected without writes.
