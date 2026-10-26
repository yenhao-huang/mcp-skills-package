# ExecuTorch Result

批次：<NNNNNN_YYYY-MM-DD_HHmmss>
報告日期：<YYYY-MM-DD Asia/Taipei>
更新時間：<YYYY-MM-DD HH:mm:ss Asia/Taipei>
選擇紀錄：尚未選擇；等待用戶從 issue-disptach.pdf 指定議題。

| 選擇的 issue | 選擇 issue | issue 開發 | 用戶在社群寄送 PR | 該 PR 被 merge | 目前社群 CI 情況 |
| --- | --- | --- | --- | --- | --- |

只在用戶實際選定後加入資料列，不把候選自動視為已選。
四個進度欄只填「未開始／進行中／完成／受阻／待確認」，不增加其他階段。

- 選擇 issue：用戶明確選定後標記完成，記錄選擇時間與來源。
- issue 開發：涵蓋重現、修正、測試及個人 fork PR。必要驗證通過且修正可供用戶提交時才標記完成；fork PR 不代表已送出社群 PR。
- 用戶在社群寄送 PR：只在唯讀確認用戶已提交對應社群 PR 後標記完成；技能不得代送。
- 該 PR 被 merge：只依該社群 PR 的 mergedAt／merged 狀態標記完成。closed 不等於 merged；個人 fork PR 合併也不算。

「目前社群 CI 情況」只放目前社群 PR 的 CI 摘要，使用以下單行格式；日期為 Asia/Taipei。
保留使用者指定的 `CI sucess` 拼字。

```text
<YYYY/MM/DD>; CI fail: <count>; CI sucess: <count>; Require fix: <yes/no>; Evidence: <失敗 job／log 連結、關鍵錯誤與是否由本次 fix 造成的證據>
```

統計單位為 workflow：同一社群 PR 的目前 head，每個 workflow/event 只計最新
run／attempt；不可混入舊 head、過期重跑或把 matrix job 再重複計數。讀完所有頁面。
尚未完成、skipped、cancelled、action_required 等不算 success，必要時在 Evidence
簡述。每個失敗 workflow 仍須查到實際失敗 job 才能判斷根因。

- `yes`：至少一個失敗有證據顯示與我們的 fix 有關，列出應修正之處。
- `no`：已確認目前無失敗，或所有失敗都有證據顯示與 fix 無關；列出根據。
- 證據不足、仍在執行、缺 log／權限時，例外填 `unknown` 並寫明限制；不可硬填 no。
- 尚無社群 PR 時 counts 與 Require fix 填 `n/a`；Evidence 說明未提交，不拿 fork CI 代替。

新出現或尚未檢查的失敗，依 skill 的 `references/ci-triage.md` 唯讀調查並記錄。
已查過且身份與錯誤未變者沿用有日期的證據；新 head、attempt 或錯誤須重新核對。
同一 PR 也在下方追蹤表時，摘要與判斷必須一致，不在此欄重複貼開發歷史。
社群 issue／PR 連結一律用 redirect.github.com。讀取失敗標示待確認，不清除既有事實。

## PR 追蹤表

| 追蹤項目 | 社群 PR | 進度 | 目前狀況／下一步 | 查核時間 |
| --- | --- | --- | --- | --- |

已選 issue 的「追蹤項目」完整沿用上表「選擇的 issue」的名稱、編號與連結，順序相同。僅追蹤、未選定的 PR 接續列在後面，不因此新增選題或刪除追蹤列。

進度只使用「未發 PR／PR 未 merge／Done」。Done 必須確認該社群 PR 已 merge；closed 未 merge 仍是 PR 未 merge，原因記在目前狀況。用戶指定追蹤的 PR 可以不在本批候選內，追蹤不代表選題或授權開發。

每日建立當日快照，即使狀態未變。延續先前選題與追蹤列；同日重跑更新當日檔案，保留過往日期。

<!-- 歷史候選與排程執行紀錄僅存內部 STATE.md／cron logs，不輸出到 Result.md。 -->
