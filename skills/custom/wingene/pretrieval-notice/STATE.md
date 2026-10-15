# pretrieval-notice State

Run ID: w78-daily-38-20261015
Instance: /root
Started: 2026-10-15 Asia/Taipei
Scope: GitHub issue #38; daily 08:30 W78 scheduler, fixed Markdown report and daily repository publication.

| Step | Status | Evidence |
| --- | --- | --- |
| Context and issue | completed | App project identifies w78_pretrieval_tailscale at /; Docker daemon runs in this sandbox; issue #38 created; isolated agent/fix-38 worktree. |
| Implement | completed | Fixed report.template.md, notice.render, publish.py, Dockerfile and Compose definition. |
| Validate | completed | 15 unittest tests passed; generic skill validator and git diff --check passed. Isolated Compose install -> down -> fresh-state install passed with live queries and healthy next_run; test resources removed. |
| Deploy | completed | W78 service pretrieval-notice-notice-1 healthy, restart unless-stopped; first report https://github.com/yenhao-huang/daily/blob/main/wingene/pretrieval/2026-10-15_105933.md verified by fresh clone. Next run 2026-10-16 08:30 Asia/Taipei. |
| Deliver | in_progress | Preparing issue #38 PR; deployment is active, repository merge still pending. |

## Validation commands and lifecycle evidence

- `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s skills/custom/wingene/pretrieval-notice/references/scripts -p 'test_*.py' -v`: 15 passed.
- `/data/finetune_env/bin/python /home/howard/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/custom/wingene/pretrieval-notice`: valid.
- Compose file: `references/deploy/docker-compose.yml`; test project `pretrieval-notice-lifecycle`, env `/data/deployments/pretrieval-notice/lifecycle.env`, isolated state `lifecycle-state`.
- First `up -d --wait`: healthy; live Gitea query returned 8 open howard issues; GitHub `ls-remote` succeeded.
- `down --remove-orphans`: Docker container/network label queries returned empty; external state retained.
- Renamed first scheduler state, repeated `up -d --wait`: healthy; live query succeeded; fresh next_run 2026-10-16T08:30:00+08:00.
- Final test `down`: test resources absent. Production uses separate `state`, project `pretrieval-notice`, and a stable skill copy under `/data/deployments/pretrieval-notice/skill`.
- Production `publish.py once`: remote report verified, no pending payload; operational JSON state remains outside Git.
