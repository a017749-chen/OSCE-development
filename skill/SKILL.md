---
name: osce-item-development
description: >
  Develop, revise or audit an OSCE assessment station end to end, following the Taiwan Association of Medical Education (TAME) format and the 114 OSCE item-development guideline/checklist, and producing a directly printable .docx station file. Covers the pre-authoring clarification dialogue and blueprint gate, competency alignment, clinical scenario, candidate instructions, standardized-patient/family script, examiner guide, observable 0/1/2 scoring anchors, station-type specifics (history, physical examination, communication/education, explanation/management, technical) and station QA. Trigger for OSCE 出題／修題／審題, 「幫我出一題 OSCE」,「設計 OSCE 試題/教案」,「開發 OSCE 題目」,「我要做一個 OSCE [站型]站」,「出一題 [症狀/主題] 的 OSCE」, SP/family scripts, candidate/examiner guides, or OSCE scoring rubrics. Do not trigger for ordinary clinical case discussion, pure VR/dry-lab simulation curriculum, OSCE psychometrics or standard setting alone (use $osce-education), reliability/statistical analysis alone (use $clinical-statistics), or generic teaching documents unrelated to an OSCE station.
---

# OSCE Item Development — Canonical Workflow

## Core contract

OSCE is performance-based assessment. Align `competency → task → observable behaviour → scoring → SP/examiner standardization` and keep the station feasible for the stated learner and time.

# OSCE 試題開發 Skill

協助使用者「分階段、先討論後產出」地共同開發 OSCE 站：先釐清教案藍圖，再草擬完整站次內容，最後依國考型檢核表審閱並產出正式版本。

**三階段架構**：階段一 出題前確認對話（取得藍圖確認卡同意）→ 階段二 草擬教案五大部分 → 階段三 輸出 Word 檔。

---

## 第一原則

- **OSCE 是表現本位（performance-based）評量**：站次測量學員能在臨床情境中**做什麼**，而非只是「知道什麼」。
- **對齊學員程度、臨床情境、任務、能力指標**。不要把情境設得超出該層級可合理處理的範圍。
- **8 分鐘可完成**：避免劇本過長、資料過多、或需完整診斷處置流程的任務。
- **站型乾淨**：除非評量設計刻意如此，不要混合不相容站型。
- **評分可觀察**：每個評分項目應描述考官／SP 能可靠判斷的具體行為或回應。
- **保密與試題完整性**：不放真實病人識別資料或機構敏感細節（除非已授權且必要）。

---

## 階段一：出題前確認對話

**先對話、再產出。** 動筆前一定要跟出題老師把這一題的基本設定講清楚——AI 自行假設站型、診斷、項目數，老師事後才發現方向不對，整份就得重做。

### 閘門規則

- **預設先對話再產出**；唯有使用者明確表示「不用問、直接產」時才略過提問。
- **已提供的參數不重複問**，只問缺漏或前後矛盾之處。
- **無論如何都要出示「藍圖確認卡」**，未取得明確確認前**不得進入產出**。

### 需釐清的參數

| 參數 | 說明 |
|------|------|
| **站型** | 病史詢問、身體檢查、醫病溝通與衛教、病情解釋及臨床處置、技術／混合 |
| **學員程度** | clerk、PGY、國考考生、住院醫師⋯ |
| **目標能力／領域** | 病人照護、溝通、臨床推理、專業素養、技術技能、安全 |
| **核心任務** | 考生在 8 分鐘內要完成什麼 |
| **目標診斷與重要鑑別** | 主診斷＋至少 2-3 個有意義的鑑別 |
| **評分項目數（N）** | 要出幾項評分項目——**必須問，不要預設** |
| **場景** | 門診、急診、病房、手術室、處置室、衛教室 |
| **必要人員** | SP、考官、護理師、家屬、假人/模型 |
| **產出層級** | 討論用草稿、完整可印教案、或僅檢核表審閱 |

### 分三輪提問

**第 1 輪 — 站次定位**（決定整站骨架）
1. 站型？ 2. 學員程度？ 3. 科別與主題／主訴？ 4. 場景？

**第 2 輪 — 評量設計**（決定評分表）
1. 主要評量目標（一句話：考生要能做到什麼）？ 2. 核心任務（8 分鐘內完成什麼）？
3. 主診斷＋重要鑑別診斷（≥3）？ 4. 目標能力／領域？
5. **要出幾項評分項目？** 6.（可選）高鑑別力★想考的重點？

**第 3 輪 — 執行細節**（決定道具與產出）
1. 必要人員與道具？ 2. 產出層級？ 3.（可選）預估難度與過關意圖？

### 評分項目數（N）怎麼問

- 問法：「這一站要出**幾項**評分項目？（國考型建議 15 項；其他考型 10–15 項；也可依你的需求指定）」
- 預設 15，但**一定要讓老師有機會改**，不得逕自套用。
- **滿分自動＝N × 2**（每項 0/1/2），不再固定 30 分。
- 比例型規則隨 N 換算，並在確認卡標出實際數字：
  - ★高鑑別力 2–5 項；共通／通用項目 ≤1 項
  - 主要評分範圍 ≥50%（即至少 ⌈N/2⌉ 項）
  - 病史站 LQQOPERA 群組 ≤30%（N=15→≤4；N=12→≤3；N=10→≤3）

### 提問風格

- 每輪**一次問完該輪**（最多 4–5 題），編號呈現，每題附**選項或建議預設值**，老師可只回數字或「用預設」。
- 老師答不出來時（最常見：鑑別診斷、核心任務、評量目標），**主動提 2–3 個建議草案讓他挑**，不要空等。
- **真正固定、不必問的只有**：測驗時間 8 分鐘、每項 0/1/2 三級尺標、五大部分結構。（**項目數與滿分不在此列**。）
- 若環境支援選項式提問工具（AskUserQuestion），用它呈現可列舉參數（站型／學員程度／場景／產出層級／項目數）；否則用編號清單。

### 藍圖確認卡（產出前閘門）

三輪結束（或使用者已給齊）後，輸出下列固定格式；未提供欄位標「（待補）」，使用者已提供的標「（已提供）」：

```
【藍圖確認卡】
站　　型：        學員程度：
科別主題：        場　　景：
評量目標：
核心任務：
主 診 斷：        鑑別診斷：（≥3）
目標能力：        人員道具：
評分項目：N 項    滿　　分：N×2 分
產出層級：        預估難度：
── 自動套用 ──
8 分鐘｜每項 0/1/2｜★2–5 項｜共通 ≤1｜主要範圍 ≥⌈N/2⌉ 項｜子項目 ≤3
（病史站 LQQOPERA ≤30%；身體檢查站 IAPP 順序；溝通／病情解釋站 Teach-back 不可省略）
```

結尾固定問：「以上確認無誤請回『確認』，要改哪一項直接說。」**取得明確確認後才進入階段二。**

---

## 階段二：標準工作流程（草擬）

> 進入本階段的前提：階段一的藍圖確認卡已取得使用者明確確認。

### 0. 正式草擬前先讀格式範本

正式產出前，先檢視 `G:\我的雲端硬碟\OSCE\OSCE教案開發教學\4.試題開發格式` 中對應站型的範本：

- `1.試題參考格式-空白+例句(SP  病史詢問).docx`
- `2.試題參考格式-空白+例句(SP  身體檢查).docx`
- `3.試題參考格式-空白+例句(SP  醫病溝通與衛教).docx`
- `4.試題參考格式-空白+例句(SP  病情解釋及臨床處置).docx`

若站型不符合上述四種，說明最接近哪一種、做了哪些格式調整。**早期腦力激盪可略過範本讀取，但正式輸出必須依範本結構**。

### 1. 建立評量藍圖

- 站次名稱、站型、學員程度、時間（通常 8 分鐘）、場景、目標能力、過關意圖。
- 以一句話寫出**主要評量目標**。
- 對應至臨床能力標準或在地能力框架。

### 2. 塑造臨床情境

- 一個聚焦的主訴或臨床問題。
- 提供足夠完成任務的資料，但不要過度暴露而縮窄臨床推理。
- 案例內部一致：年齡、性別、生命徵象、病程、檢驗影像、檢查發現、預期處置都應吻合。
- **告示牌主訴 ≤ 30 中文字**。

### 3. 草擬教案五大部分

按以下五大部分輸出（依台灣 TAME 標準）：

1. **告示牌**：站次號（**48pt**）＋病患資訊（**36pt**，≤30字）
2. **考生指引**（**26pt**）：背景資料（<30字）＋測驗主題（**≤3 個**紅色●）＋測驗時間＋**相關檢查報告表格**（診間文件 14pt）
3. **評分表**：N 項 0/1/2 評分＋整體表現 5 等第＋**滿分 N×2 分**（N＝階段一確認的項目數）
4. **考官指引**：病情摘要＋鑑別診斷（≥3 個）＋道具＋**評分說明（每項三等級）**＋**SP 劇本摘要**
5. **SP 指引**：演出說明＋回應原則＋劇情摘要＋**劇本對白例句（三欄一問一答表格）**

### 4. 設計評分項目（Checklist）

**格式規則：**
- 共 **N 項**——**N 於階段一與使用者確認**（國考型建議 15 項；其他考型 10-15 項）；每項 0/1/2 分，**滿分＝N×2 分**
- **2-5 項為高難度題**（鑑別力高）
- **共通／通用項目最多 1 項**
- **主要評分範圍應佔 50% 以上**（即至少 ⌈N/2⌉ 項）
- 每項描述**可觀察的具體行為**，避免主觀形容詞（如「適當地」）
- 完全做到／部份做到／沒有做到之錨點要清楚
- 子項目不超過 3 個
- **避免重複給分**：同一行為不要在多項各給一次分
- **避免需要隱性推論**才能評分的項目

**站型框架建議（以 N＝15 為例；N 不同時按比例調整，比例型上限如 LQQOPERA ≤30%、主要範圍 ≥50% 仍須成立）：**

- **病史詢問站**：開場（1）→ LQQOPERA 群組（合併計分，≤4 項，符合 ≤30% 上限）→ 過去病史/手術史（1）→ 藥物史/過敏史（1）→ 家族史（1）→ 社會史/旅遊史（1）→ 系統回顧（1）→ 作結/ICE（1）→ 主題特異／鑑別診斷高鑑別項（★，4-5）
  - 注意：LQQOPERA 雖有八個面向，但要**合併成少數評分項**，群組不超過總項目 30%（國考檢核標準，15 項時即 ≤4 項）；把分數留給鑑別診斷線索、危險因子、ICE 等高鑑別力項目（合計約 15 項）
- **身體檢查站**：基本態度（2）→ 視診（1-2）→ IAPP 系統檢查（視→聽→叩→觸，腹部聽診必須在叩觸前）（4-6）→ 診斷特定徵象（4-6）→ 作結口頭報告（1-2）
- **醫病溝通站**：建立關係/同理（2）→ 確認現況理解（1）→ 衛教資訊（6-8）→ **Teach-back（1，不可省略）** → 結尾（2-3）
- **病情解釋／臨床處置站**：準備（1）→ 告知病情（3-4）→ 解釋診斷/檢查/處置（4-5）→ 共同決策（2-3）→ Teach-back＋結尾（2）

### 5. 設計 SP 行為

- 給 SP 清楚的身份、情緒、痛苦程度、說話風格、界線
- **明確標示 SP 可說／可做、不可說／不可做**
- **每個 SP 面向評分項目都要有對應的 SP 回應或行為描述**，含詳細溝通範例
- SP 主動發問**不超過 5 個**
- 若 SP 被特定考生語句觸發，要明確標示觸發條件
- **劇本對白例句必須是三欄表格**：

| 病歷架構 | 醫師對 SP 說的話 | SP 的回應或提問 |
|---------|--------------|---------|

- SP 劇本摘要同時放在**考官指引末尾**，供考官掌握情境

### 6. 草擬考生指引

- 說明角色、場景、任務、時間、可用資源
- **不洩漏評分細節**，不直接重複評分項目用語
- 若某領域不評分，明確說明（例：「本站不評分身體檢查」）
- 標示是否有護理師/助理或假人/模型可用
- **測驗主題 ≤ 3 個紅色 ●**（官方範本：「少於3項提示」；一般為 2-3 項）；若有避免行為，加 ※ 說明
  ```
  ● 任務一
  ● 任務二
  ● 任務三
  ※ 請勿詢問考生指引中已提供的資訊
  ```

### 7. 準備資料與道具

- **提示卡 ≤ 3 張**
- 難以模擬的徵象（紅疹、黃疸、黑便、傷口）改用圖片/照片
- **相關檢查報告** A4 ≤ 3 頁；純文字檢驗報告 ≤ 2 頁
- 含**有意義的陽性與陰性發現**，避免大量無關正常數據
- 相關檢查報告表格（考生指引內）：
  - 欄1：生命徵象（BP/HR/Temp/RR/SpO2）
  - 欄2：主要臨床症狀摘要
  - 第3列起：過去病史/藥物史（標示「須由考生自行詢問」）

### 8. 依檢核表審閱

- 國考型一般要求
- 該站型的考官要求
- SP 要求
- 考生指引清晰度
- **預估難度**：極難 / 難 / 中 / 易
- 在站次意圖與檢核表都穩定後，才**建議過關分數**

---

## 站型專屬注意事項

### 病史詢問站
- 評分情報蒐集、時序組織、相關危險因子探詢、症狀-疾病連結、能否摘要或轉場
- LQQOPERA 群組不超過 30% 評分項
- 避免「詢問相關症狀」這類空泛項目，除非已指定預期症狀
- SP 回答聚焦、以被動回應考生提問為主

### 身體檢查站
- 考生指引須明示**檢查部位／系統**與**不評分項目**
- 用聚焦、可觀察的步驟；避免「腹部檢查表現良好」這類含糊給分
- 若需助手、站姿/臥姿 SP、覆蓋、暴露、隱私處理，明示於設置與考生指引
- 無法模擬的異常用圖/報告提示，並定義考生如何辨識或詮釋
- **腹部 IAPP 順序不可跳過聽診**

### 醫病溝通與衛教站
- 評分重點：建立關係、議程設定、同理、訊息分塊、確認理解、回應情緒、結尾
- **Teach-back 不可省略**，是高鑑別力項目
- 不要讓禮貌性項目主導評分；溝通品質要支持臨床任務

### 病情解釋／臨床處置站
- 評分：對可能診斷的解釋、不確定性、下一步檢查、立即安全議題、治療選項、追蹤、病人擔憂
- 考生有足夠資訊解釋與計畫，但任務不能變成朗讀結果
- SP 提問測試：諮詢清晰度、同理、安全網、共同決策

### 技術／處置站
- 區分：安全/身份/同意、準備、無菌或清潔技術、關鍵步驟、完成、併發症處置
- 用設備清單與設置照片/示意圖協助
- 步驟有先後順序時明確標示

---

## 階段三：輸出 Word 檔

**輸出路徑**：`D:\OSCE教案開發教學\[科別]_[主題]_OSCE試題.docx`

### 工具（docx 產出）

docx 全新產出以 **PowerShell + Microsoft Word COM** 為主（穩定、所見即所得）。
備註：本機亦有 Node.js 與 Python（含 python-pptx）；若需「**編輯既有** .pptx／.docx」而不破壞圖片版面，可改用 python-pptx 等套件。**PowerPoint COM 在本機已損壞（Interface not registered，0x80040155），請勿使用**；且切勿用整份重產的腳本覆蓋使用者已手動編輯過的檔案。

### 中文編碼安全寫法

```powershell
# 第一段：用 UTF-8 with BOM 建立檔案（確保 PowerShell 正確讀取中文）
[System.IO.File]::WriteAllText("D:\OSCE教案開發教學\_temp.ps1", $part1, [System.Text.Encoding]::UTF8)

# 後續追加：用 UTF-8 without BOM（避免中間出現 BOM 破壞檔案）
$encNoBOM = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::AppendAllText("D:\OSCE教案開發教學\_temp.ps1", $part2, $encNoBOM)

& powershell -ExecutionPolicy Bypass -File "D:\OSCE教案開發教學\_temp.ps1" 2>&1
Remove-Item "D:\OSCE教案開發教學\_temp.ps1" -Force
```

若 Word 未關閉導致儲存失敗：`Get-Process WINWORD | Stop-Process -Force`

### 特殊字元（**踩過的坑**）

Windows PowerShell 5.1 **不支援 `` `u3000 `` 這類 Unicode 逸出**，會原樣輸出「u3000」字面文字，
造成 □ ■ ℃ μ ’ … 全形空格全部變成亂碼。務必**直接在 UTF-8 腳本中打真正的字元**，
或用 `[char]0x3000`：

| 用途 | 直接寫 | 或 |
|------|--------|-----|
| 全形空格 | `　` | `[char]0x3000` |
| 未勾選方塊 | `□` | `[char]0x25A1` |
| 已勾選方塊 | `■` | `[char]0x25A0` |
| 攝氏度 | `℃` | `[char]0x2103` |
| micro | `μ` | `[char]0x03BC` |
| 右單引號（Murphy’s） | `’` | `[char]0x2019` |
| 刪節號 | `…` | `[char]0x2026` |

產出後務必掃描殘留：`if ($full -match 'u3000|u2610|u25A0|u2103|u03BC|u2019|u2026') { 有問題 }`

### 標準輔助函式

```powershell
$word = New-Object -ComObject Word.Application; $word.Visible = $false
$doc = $word.Documents.Add()
$doc.PageSetup.PaperSize = 7  # wdPaperA4（注意：9 是 A5，會造成表格被切邊）
$doc.PageSetup.TopMargin    = $word.CentimetersToPoints(2.0)
$doc.PageSetup.BottomMargin = $word.CentimetersToPoints(2.0)
$doc.PageSetup.LeftMargin   = $word.CentimetersToPoints(2.0)
$doc.PageSetup.RightMargin  = $word.CentimetersToPoints(2.0)
# A4 + 四邊 2.0cm => 版面可用寬度 17cm，所有表格總寬不得超過 17cm
# 行距：單行、段前後間距 0（Word 預設 1.16 倍行距＋段後 8pt 會讓行高看起來加倍）
$norm = $doc.Styles.Item(-1).ParagraphFormat   # Normal 樣式
$norm.LineSpacingRule = 0; $norm.SpaceBefore = 0; $norm.SpaceAfter = 0
$sel = $word.Selection

function NL { $sel.TypeParagraph() }
function PB { $sel.InsertBreak(7) }                  # 分頁
function SA { param($a=0) $sel.ParagraphFormat.Alignment = $a }
function SZ { param($s=12) $sel.Font.Size = $s }     # 全文預設 12pt
function B1 { $sel.Font.Bold = 1 }
function B0 { $sel.Font.Bold = 0 }
function U1 { $sel.Font.Underline = 1 }
function U0 { $sel.Font.Underline = 0 }
function CR { param($c=0) $sel.Font.Color = $c }     # 255 = 紅（BGR）
function T  { param($t) $sel.TypeText($t) }
function BU { param($t) SZ 20; B1; T $t; B0; SZ 12; NL }          # 20pt 粗體＝五大部分標題
function H26 { param($t) SZ 26; T $t; SZ 12 }                     # 26pt＝考生指引本體
function TC { param($tbl) $tbl.Rows.Alignment = 1 }  # 表格置中（必加）
```

### 表格規則

- 繁體中文 Word 表格樣式名稱用 `"表格 格線 1"`（不是 `"Table Grid"`）
- 每個表格建立後**必呼叫 `TC $tbl`**，否則表格靠左跑掉
- 表頭底色用 `Shading.BackgroundPatternColor = 14277081`（淺藍灰）
- 欄寬用 `$word.CentimetersToPoints(cm)` 換算，**表格總寬 ≤ 17cm**（超過會被切邊）
- 框線細化為 0.5pt：`$tbl.Borders.Item($i).LineWidth = 4`（i = 1..6）
- 儲存格內距縮小：上下 0.03cm、左右 0.12cm（Top/Bottom/Left/RightPadding）
- 表格內段落：SpaceBefore/SpaceAfter = 0、LineSpacingRule = 0（單行）
- 完成後 `$tbl.AllowAutoFit = $false` 鎖定欄寬
- 表格後移動游標：`$sel.EndOf(6,0) | Out-Null; NL; NL`

### 字級規格（依官方範本，**不可自行縮小**）

已用官方四份範本的 XML 實測確認，字級是 TAME 格式的一部分：

| 元素 | 字級 | 說明 |
|------|------|------|
| 五大部分標題（告示牌／考生指引／評分表／考官指引／SP指引） | **20pt** | 粗體 |
| 告示牌 站次號「第　站」 | **48pt** | 粗體置中；考生於門口遠距閱讀 |
| 告示牌 病患資訊（年齡、性別、症狀） | **36pt** | 粗體置中，≤30字 |
| 考生指引 背景資料／測驗主題／測驗時間／相關檢查報告標題 | **26pt** | 進站前 1 分鐘要讀完 |
| 診間內提供考生訊息之文件（檢查報告內容） | **14pt** | 官方註明「黏貼固定於診間桌面上」 |
| 評分表 滿分／總得分／評分考官簽名 | **14pt** | |
| 其餘內文、表格內容、考官指引、SP 指引本體 | **12pt** | Normal 樣式預設 |

### 五大部分骨架

#### 一、告示牌（2 列 1 欄表格）
- 列 1：「第　站」**48pt** 粗體置中
- 列 2：病患資訊（≤30字）**36pt** 粗體置中

#### 二、考生指引（含相關檢查報告 3×2 表格）
- 段落標題「考生指引」20pt；以下欄位本體 **26pt**
- ■背景資料（≤30字）
- ■測驗主題：**≤3 個**紅色 ●＋（可選）※避免事項
- ■測驗時間：8 分鐘
- ■相關檢查報告（3列2欄表格，含生命徵象/症狀/過去病史與藥物標示）——**表格內文 14pt**

#### 三、評分表（5 欄表格）
- 標題列印「滿分：N×2 分」（14pt）。**注意**：官方空白範本預印「滿分：30分」（對應 15 項），本 skill 採 N×2 計分，N≠15 時務必改寫該數字，勿沿用 30。
- 欄標題：`@("評分項目（共 N 項）","0 沒有做到","1 部分做到","2 完全做到","註解")`——**N 要帶入實際確認的項目數**（例：共 10 項）
- 欄寬：`@(8.0, 1.6, 1.6, 1.6, 1.4) cm`
- 整體表現另一表（6 欄：整體表現／差1分／待加強2分／普通3分／良好4分／優秀5分）

#### 四、考官指引（含評分說明＋SP 劇本摘要）
- 考官任務提示（固定 5 條）
- 測驗場景、SP 基本資料、起始姿勢
- 病情摘要、鑑別診斷（≥3 個依可能性排序）、道具
- **評分說明**：每項三等級（完全做到/部份做到/沒有做到）
- **SP 劇本摘要**：情緒強度＋人物設定＋回應考生原則

#### 五、SP 指引（含三欄對白表格）
- 場景、起始姿勢、情緒（x/10）、表情、肢體動作、對話風格
- ■人員/道具：紅字標示
- 回應考生原則（prose）、劇情摘要
- **劇本對白例句（三欄表格）**：欄寬 3.5 / 6.5 / 5.5 cm
  - 欄標題：`@("病歷架構","醫師對 SP 說的話","SP 的回應或提問")`（依官方範本用字）
- **診間示意圖**（官方範本必備）：請明示拉簾、診助、考官、SP、考生之建議位置

### 儲存

```powershell
$doc.SaveAs2($outputPath, 16)
$doc.Close(); $word.Quit()
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
[System.GC]::Collect()
```

---

## 品質檢核閘（產出前自問）

### 站次層級
- **是否已出示藍圖確認卡並取得使用者明確確認？**（未確認不得產出）
- 任務在 8 分鐘內可完成嗎？
- 站次符合學員程度與目標能力嗎？
- 站型乾淨、未混合不相容類型嗎？

### 評分層級
- 全部評分項目都是**可觀察行為**嗎？
- **項目數與藍圖確認卡一致？滿分＝N×2？**（國考型建議 15 項＝滿分 30）2-5 項為高難度？
- 共通項目 ≤ 1？主要評分範圍 ≥ 50%（≥⌈N/2⌉ 項）？
- 部份給分的錨點清楚嗎？
- 每個 SP 面向項目都有對應 SP 回應嗎？

### SP 層級
- SP 主動提問 ≤ 5 個？
- 觸發條件明確？

### 考生指引層級
- 提示卡 ≤ 3？檢查報告 ≤ 3 頁（純文字 ≤ 2 頁）？
- 考生指引清晰，未洩漏評分？

### 格式層級（本系統 Word 輸出）
- **字級符合官方規格？**告示牌 48/36pt、考生指引 26pt、五大部分標題 20pt、診間文件 14pt、其餘 12pt
- 背景資料 ≤ 30 字？告示牌病患資訊 ≤ 30 字？
- 測驗主題 ≤ 3 個紅色 ●？
- **SP 指引末含診間示意圖？**
- 鑑別診斷 ≥ 3 個？病史詢問涵蓋過去病史/藥物史/家族史/社會史？
- 醫病溝通站含 Teach-back？腹部檢查依 IAPP 順序？
- 劇本對白用三欄一問一答表格？
- 考官指引含評分說明（三等級）＋ SP 劇本摘要？
- **所有表格皆已呼叫 `TC $tbl` 置中**？

---

## 偏好的輸出順序

### 討論用草稿
1. 站次藍圖
2. 考生指引
3. 考官指引與站次流程
4. SP 設定、情緒、背景、劇本
5. 必要道具/報告
6. 評分表＋評分說明
7. 審閱筆記與待釐清問題

### 正式教案另加
- 封面 metadata
- 情境摘要
- 場地設置檢核表
- 時間與人員角色
- 考官評分表
- SP 訓練檢核表
- 考生面頁
- 附件與資料

---

## 修訂風格

- **先保留臨床意圖**，再修可行性與評分信度
- 偏好**收緊模糊的評分項目**，而非加更多項目
- 若站次過大，分拆為獨立的病史／檢查／衛教／處置站
- 不確定時，**標記為待討論點**，不要默默自行編造高利害臨床細節

---

## Handbook detail (on demand)
Read [references/handbook-integration.md](references/handbook-integration.md) when the task needs handbook-specific workflow, acceptance or compatibility details. Do not load all original run cards.

## Cross-skill boundaries

- Simulation curriculum without a summative OSCE item → `$simulation-curriculum`.
- OSCE psychometrics, standard setting, blueprint-level or programme-level work → `$osce-education`.
- ICC / Cronbach / item analysis only → `$clinical-statistics`. If performance data are used to revise the station, statistical analysis may hand back to this skill for item redesign.
- For the final Word/PDF station file, finish content and QA first, then use `$artifact-production`. The docx-generation detail above remains authoritative for encoding, table widths and font sizes. User-specified templates/paths override it. Do not regenerate over a manually edited canonical file without preserving it.

## Context Repo contract

- Store final station documents in the cloud project workspace; keep durable blueprint/format decisions and handoff in the Context Repo only when this is a persistent project.
- For substantial persistent project changes, finish with `$context-closeout`.

<!-- merged 2026-09-09: local ~/.claude/skills/osce-item-development (23 KB, made primary at the user's direction) + repo skeleton (English trigger/anti-trigger frontmatter, cross-skill boundaries, Context Repo contract). Prior repo SKILL.md preserved under references/. -->
