# Word COM 產檔細節（舊流程）

只有在 Windows＋Microsoft Word 上、且需要用 COM 產生或編輯 .docx 時才讀這份。字級、欄寬、限制等數字以 `rules.yaml` 為準，這裡若有出入，以 rules.yaml 為準。

### 工具（docx 產出）

docx 全新產出以 **PowerShell + Microsoft Word COM** 為主（穩定、所見即所得）。
編輯 .docx 使用 Word COM 或 python-docx；python-pptx 僅處理 .pptx。先檢查當前機器可用工具，勿把另一台機器的 COM 故障視為全域限制。套件修改不保證版面不變；須逐頁渲染檢查，保留使用者手動修改的原檔。

### 中文編碼安全寫法

PowerShell 5.1 腳本使用 UTF-8 with BOM；後續追加使用 UTF-8 without BOM。
暫存腳本使用 runtime://osce 下的唯一檔名；只清理本次建立的檔案。

Word 儲存失敗時，保留本次文件與錯誤資訊供重試，不得列舉並強制結束所有 WINWORD。
只操作本次建立且由本次流程持有的 document/application COM 物件。

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

#### 三、評分表

- **模式 A（條列式評分，醫學系或指定條列者）**：
  - 標題列印「滿分：N×2 分」（14pt）。**注意**：官方空白範本預印「滿分：30分」（對應 15 項），本 skill 採 N×2 計分，N≠15 時務必改寫該數字，勿沿用 30。
  - 欄標題：`@("評分項目（共 N 項）","0 沒有做到","1 部分做到","2 完全做到","註解")`——**N 要帶入實際確認的項目數**（例：共 10 項）
  - 欄寬：`@(8.0, 1.6, 1.6, 1.6, 1.4) cm`
  - 整體表現另一表（6 欄：整體表現／差1分／待加強2分／普通3分／良好4分／優秀5分）

- **模式 B（敘事醫學方式評分，非醫學職類選用）**：
  - 標題列印「評量方式：全人照護與敘事醫學質性評量規準（滿分依 rules.yaml：三個計分向度 × 4 分＝12 分）」（14pt）。
  - 四向度規準表（5 欄）：
    - 欄標題：`@("敘事評量向度","優異 (4分)","熟練 (3分)","發展中 (2分)","未達標準 (1分)")`
    - 欄寬：`@(3.8, 3.3, 3.3, 3.3, 3.3) cm`（總寬 17.0 cm）
    - 列包含：1. 全心傾聽與病患故事探索 (Attention)；2. 同理共鳴與處境再現 (Representation)；3. 關係締結與共同照護同盟 (Affiliation)。
  - 考官質性敘事觀察與反思回饋表（2 欄或 2 列大表格）：
    - 包含「關鍵互動觀察紀錄（Critical Incidents）」與「質性反思與教學回饋建議（Reflective Feedback）」，供考官記錄具體觀察對話。
    - 欄寬：`@(8.5, 8.5) cm`。
  - 整體表現另一表（6 欄：整體表現／差1分／待加強2分／普通3分／良好4分／優秀5分）。

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
# $doc/$word 必須是本次建立的物件，outputPath 必須是新的修訂檔名。
try {
    if (Test-Path -LiteralPath $outputPath) { throw "輸出已存在，請使用新的修訂檔名。" }
    $doc.SaveAs2($outputPath, 16)
} catch {
    # 保留本次文件供人工另存或重試；不關閉其他 Word 文件。
    throw
}
$doc.Close()
# 僅當本次 application 已無其他文件時結束。
if ($word.Documents.Count -eq 0) { $word.Quit() }
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($doc) | Out-Null
[System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
```
