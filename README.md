# OSCE 試題開發工作包

依**台灣醫學教育學會（TAME）**格式與 114 年度 OSCE 試題開發指引／檢核表，開發、修訂、審閱 OSCE 教案的完整工具組。

維護者：陳義展 醫師（長庚醫院 一般外科／臨床技能中心主任）

> ⚠️ **本 repo 建議設為 private。** `templates/` 收錄的是台灣醫學教育學會的官方試題參考格式，著作權屬該學會；此處僅供內部出題作業對照使用，請勿對外散布。

---

## 目錄結構

| 目錄 | 內容 |
|------|------|
| `skill/` | **osce-item-development skill 的唯一正本**；Claude、Codex、Context Repo 的副本都由 `sync-skill.ps1` 部署 |
| `rules.yaml` | **所有硬規格數字的唯一來源**；SKILL.md、SKILL_GPT.md、本 README 的規格區塊與 `grill_me.py` 都從它產生 |
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
1. 打開本 repo 根目錄的 [`SKILL_GPT.md`](SKILL_GPT.md)。
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

### 硬規格（由 rules.yaml 產生，改數字請改 rules.yaml 後執行 `python scripts/build_docs.py`）

<!-- BEGIN GENERATED: hard-spec (edit rules.yaml, then run scripts/build_docs.py) -->
**頁面**：A4，四邊 2.0 cm，表格總寬 ≤17.0 cm。五大部分：告示牌／考生指引／評分表／考官指引／SP 指引。測驗時間 8 分鐘。

**字級（TAME 官方，不可自行縮小）**

| 元素 | 字級 | 說明 |
|---|---|---|
| 告示牌 站次號「第　站」 | **48pt** | 粗體置中；考生在門口遠距閱讀 |
| 告示牌 病患資訊（≤30 字） | **36pt** | 粗體置中 |
| 考生指引本體（背景、測驗主題、時間、報告標題） | **26pt** | 進站前 1 分鐘要讀完 |
| 五大部分標題 | **20pt** | 粗體 |
| 診間文件／檢查報告內容 | **14pt** | 黏貼於診間桌面 |
| 評分表 滿分／總得分／考官簽名 | **14pt** |  |
| 其餘內文、表格、考官指引、SP 指引 | **12pt** | Normal 樣式 |

**條列式評分（醫學系預設）**

- 共 **N 項**，N 於階段一確認（國考型建議 15 項，其他 10–15 項）；每項 0 沒有做到／1 部分做到／2 完全做到，**滿分＝N×2 分**。
- ★高鑑別力 **2–5 項**；共通／通用項目 **≤1 項**；主要評分範圍 **≥50%**（至少 ⌈N/2⌉ 項，N=15 時 ≥8）；子項目 **≤3**。
- 病史站 LQQOPERA 群組 **≤30%**（N=15→≤4, N=12→≤3, N=10→≤3）。
- 評分表欄位：`評分項目（共 N 項） | 0 沒有做到 | 1 部分做到 | 2 完全做到 | 註解`，欄寬 8.0 / 1.6 / 1.6 / 1.6 / 1.4 cm。官方範本預印「滿分：30分」只對應 15 項，N 不同時務必改寫。
- 整體表現 5 等第：差1分／待加強2分／普通3分／良好4分／優秀5分。

**敘事醫學評分（非醫學職類可選）**

- 每個計分向度四級：優異（4分）／熟練（3分）／發展中（2分）／未達標準（1分）；**滿分 12 分**。
- 向度1：全心傾聽與病患故事探索（Attention: Eliciting Illness Narrative）——能否辨識病人隱含的情緒暗號（Cues），探詢疾病對日常生活、家庭角色與心靈負擔的衝擊，營造安全包容的傾聽氛圍。
- 向度2：同理共鳴與處境再現（Representation: Empathic Resonance & Reflection）——能否以反思性同理精準回饋病人的焦慮與脆弱，讓病人感受到自己的痛苦被看見與理解。
- 向度3：關係締結與共同照護同盟（Affiliation: Relational Alliance & Shared Care）——能否平權互動、尊重病人價值觀，把專業建議融入病人真實生活，締結可行的照護同盟。
- 向度4：考官質性敘事觀察與反思回饋（Narrative Observation & Qualitative Feedback）——考官記錄關鍵互動片段（Critical Incidents）與反思引導回饋（Reflective Feedback），作為測驗後 debriefing 教材。**不計分。**
- 另附整體表現 5 等第。規準全文見 `references/narrative-rubric.md`。

**SP 提問**

- SP 主動提問 **≤5 題**，其中會觸及評分項目的 **≤2 題**。
- 提問押在**考生完成主要說明之後**（或明顯停頓時），SP 不得主導會談。
- 劇本對白例句表（三欄：`病歷架構 | 醫師對 SP 說的話 | SP 的回應或提問`，欄寬 3.5 / 6.5 / 5.5 cm）至多 **2 列**寫成提問，其餘列只寫「回應」。
- 提問若觸及評分項目，評分說明須註明「經 SP 提問後才說明者，最多給 1 分（部份做到）」。

**站型紅線**

- **病史詢問站**：LQQOPERA 群組 ≤30%，把分數留給鑑別線索、危險因子、ICE。
- **身體檢查站**：腹部依 視診→聽診→叩診→觸診（**聽診在叩、觸之前**）。
- **醫病溝通與衛教站**、**病情解釋及臨床處置站**：**Teach-back 不可省略**。
- 全部站型：8 分鐘可完成；鑑別診斷 ≥3 個；提示卡 ≤3 張；檢查報告 A4 ≤3 頁（純文字 ≤2 頁）；考生指引測驗主題 ≤3 個紅色 ●；背景資料與告示牌病患資訊各 ≤30 字；不放真實病人識別資料。

**範本檔名**

- 病史詢問：`1.試題參考格式-空白+例句(SP  病史詢問).docx`
- 身體檢查：`2.試題參考格式-空白+例句(SP  身體檢查).docx`
- 醫病溝通與衛教：`3.試題參考格式-空白+例句(SP  醫病溝通與衛教).docx`
- 病情解釋及臨床處置：`4.試題參考格式-空白+例句(SP  病情解釋及臨床處置).docx`
<!-- END GENERATED: hard-spec -->

---

## 已知待辦

`stations/` 中 **2026-07 之前產出的教案**採舊字級（全文 12pt、告示牌 36／24pt），**不符官方規格**，送審前需調整。目前僅 `一般外科_腹痛病情解釋_OSCE試題.docx` 已套用正確字級。

---

## 產出環境備註

- .docx 產出使用 **PowerShell + Microsoft Word COM**
- 編輯 .docx 使用 Word COM 或 python-docx；python-pptx 用於 .pptx。修改後另做逐頁版面檢查。
- COM 可用性需在當前機器檢查。只管理本次建立的文件，不強制結束其他 Word 工作階段。

## 改規則與部署

先讀 [`AGENTS.md`](AGENTS.md)。簡單說：

1. 數字改 `rules.yaml`，流程與說明改 `skill/SKILL.md` 的手寫段落。
2. `python scripts/build_docs.py` 重新產生 GENERATED 區塊；`python -B -m unittest discover -s tests` 跑測試。
3. 開 PR，合併後部署：

```powershell
# 預設唯讀，列出每個目標會改什麼
.\sync-skill.ps1 -ContextRoot '<本機 Context Repo>'
# 實際部署到 ~/.claude/skills、~/.codex/skills 與 Context Repo
.\sync-skill.ps1 -ContextRoot '<本機 Context Repo>' -Apply
# 第一次接管從未被本工具部署過的副本（被取代的檔案先備份到 .sync-backups/）
.\sync-skill.ps1 -ContextRoot '<本機 Context Repo>' -Apply -Adopt
```

部署過的副本若被手改，工具整批拒絕、不寫入任何檔案——那代表有人繞過正本，先把改動併回 `skill/`。
`-Adopt` 不會覆蓋這種情況。Context Repo 那一份部署後要在 Context Repo 另外 commit。

範本依序使用 `-TemplateRoot`、registry 解析的雲端範本、repo `templates/`；缺少四種站型範本時停止。
部署會產生 `deployment.local.json`，讓已安裝的 skill 找到實際的 template_dir、output_dir、runtime_dir。
本機指標、`.sync-state.json` 與 `.sync-backups/` 不進 Git。

需要 Python 3.10+ 與 `pip install -r requirements.txt`（PyYAML）。

- Windows PowerShell 5.1 **不支援 `` `u3000 `` 這類 Unicode 逸出**，特殊字元（□ ■ ℃ μ ’ …）須直接輸入真字元
