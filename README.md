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

## 出題與使用方式

本工作包支援兩種出題流程：

### 方式 A：Grill Me 引導式訪談 → 自動產出專屬 Prompt（推薦）

出題教師無需事先寫好複雜的 Prompt，系統會像專科審題委員般，透過結構化訪談引導老師設定背景、情境與評量指標，並在訪談結束後**自動編譯產出一份專屬的《OSCE 出題 Prompt》**，可直接複製貼入任何 AI 大模型（Claude、ChatGPT、Gemini、本機模型）開始出題：

1. **命令列獨立工具（任何環境皆可執行）**：
   ```bash
   python scripts/grill_me.py
   ```
   逐步回答職類、情境、任務與 SP 設定，完成後即在目錄下產出 `OSCE_Authoring_Prompt.md`。

2. **Skill 對話模式**：
   在已部署 skill 之環境直接說：
   ```
   幫我出一題 OSCE
   ```
   或
   ```
   用 Grill Me 幫我設定 OSCE 題目並產出出題 Prompt
   ```

### 方式 B：直接填寫靜態 Prompt 範本

- **醫學系專用（條列式 0/1/2 計分）**：`teaching/OSCE出題Prompt_出題教師專用.docx`
- **跨職類與敘事醫學專用（全人照護質性評量）**：`teaching/OSCE出題Prompt_跨職類與敘事醫學版.md`

把範本中的 `--` 換成自己的臨床情境即可直接送出。

### 方式 C：免費版 ChatGPT / 網頁大模型用戶（無 Agent 環境專用）

若您手邊沒有 coding agent 或進階終端工具，僅使用一般的**免費版 ChatGPT（3.5 / 4o-mini / 4o 均可）、Claude 或 Gemini 網頁介面**：
1. 打開本 repo 根目錄的 [`SKILL_GPT.md`](SKILL_GPT.md)（或 [`teaching/SKILL_GPT.md`](teaching/SKILL_GPT.md)）。
2. **複製全部內容**，貼入網頁版 ChatGPT 的第一條對話（或填入 Custom GPT 的 Instructions 欄位）。
3. ChatGPT 會立即載入所有 TAME 規範、職類分流、敘事醫學向度規準與防呆紅線，並自動啟動 **Grill Me 訪談對話**，引導您完成背景設定並產出試題！

---

## 核心規格與評分模式摘要

### 職類分流與評分模式

| 考評職類 | 支援評分模式 | 評分架構說明 |
|----------|--------------|--------------|
| **醫學系／醫師** | **TAME 官方條列式評分** | 項目數 N 由出題者決定（建議 10–15 項，國考型 15 項），**滿分＝N×2 分**。每項 0 沒有做到／1 部分做到／2 完全做到。★高鑑別力 2–5 項；共通項 ≤1；主要範圍 ≥⌈N/2⌉ 項；子項目 ≤3。 |
| **非醫學職類**<br>（護理、藥學、物理治療、職能治療、呼吸治療、營養、社工、心理、醫技等） | **敘事醫學方式評分**<br>（推薦全人照護溝通/衛教） | 採用 Rita Charon 敘事醫學體系，**不產出破碎扣分式的 0/1/2 條列打勾**，改採四大核心向度質性評量規準（優異4分／熟練3分／發展中2分／未達標準1分）：<br>1. **全心傾聽與病患故事探索 (Attention)**<br>2. **同理共鳴與處境再現 (Representation)**<br>3. **關係締結與共同照護同盟 (Affiliation)**<br>4. **考官質性敘事觀察與反思回饋表 (Narrative Feedback)**<br>＋整體表現 5 等第。 |
| **非醫學職類** | **專業條列式評分** | 若該職類技術操作站需要客觀步驟查核，亦可指定採用 0/1/2 條列式評分。 |

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
