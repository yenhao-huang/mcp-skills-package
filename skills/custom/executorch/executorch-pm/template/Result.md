更新時間：<YYYY-MM-DD HH:mm:ss Asia/Taipei>

| 選擇的 issue | 選擇 issue | issue 開發 | 用戶在社群寄送 PR | 該 PR 被 merge | 目前社群 CI 情況 |
| --- | --- | --- | --- | --- | --- |

<!-- 以下為模板使用規則，產出報告時移除此說明區；首行只保留更新時間，不加標題、批次、報告日期或括號註記。 -->

不輸出「追蹤範圍與選擇紀錄」或「CI 判讀」等說明區段。
選題依據、停止追蹤決定與通用 CI 判讀規則保留在內部狀態／規則；
移除公開說明不代表重新啟用追蹤。

Result.md 恰有上方一張六欄表，不另加 PR 摘要表或三狀態進度欄。
以使用者指定的 [2026-11-06 版本](https://github.com/yenhao-huang/daily/blob/main/executorch/999976_2026-11-06_040301/Result.md)為結構範例，狀態與查核時間仍需每日重新確認。

只有用戶實際選定的議題才算選題，不把候選或僅追蹤 PR 自動視為已選。
四個進度欄以「未開始／進行中／完成／受阻／待確認」起首，可接精簡 PR 連結，例如：
`完成 · [PR 24122](https://redirect.github.com/pytorch/executorch/pull/24122)`、
`受阻 · [fork PR 45](https://github.com/yenhao-huang/executorch/pull/45)`。
不增加其他階段；個人 fork 連結放在 issue 開發欄。

- 選擇 issue：用戶明確選定後標記完成，記錄選擇時間與來源。
- issue 開發：涵蓋重現、修正、測試及個人 fork PR。必要驗證通過且修正可供用戶提交時才標記完成；fork PR 不代表已送出社群 PR。
- 用戶在社群寄送 PR：只在唯讀確認用戶已提交對應社群 PR 後標記完成；技能不得代送。
- 該 PR 被 merge：只依該社群 PR 的 mergedAt／merged 狀態標記完成。closed 不等於 merged；個人 fork PR 合併也不算。

「目前社群 CI 情況」只放目前社群 PR 的 CI 摘要，使用以下單行格式；日期為 Asia/Taipei。
保留使用者指定的 `CI sucess` 拼字。

```text
<YYYY/MM/DD>; CI fail: <count>; CI sucess: <count>; Require fix: <P(true)>% (true|false); Evidence: <一句原因／限制＋1–2 個證據連結>
```

統計單位為 workflow：同一社群 PR 的目前 head，每個 workflow/event 只計最新
run／attempt；不可混入舊 head、過期重跑或把 matrix job 再重複計數。讀完所有頁面。
尚未完成、skipped、cancelled、action_required 等不算 success，必要時在 Evidence
簡述。每個失敗 workflow 仍須查到實際失敗 job 才能判斷根因。

- 百分比是 executorch-dev 估計「我們的修改需要修正」為 true 的機率；不是 CI 通過率或實測統計。例：`Require fix: 20% (false)`。
- 大於 50% 傾向 true，小於 50% 傾向 false；不能填 unknown 或 50%。證據接近平衡時選 51%／49%，並註明低信心及缺口。
- 缺日誌或等待核准也要有暫定傾向，不能描述為已確認無關或 CI 通過。
- Evidence 只留一句主要原因／限制與 1–2 個連結；詳細三輪查核、反證與下一步留在內部記錄。
- 尚無社群 PR 時 counts 與 Require fix 填 `n/a`；Evidence 說明未提交，不拿 fork CI 代替。

新出現或尚未檢查的失敗，由 PM 交給 executorch-dev，依 `references/ci-triage.md` 執行至少三輪查核、反思與深入探索並記錄。
已查過且身份與錯誤未變者沿用有日期的證據；新 head、attempt 或錯誤須重新核對。
每項工作只在唯一表格呈現一次，不在 CI 欄重複貼開發歷史。
社群 issue／PR 連結一律用 redirect.github.com。讀取失敗標示待確認，不清除既有事實。

僅追蹤、未選題的 PR 放在已選議題之後，仍使用同一張表：
第一欄標示「僅追蹤 PR（未選題）」及 PR 名稱／編號／連結；
選擇 issue 填「未開始」，未經驗證的開發史填「待確認」，
社群提交與合併欄依唯讀查核證據填寫。追蹤不代表選題或授權開發。
保留已完成與已關閉未合併的 PR；closed 不等於 merged。

延續舊報告時，把第二張表的 PR 連結、合併證據、阻礙、下一步與查核時間
整合到對應列的階段註記；CI 相關證據留在 CI Evidence，再移除新快照中的第二張表。
不得因此遺失獨立追蹤 PR、已完成列、選擇證據或最後成功查核時間；
讀取失敗保留舊事實與日期並簡述限制，不把舊結果冒充今日成功查核。

發布前檢查 Markdown 表格區塊恰有一個、六欄名稱及順序完全相同、
每列六格、四個階段狀態起首正確（可含 PR 註記）、追蹤列與證據無遺漏。
詳細查核紀錄留內部，表格外只保留必要的精簡查核說明。

每日建立當日快照，即使狀態未變。延續先前選題與追蹤列；同日重跑更新當日檔案，保留過往日期。

<!-- 歷史候選與排程執行紀錄僅存內部 STATE.md／cron logs，不輸出到 Result.md。 -->
