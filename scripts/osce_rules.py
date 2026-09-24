"""Load rules.yaml and render the hard-spec text every document shares.

One source for every number a station is checked against. Documents keep their own
prose - the skill is written for an agent, SKILL_GPT.md for a free web model, the
README for a person - but the numbers inside them come from here.
"""
from __future__ import annotations

import math
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
RULES = REPO / "rules.yaml"


def load(path: Path = RULES) -> dict:
    try:
        import yaml
    except ImportError as exc:  # pragma: no cover - environment message
        raise SystemExit("需要 PyYAML：pip install -r requirements.txt") from exc
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def lqqopera_max(rules: dict, n: int) -> int:
    return math.floor(n * rules["station_types"]["history"]["lqqopera_max_fraction"])


def main_construct_min(rules: dict, n: int) -> int:
    return math.ceil(n * rules["checklist"]["main_construct_min_fraction"])


def narrative_total(rules: dict) -> int:
    return len(rules["narrative"]["scored_dimensions"]) * max(rules["narrative"]["levels"])


def fonts_table(rules: dict) -> str:
    f = rules["fonts_pt"]
    rows = [
        ("告示牌 站次號「第　站」", f["sign_station_number"], "粗體置中；考生在門口遠距閱讀"),
        (f"告示牌 病患資訊（≤{rules['limits']['sign_patient_info_chars']} 字）",
         f["sign_patient_info"], "粗體置中"),
        ("考生指引本體（背景、測驗主題、時間、報告標題）", f["candidate_body"], "進站前 1 分鐘要讀完"),
        ("五大部分標題", f["section_title"], "粗體"),
        ("診間文件／檢查報告內容", f["room_documents"], "黏貼於診間桌面"),
        ("評分表 滿分／總得分／考官簽名", f["score_header"], ""),
        ("其餘內文、表格、考官指引、SP 指引", f["body"], "Normal 樣式"),
    ]
    lines = ["| 元素 | 字級 | 說明 |", "|---|---|---|"]
    lines += [f"| {name} | **{size}pt** | {note} |" for name, size, note in rows]
    return "\n".join(lines)


def checklist_rules(rules: dict) -> str:
    c = rules["checklist"]
    n = c["items_default"]
    lq = ", ".join(f"N={k}→≤{lqqopera_max(rules, k)}" for k in (15, 12, 10))
    return "\n".join([
        f"- 共 **N 項**，N 於階段一確認（國考型建議 {n} 項，其他 {c['items_min']}–{c['items_max']} 項）；"
        f"每項 {'／'.join(c['levels'])}，**滿分＝N×2 分**。",
        f"- ★高鑑別力 **{c['high_discrimination_min']}–{c['high_discrimination_max']} 項**；"
        f"共通／通用項目 **≤{c['generic_items_max']} 項**；"
        f"主要評分範圍 **≥{int(c['main_construct_min_fraction'] * 100)}%**（至少 ⌈N/2⌉ 項，N={n} 時 ≥{main_construct_min(rules, n)}）；"
        f"子項目 **≤{c['sub_items_max']}**。",
        f"- 病史站 LQQOPERA 群組 **≤{int(rules['station_types']['history']['lqqopera_max_fraction'] * 100)}%**（{lq}）。",
        f"- 評分表欄位：`{' | '.join(c['columns'])}`，欄寬 {' / '.join(str(w) for w in c['columns_cm'])} cm。"
        f"官方範本預印「滿分：30分」只對應 {n} 項，N 不同時務必改寫。",
        f"- 整體表現 5 等第：{'／'.join(f'{name}{i}分' for i, name in enumerate(rules['global_rating'], 1))}。",
    ])


def sp_rules(rules: dict) -> str:
    s = rules["sp"]
    return "\n".join([
        f"- SP 主動提問 **≤{s['questions_max']} 題**，其中會觸及評分項目的 **≤{s['scoring_questions_max']} 題**。",
        "- 提問押在**考生完成主要說明之後**（或明顯停頓時），SP 不得主導會談。",
        f"- 劇本對白例句表（三欄：`{' | '.join(s['dialogue_columns'])}`，"
        f"欄寬 {' / '.join(str(w) for w in s['dialogue_columns_cm'])} cm）"
        f"至多 **{s['dialogue_question_rows_max']} 列**寫成提問，其餘列只寫「回應」。",
        f"- 提問若觸及評分項目，評分說明須註明「經 SP 提問後才說明者，最多給 {s['prompted_item_score_cap']} 分（部份做到）」。",
    ])


def station_red_lines(rules: dict) -> str:
    t = rules["station_types"]
    order = "→".join(t["physical"]["abdomen_order"])
    lim = rules["limits"]
    return "\n".join([
        f"- **{t['history']['name']}站**：LQQOPERA 群組 ≤{int(t['history']['lqqopera_max_fraction'] * 100)}%，"
        "把分數留給鑑別線索、危險因子、ICE。",
        f"- **{t['physical']['name']}站**：腹部依 {order}（**聽診在叩、觸之前**）。",
        f"- **{t['communication']['name']}站**、**{t['explanation']['name']}站**：**Teach-back 不可省略**。",
        f"- 全部站型：{rules['station']['minutes']} 分鐘可完成；鑑別診斷 ≥{lim['differentials_min']} 個；"
        f"提示卡 ≤{lim['cue_cards_max']} 張；檢查報告 A4 ≤{lim['report_pages_max']} 頁（純文字 ≤{lim['text_report_pages_max']} 頁）；"
        f"考生指引測驗主題 ≤{lim['candidate_tasks_max']} 個紅色 ●；背景資料與告示牌病患資訊各 ≤{lim['candidate_background_chars']} 字；"
        "不放真實病人識別資料。",
    ])


def narrative_rules(rules: dict) -> str:
    n = rules["narrative"]
    levels = "／".join(f"{name}（{score}分）" for score, name in sorted(n["levels"].items(), reverse=True))
    lines = [f"- 每個計分向度四級：{levels}；**滿分 {narrative_total(rules)} 分**。"]
    for i, d in enumerate(n["scored_dimensions"], 1):
        lines.append(f"- 向度{i}：{d['name']}（{d['en']}）——{d['focus']}")
    fb = n["feedback_dimension"]
    lines.append(f"- 向度{len(n['scored_dimensions']) + 1}：{fb['name']}（{fb['en']}）——{fb['focus']}**不計分。**")
    lines.append("- 另附整體表現 5 等第。規準全文見 `references/narrative-rubric.md`。")
    return "\n".join(lines)


def fonts_line(rules: dict) -> str:
    f = rules["fonts_pt"]
    return (f"字級（TAME 官方，不可縮小）：告示牌站次號 {f['sign_station_number']}pt、病患資訊 {f['sign_patient_info']}pt；"
            f"考生指引本體 {f['candidate_body']}pt；五大部分標題 {f['section_title']}pt；"
            f"診間文件與評分表滿分列 {f['room_documents']}pt；其餘 {f['body']}pt。")


def hard_spec(rules: dict) -> str:
    """The full block used by SKILL.md and the README."""
    page = rules["page"]
    return "\n\n".join([
        f"**頁面**：{page['paper']}，四邊 {page['margin_cm']} cm，表格總寬 ≤{page['table_width_max_cm']} cm。"
        f"五大部分：{'／'.join(rules['station']['sections'])}。測驗時間 {rules['station']['minutes']} 分鐘。",
        "**字級（TAME 官方，不可自行縮小）**\n\n" + fonts_table(rules),
        "**條列式評分（醫學系預設）**\n\n" + checklist_rules(rules),
        "**敘事醫學評分（非醫學職類可選）**\n\n" + narrative_rules(rules),
        "**SP 提問**\n\n" + sp_rules(rules),
        "**站型紅線**\n\n" + station_red_lines(rules),
        "**範本檔名**\n\n" + "\n".join(
            f"- {v['name']}：`{v['template']}`" for v in rules["station_types"].values()),
    ])


def gpt_spec(rules: dict) -> str:
    """Compact version for a free web model; no file paths, no references."""
    return "\n\n".join([
        "【" + fonts_line(rules).replace("：", "】", 1),
        "【條列式評分】\n" + checklist_rules(rules),
        "【敘事醫學評分】\n" + narrative_rules(rules).replace(
            "規準全文見 `references/narrative-rubric.md`。", "每向度需寫出四級錨點描述。"),
        "【SP 防呆紅線】\n" + sp_rules(rules),
        "【站型紅線】\n" + station_red_lines(rules),
    ])


def prompt_tail(rules: dict) -> str:
    """What a generated authoring prompt adds after its own rubric section."""
    return "\n".join(["- " + fonts_line(rules), station_red_lines(rules)])
