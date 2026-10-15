# Daily schedule

- Name: PRetrieval 未關閉 issue 提醒
- Timezone: Asia/Taipei
- Time: 04:00 every day
- Local cron equivalent: `0 4 * * *` in Asia/Taipei (20:00 UTC previous day).
- Delivery: the user's automation task/chat notification surface.
- Runtime: a host that can reach the internal Gitea server and use the user's
  existing Git credential helper and persistent preferences file.

## Prompt

```text
使用 $pretrieval-notice，查詢 leo/PRetrieval 指派給 howard 的所有未關閉 issue（排除 PR），以繁體中文通知我。讀取持久保存的優先順序，將我指定重要的 issue 依指定順序排最上面並標示「重要」，其餘依編號由新到舊。包含台北查詢時間、總數、每筆編號、標題及連結。每天都要回報，即使內容未變；沒有 issue 時明確說明。認證或連線失敗時回報原因，不得當作沒有 issue，也不得使用舊資料假裝成功。不修改 Gitea 資料。
```

Use the app's supported automation tools, searching for `automation_update`
first. Inspect existing automations and reuse a matching task instead of
creating duplicates. Use the tool schema's schedule and timezone fields;
read back its ID, active status, next run, runtime, and prompt before claiming
it is enabled. Record those values in local STATE.md.

If the tool is unavailable, report that scheduling is not enabled and provide
this prepared prompt and time. Do not silently substitute a session-start
hook (it does not guarantee 04:00 execution), OS cron, email, or a hosted task
that cannot access the private LAN.
