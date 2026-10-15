# Issue <編號>：<問題摘要>

> 依使用者提供的 ExecuTorch issue 18832 報告結構整理：如何 Reproduce、
> 問題釐清／解決方法、解決後的 Demo、環境設定，並加入驗收條件與回歸證據。
> 複製到 repository 慣用的報告位置，例如 `docs/howard/<issue-number>.md`。
> 將所有 `<...>` 換成實際資料；下方命令是佔位範本，須改成可重跑的完整命令。
> 未執行的項目標記 blocked 並說明原因，不可把預期輸出當作實測結果。

- Issue：<URL>
- Baseline commit：<SHA>
- Fixed commit：<SHA；尚未 commit 時填待補>
- 私人 PR 目標：<owner/repo>
- PR：<URL；尚未建立時填待補>
- 報告日期：<日期>

## 驗收條件整理

開發前從 issue 與討論整理條件，逐項列出來源、預期行為與驗證方式。
下表是範例，請替換或補充為該 issue 的實際條件。

| ID | 需求來源 | 驗收條件／預期行為 | 驗證方式 | 必備證據 |
| --- | --- | --- | --- | --- |
| AC-1 | <issue／comment URL> | 原始失敗情境在修正後成功 | 重跑原始 reproducer | 修正前後命令、exit code、關鍵輸出 |
| AC-2 | <issue／comment URL> | 回歸測試能偵測原始缺陷 | 同一測試在 baseline 失敗、fixed 通過 | 測試名稱、兩個版本的結果 |
| AC-3 | <相關行為或需求來源> | 受影響的既有行為維持正確 | 執行相關測試 | 命令、測試摘要 |

## 環境設定

- OS／架構／硬體：<版本與必要資源>
- Repository／worktree：<位置與版本>
- Runtime／venv／依賴：<版本、路徑、安裝方式>
- 必要輸入／模型／產物：<來源、版本或 checksum、取得或生成方式>
- 環境變數與限制：<必要設定、timeout、資源限制>

```bash
cd <repository-path>
<environment-setup-command>
<build-or-artifact-generation-command-if-required>
```

只列必要步驟；不需要 build 或產物生成時明確註明不適用。

## 1. reproduce：如何 Reproduce

在未修改的 baseline 執行，記錄可重跑的完整命令與原始證據。

```bash
cd <baseline-worktree>
<reproduction-command-with-all-required-arguments>
```

- 正確行為：<本來應發生什麼>
- 實際行為：<實測失敗現象>
- Exit code：<實測值>
- 關鍵輸出：

```text
<實際錯誤訊息或失敗輸出>
```

- 證據／log：<路徑或連結>
- 重現狀態：<reproduced / blocked / not reproduced；後兩者填原因與下一步>

## 2. dev：問題釐清／解決方法

**問題釐清**

<根因、觸發條件、證據，以及相關程式位置。區分已證實事實與待驗證假設。>

**解決方法**

<最小修正、修正前後行為、選擇此方法的原因與限制。>

| 變更位置 | 變更內容與原因 | 對應驗收條件 |
| --- | --- | --- |
| <file:symbol> | <具體修正> | <AC-ID> |

- Diff review：<發現與處理結果>

## 3. regression test：回歸驗證

同一回歸測試在 baseline 與 fixed 各跑一次；若為新測試，將測試套用到
隔離的 baseline worktree，而不帶入修正，避免干擾既有工作目錄。
若不可行，記錄原因、替代證據與尚未驗證的範圍。

```bash
cd <baseline-worktree-with-regression-test-only>
<focused-regression-test-command>

cd <fixed-worktree>
<same-focused-regression-test-command>
<relevant-adjacent-tests-command>
```

| 測試／情境 | 對應 AC | Baseline 實測結果 | Fixed 實測結果 | 證據 |
| --- | --- | --- | --- | --- |
| <原始缺陷回歸測試> | <AC-ID> | <失敗訊息、exit code> | <通過摘要、exit code> | <log> |
| <相關既有行為> | <AC-ID> | <結果或未執行原因> | <結果> | <log> |

確認 baseline 失敗原因是原始缺陷；依賴缺失或環境錯誤不能充當回歸證據。

## 解決後的 Demo

在 fixed 版本重跑原始 reproducer，列出完整命令。若輸入或環境與 baseline
不同，說明原因及對比較結果的影響。

```bash
cd <fixed-worktree>
<original-reproduction-command-with-all-required-arguments>
```

- 預期結果：<修正後應有的行為>
- 實測結果／exit code：<實測值>
- 關鍵輸出與產物：<輸出、log、產物路徑>

## 驗收結果與待辦

每個 AC 都必須有對應結果與證據；狀態僅使用 passed、failed、blocked。
尚未執行或缺乏必要證據填 blocked。必要條件未全數 passed 前，不宣稱驗收完成。

| ID | 狀態 | 實測結果與證據 | 未完成原因／下一步 |
| --- | --- | --- | --- |
| AC-1 | <passed / failed / blocked> | <修正後 reproducer 結果> | <待辦或無> |
| AC-2 | <passed / failed / blocked> | <baseline/fixed 回歸證據> | <待辦或無> |
| AC-3 | <passed / failed / blocked> | <相關測試證據> | <待辦或無> |

- 尚未驗證的範圍／剩餘風險：<具體限制或無>
- 驗收結論：<通過／尚未通過，附原因>
- PR／CI／review 狀態：<已確認狀態，不將本機通過等同 CI 通過>
- `STATE.md`：<已同步的報告路徑、階段與待辦>
