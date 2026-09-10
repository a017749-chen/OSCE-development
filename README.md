# OSCE 試題開發工作包

依**台灣醫學教育學會（TAME）**格式與 114 年度 OSCE 試題開發指引／檢核表，開發、修訂、審閱 OSCE 教案的完整工具組。

維護者：陳義展 醫師（長庚醫院 一般外科／臨床技能中心主任）

> ⚠️ **本 repo 建議設為 private。** `templates/` 收錄的是台灣醫學教育學會的官方試題參考格式，著作權屬該學會；此處僅供內部出題作業對照使用，請勿對外散布。

---

## 目錄結構

| 目錄 | 內容 |
|------|------|
| `skill/` | Context Repo 正式 skill 的發行快照；請在 Context Repo 修改後同步 |
| `templates/` | 台灣醫學教育學會官方試題參考格式（四種 SP 站型＋操作技能站） |
| `teaching/` | 出題教師講習簡報、可直接複製的出題 Prompt 講義 |
| `stations/` | 已完成的教案範例（16 份，涵蓋五種站型） |

---

## skill 怎麼用

先依下方「跨機部署」安裝完整 skill 目錄（含 references 與本機資產指標），然後直接說：

```
幫我出一題 OSCE
```

skill 會整理站次定位、評量設計、執行細節並展示藍圖。已給齊設定並要求產出、或已授權直接產出時繼續；僅詢問會實質改變結果的缺漏。

`teaching/OSCE出題Prompt_出題教師專用.docx` 是給出題老師的填空式 prompt，把 `--` 換成自己的內容即可。

---

## 核心規格摘要

### 評分表
- 評分項目數 **N 由出題者決定**（國考型建議 15，其他 10–15），**滿分＝N×2**
- 每項 0／1／2 三級，錨點須為可觀察行為
- ★高鑑別力 2–5 項；共通項 ≤1；主要評分範圍 ≥⌈N/2⌉ 項；子項目 ≤3

### 字級（**TAME 官方硬規格，不可自行縮小**）
| 元素 | 字級 |
|------|------|
| 告示牌 站次號 | 48pt |
| 告示牌 病患資訊（≤30字） | 36pt |
| 考生指引本體 | 26pt |
| 五大部分標題 | 20pt |
| 診間文件、評分表滿分／簽名 | 14pt |
| 內文與表格 | 12pt |

### SP 提問限制
- 主動發問 **≤5 題**，其中觸及評分項目的 **≤2 題**
- 提問須押在**考生完成主要說明之後**，SP 不得主導會談
- **劇本對白例句表至多 2 列**可寫成提問，其餘列只寫「回應」
- 若提問觸及評分項目，評分說明須註明「經 SP 提問後才說明者，最多部份做到（1 分）」

### 站型專屬紅線
- 病史站：LQQOPERA 群組 ≤30%（15 項時即 ≤4 項）
- 身體檢查站：腹部須依 IAPP 順序（**聽診在叩、觸之前**）
- 溝通衛教／病情解釋站：**Teach-back 不可省略**

---

## 已知待辦

`stations/` 中 **2026-07 之前產出的教案**採舊字級（全文 12pt、告示牌 36／24pt），**不符官方規格**，送審前需調整。目前僅 `一般外科_腹痛病情解釋_OSCE試題.docx` 已套用正確字級。

---

## 產出環境備註

- .docx 產出使用 **PowerShell + Microsoft Word COM**
- 編輯 .docx 使用 Word COM 或 python-docx；python-pptx 用於 .pptx。修改後另做逐頁版面檢查。
- COM 可用性需在當前機器檢查。只管理本次建立的文件，不強制結束其他 Word 工作階段。

## 跨機部署

唯一規則來源為私人 YiChan-Context-Repo 的
`.agents/skills/osce-item-development/`；本 repo 管理部署程式。
既有 templates/stations/teaching 檔案保留作相容與歷史用途，本次不遷移。
新教案成果依 registry 保存到 cloud://OSCE/OSCE教案開發教學。

需要 Python 3.10+；YAML registry 另需 `pip install -r requirements.txt`。
Context Repo 位置可使用 -ContextRoot 或 YICHAN_CONTEXT_ROOT；
未指定時偵測使用者 Documents/ 或使用者根目錄下的 YiChan-Context-Repo。
兩處皆存在時須明確指定。雲端與 runtime 根目錄取自該 repo 的
SYSTEM_REGISTRY.yaml 與 SYSTEM_REGISTRY.local.yaml。

```powershell
# 預設唯讀，列出 Claude 與 Codex 各自的變更及衝突
.\sync-skill.ps1 -ContextRoot '<本機 Context Repo>'
# 實際部署
.\sync-skill.ps1 -ContextRoot '<本機 Context Repo>' -Apply
# 更新本 repo 的發行快照（明確指定目標）
.\sync-skill.ps1 -ContextRoot '<本機 Context Repo>' -Target '.\skill' -Apply
```

範本依序使用 -TemplateRoot、registry 解析的雲端範本、repo templates/。
缺少四種站型範本時停止。部署會產生 deployment.local.json，讓已安裝的 skill
找到實際 template_dir、output_dir、runtime_dir。
本機指標、同步基準 .sync-state.json 與 .sync-backups/ 不進 Git。

任何目標有未管理差異或上次部署後的自行修改時，整批預檢失敗且不寫入。
首次接管既有不同內容時，先將差異整合回 Context Repo，保存舊版本，
再讓目標與 canonical 內容一致後建立基準。工具沒有強制覆蓋選項。
正常來源更新會先備份被替換檔案、複製後驗證 SHA-256；多餘檔案保留並列出。
若執行中失敗，已完成的個別檔案可能已更新；保留備份且錯誤退出，修正後重跑。

驗證：`python -B -m unittest discover -s tests`。
這些測試驗證部署行為，不代表既有教案通過臨床審題或逐頁視覺 QA。
- Windows PowerShell 5.1 **不支援 `` `u3000 `` 這類 Unicode 逸出**，特殊字元（□ ■ ℃ μ ’ …）須直接輸入真字元
