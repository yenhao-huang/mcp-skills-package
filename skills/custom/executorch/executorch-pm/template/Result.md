更新時間：<YYYY-MM-DD HH:mm:ss Asia/Taipei>

| 選擇的 issue | 選擇 issue | issue 開發 | 用戶在社群寄送 PR | 該 PR 被 merge | 目前社群 CI 情況 |
| --- | --- | --- | --- | --- | --- |

## Details

### issue 開發 stage

#### <issue 名稱>（issue <編號>）

- 開發：<目前實作進度與個人 fork PR 連結；未確認處明示待確認。>
- 驗證：<測試／驗收結果、證據連結、限制與下一步。>
- 查核時間：<YYYY-MM-DD HH:mm:ss Asia/Taipei>

### 社群評論 stage

#### <issue 名稱>（issue <編號>）

- 社群評論／審查：<issue 留言、PR review、原始來源連結與目前處理狀態。>
- PR 狀態／下一步：<唯讀確認的 open/closed/merged 狀態、阻礙及待處理事項。>
- 查核時間：<YYYY-MM-DD HH:mm:ss Asia/Taipei；失敗時保留最後成功查核時間並註明本次限制。>

CI：<YYYY/MM/DD>; CI fail: <count>; CI sucess: <count>; Require fix: <P(true)>% (true|false); Evidence: <一句原因／限制＋1–2 個證據連結>

<!-- 模板使用規則：產出時移除此整段註解，填入實際資料並刪除未使用的範例區塊。

首行只留更新時間，不加標題、批次、報告日期或括號編輯註記。
不輸出「追蹤範圍與選擇紀錄」或通用「CI 判讀」區段；選題來源、停止／恢復追蹤
決定及判讀規則保留在內部狀態。沒有選題或追蹤項目時保留空表與兩個 stage 標題，
各 stage 寫「目前無追蹤項目。」，不建立虛構範例列。

只輸出一張六欄摘要表，再依序放 Details 的兩個 stage。四個進度欄以
未開始／進行中／完成／受阻／待確認 起首，可接短 PR 連結；CI 欄只放簡短計數或狀態。
開發細節、測試、社群評論、CI Evidence、Require fix、阻礙與查核時間全部放在 Details。
兩個 stage 內依表格順序重複各 issue 小節，保留同一身份與來源連結；不得增加第二張表。

只有實際用戶選題才標記選擇完成，選擇時間與來源記錄在內部 STATE.md。
issue 開發涵蓋重現、修正、測試與 fork PR；必要驗證通過才標記完成。
社群提交必須唯讀確認是用戶提交的對應社群 PR；合併完成必須確認同一 PR 的 merged 狀態。
fork PR 只代表開發證據；closed 或 CI 成功都不代表社群合併。

獨立追蹤 PR 排在選題後，第一欄標示「僅追蹤 PR（未選題）」與 PR 身份／連結；
選擇欄為未開始，未知開發史為待確認。保留 completed／closed-unmerged 項目，除非用戶
明確停止追蹤；已停止的項目不得從歷史報告補回，恢復需要用戶明確要求。

遷移舊報告時將原本表格的詳細說明移入相應 Details 小節，保存證據、限制及原查核時間。
先保留內部選題／停止追蹤紀錄，再移除公開歷史段落。不得改寫過往日期的報告。
CI 計數、歸因與快取遵循 references/ci-triage.md，保留 CI sucess 拼字。
尚無社群 PR 時 CI counts／Require fix 為 n/a，不能以 fork CI 代替。
API 讀取失敗保留舊事實與日期並註明限制，不把舊結果冒充今日成功查核。
社群 issue／PR 連結使用 redirect.github.com。發布前核對表格列與兩個 stage 的身份／順序，
確保所有現行追蹤項目的證據都保留，已停止項目不再出現。
-->
