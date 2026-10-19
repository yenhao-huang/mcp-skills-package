---
name: set-daily-cron
description: 設定、修改或檢查 Linux cron 定期執行 Codex 的任務，提供極簡定時範本。
---

## Workflow

1. 使用 [4 行 cron 範本](references/template/codex.cron)，修改使用者、專案目錄、時間與任務指令；任務邏輯放在指定 skill。
範本供 UTC 主機的 `/etc/cron.d/` 使用：每日 20:00 是台北次日 04:00，週日 20:00 是台北週一 04:00。
`danger-full-access` 沿用本容器已獲授權的設定；其他環境先確認使用者是否授權此權限範圍。保留共享鎖，避免 daily／weekly 同時寫入。
2. 安裝時取代同一任務的舊項目、不重複追加；確認工作目錄、登入與鎖目錄存在，並以 cron 環境實跑、核對遠端產出後才報成功。
僅維護舊的 do-cron-tasks hook 時讀取 [舊版設定](references/cron-config.md)。

回復時還原備份的原 cron 檔；首次安裝則移除該任務檔，保留其他排程。
