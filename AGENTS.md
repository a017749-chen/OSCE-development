# AGENTS.md — OSCE-development

寫給在這個 repo 工作的每一個 agent（Claude Code、Codex 或其他）。擁有者可以覆寫任何一條；
agent 不行。有衝突時先停下來問。

## 正本在哪裡

- **`skill/SKILL.md` 是 osce-item-development skill 的唯一正本。**
  `~/.claude/skills/`、`~/.codex/skills/`、`YiChan-Context-Repo/.agents/skills/` 都是部署出來的副本，
  **不要直接改副本**——改了下次部署會被擋下，而且會讓三份再次分歧（2026-09-24 之前就是這樣）。
- **`rules.yaml` 是所有數字的唯一來源**：字級、項目數、★、SP 提問上限、LQQOPERA、字數、頁數、範本檔名。
  `skill/SKILL.md`、`SKILL_GPT.md`、`README.md` 裡 `BEGIN GENERATED` 到 `END GENERATED` 之間的文字，
  以及 `scripts/grill_me.py` 產生的出題 Prompt，全部從它來。**不要手改 GENERATED 區塊。**

## 改規則的流程

1. 改 `rules.yaml`（數字）或 `skill/SKILL.md` 的手寫段落（流程、判斷、說明）。
2. `python scripts/build_docs.py` —— 重新產生所有 GENERATED 區塊。
3. `python -B -m unittest discover -s tests` —— CI 也會跑 `build_docs.py --check`。
4. 開 PR，不直接推 main。
5. 合併後部署：`.\sync-skill.ps1 -ContextRoot <Context Repo>`（預設唯讀，看清楚再加 `-Apply`）。
   Context Repo 那一份會變成 Context Repo 的變更，要在那邊另外 commit。

`-Adopt` 只用在**從未被這個工具部署過**的副本（沒有 `.sync-state.json`），被取代的檔案會先備份到
`.sync-backups/`。部署過之後又被手改的副本，`-Adopt` 也不會覆蓋——那代表有人繞過正本，要先把改動併回來。

## 出題時

- 依 `skill/SKILL.md` 的三階段走：先藍圖確認卡，再草擬，最後產檔與檢核。
- 產檔：內容寫成 YAML（照 `examples/example_station.yaml`）→ `scripts/build_station.py` → `scripts/validate_station.py` 必須零 FAIL → 轉 PDF 逐頁看。
  驗證器抓不到版面問題（跨頁、切邊）；2026-09-24 就是靠逐頁看才發現表格沒有框線。
- 改了 `validate_station.py` 或 `rules.yaml` 就重新產生 `stations/STATUS.md`。
- 範本在 `templates/`（TAME 官方格式，著作權屬該學會）。repo 保持 private；擁有者 2026-09-28 決定可以分享給院內外的出題者（加 GitHub 協作者或給 `SKILL_GPT.md`／`teaching/`），但不公開張貼。
- **不覆蓋既有教案**：`stations/` 裡的檔案是擁有者手改過的成品。修訂一律存成新檔名。
- 新教案檔名：`科別_主題_站型_OSCE試題_vN.docx`，一律正體字（「內科」不是「内科」）。

## 不可以做的事

- 不放真實病人識別資料、審題委員意見、機構敏感資料（`.gitignore` 已擋下幾種常見檔名，但不能只靠它）。
- 不強制結束使用者的 Word（不要 `Stop-Process WINWORD`）；只操作本次建立的 COM 物件。
- 不把 TAME 範本或教案推到公開位置。

## 已知待辦

- `stations/STATUS.md`：16 份中 15 份仍是舊字級；另有 4 份溝通／病情解釋站的 SP 對白表有 3–7 列提問
  （上限 2），1 份沒有表格框線，4 份背景資料超過 30 字，1 份沒有三欄對白表。擁有者決定要修哪幾份。
- 敘事醫學評分：舊文件寫「滿分 16 分」，但只有三個計分向度（第四向度是質性回饋不計分），
  依 `rules.yaml` 為 12 分。若擁有者本意是四向度都計分，改 `rules.yaml` 即可。
- `D:\osce-item-development` 是本 repo 的舊 clone（落後），擁有者決定是否移除；不要在那裡工作。
