# Agents Local Setup

這個目錄保存本機 agent 相關設定，主要包含：

- `skills/`: 本機可用的 agent skills。
- `hooks/`: agent hook 腳本。
- `.skill-lock.json`: skills CLI 的安裝紀錄，目前只記錄 `find-skills` 來源。

## Skills

目前 `skills/` 底下有下列 skills。

| Skill | 路徑 | 用途 |
| --- | --- | --- |
| `claude-sandbox` | `skills/claude-sandbox/SKILL.md` | 建立、啟動或進入 Claude Code Docker sandbox，並使用 `bypassPermissions` 模式。 |
| `codex-sandbox` | `skills/codex-sandbox/SKILL.md` | 建立、更新或執行 Codex sandbox；以 bundled `src/` 為 Dockerfile 與腳本來源。 |
| `dev` | `skills/dev/SKILL.md` | 軟體開發、除錯、測試、重構、benchmark 或實驗工作；要求先讀 `references/convention.md`。 |
| `find-skills` | `skills/find-skills/SKILL.md` | 協助搜尋、挑選、安裝 open agent skills ecosystem 的 skills。 |
| `loop-analysis` | `skills/loop-analysis/SKILL.md` | 針對 ESG contest agent-loop runs 產出固定格式的繁中 markdown 分析。 |
| `mcp-init` | `skills/mcp-init/SKILL.md` | 初始化或修復 Codex MCP 設定，包含 Jina、Firecrawl、Hugging Face、Git MCP。 |
| `notion` | `skills/notion/SKILL.md` | 管理常用 Notion pages、資料庫、頁面 registry、摘要與更新流程。 |
| `sandox-tutorial` | `skills/sandox-tutorial/SKILL.md` | 記錄 skill、MCP、AGENTS.md 等安裝與設定筆記。 |
| `skill-template` | `skills/skill-template/SKILL.md` | 建立新 Codex skill 時使用的模板與工作流程。 |
| `vllm-embedding-server` | `skills/vllm-embedding-server/SKILL.md` | 啟動、除錯、驗證本機 vLLM embedding server，特別是 Qwen embedding models。 |

### 使用原則

- 每個 skill 的觸發條件與工作流程以各自的 `SKILL.md` 為準。
- `dev` skill 對開發任務有全域約束：修改前要讀 `skills/dev/references/convention.md`，並以 design / develop / test 流程處理。
- `find-skills` 是目前 `.skill-lock.json` 中唯一有安裝來源紀錄的 skill，來源為 `vercel-labs/skills`。

## Deprecated Skills

下列 skills 已移出 active `skills/` 清單，保留在 `skills/deprecated/` 作為歷史或參考資料。

| Skill | 路徑 | 狀態 |
| --- | --- | --- |
| `codex-review` | `skills/deprecated/codex-review/SKILL.md` | 已停用，不再作為目前 active skill 觸發。 |

## Hooks

目前 `hooks/` 底下有一支 hook 腳本。

| Hook | 路徑 | 事件 | 用途 |
| --- | --- | --- | --- |
| `check_session_size.py` | `hooks/check_session_size.py` | `UserPromptSubmit` | 讀取目前 transcript JSONL，檢查最近一次 assistant usage 的有效 context token 數；超過門檻時提醒使用者先執行 `/compact`。 |

### `check_session_size.py`

行為摘要：

- 從 stdin 讀取 hook payload。
- 使用 payload 內的 `transcript_path` 找到 transcript JSONL。
- 讀取最近一次 assistant message 的 `usage`。
- 將下列 token 數相加作為有效 context size：
  - `input_tokens`
  - `cache_creation_input_tokens`
  - `cache_read_input_tokens`
- 若總數超過門檻，輸出 hook response。

可用環境變數：

| 變數 | 預設值 | 說明 |
| --- | --- | --- |
| `COMPACT_THRESHOLD` | `500000` | 超過此 token 數時觸發提醒。 |
| `COMPACT_HARD_BLOCK` | unset | 設為 `1` 時改為 block prompt，要求先 `/compact`。 |

預設模式不是 hard block，而是回傳 `hookSpecificOutput.additionalContext`，要求 agent 停下來並提醒使用者執行 `/compact`。

## 目錄概覽

```text
.
├── hooks/
│   └── check_session_size.py
├── skills/
│   ├── claude-sandbox/
│   ├── codex-sandbox/
│   ├── dev/
│   ├── find-skills/
│   ├── loop-analysis/
│   ├── mcp-init/
│   ├── notion/
│   ├── sandox-tutorial/
│   ├── skill-template/
│   ├── vllm-embedding-server/
│   └── deprecated/
│       └── codex-review/
└── .skill-lock.json
```
