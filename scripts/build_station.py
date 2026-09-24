"""Build a TAME-format OSCE station .docx from a structured station file.

    python scripts/build_station.py examples/example_station.yaml -o out/example.docx

The station file holds the content (see examples/example_station.yaml); every
format number - font sizes, column widths, page, examiner prompts, dialogue
headers - comes from rules.yaml. Page setup and styles are taken from the matching
official TAME template, so the file opens with the template's fonts and paper.

Runs anywhere Python and python-docx run; no Word needed. Refuses to overwrite an
existing file: revisions get a new name. Validate the result with
validate_station.py and still look at every rendered page before it is used.
"""
from __future__ import annotations

import argparse
import copy
import sys
from pathlib import Path

import docx
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

sys.path.insert(0, str(Path(__file__).resolve().parent))
import osce_rules  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
RED = RGBColor(0xFF, 0x00, 0x00)
HEADER_FILL = "D9E2F3"
NUMERALS = "一二三四五"


class StationError(ValueError):
    pass


def load_station(path: Path) -> dict:
    import yaml
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def blank_from_template(template: Path, rules: dict):
    """The template's styles and page, with its example content removed."""
    document = docx.Document(str(template))
    body = document.element.body
    for child in list(body):
        if child.tag != qn("w:sectPr"):
            body.remove(child)
    section = document.sections[0]
    margin = Cm(rules["page"]["margin_cm"])
    section.left_margin = section.right_margin = section.top_margin = section.bottom_margin = margin
    normal = document.styles["Normal"]
    normal.font.size = Pt(rules["fonts_pt"]["body"])
    fmt = normal.paragraph_format
    fmt.space_before = fmt.space_after = Pt(0)
    fmt.line_spacing = 1.0
    return document


class Writer:
    def __init__(self, document, rules):
        self.d = document
        self.rules = rules
        self.f = rules["fonts_pt"]
        self.sections = 0

    def para(self, text="", size=None, bold=False, red=False, align=None):
        p = self.d.add_paragraph()
        if align is not None:
            p.alignment = align
        if text:
            run = p.add_run(text)
            run.font.size = Pt(size or self.f["body"])
            run.bold = bold
            if red:
                run.font.color.rgb = RED
        return p

    def heading(self, name):
        self.para(f"{NUMERALS[self.sections]}、{name}", self.f["section_title"], bold=True)
        self.sections += 1

    def page_break(self):
        self.d.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    def table(self, rows, widths_cm, header=True, size=None):
        table = self.d.add_table(rows=len(rows), cols=len(widths_cm))
        table.style = self._grid_style()
        self.grid(table)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        for r, values in enumerate(rows):
            for c, value in enumerate(values):
                cell = table.cell(r, c)
                cell.width = Cm(widths_cm[c])
                cell.text = ""
                run = cell.paragraphs[0].add_run(str(value))
                run.font.size = Pt(size or self.f["body"])
                if header and r == 0:
                    run.bold = True
                    self._shade(cell)
        total = sum(widths_cm)
        limit = self.rules["page"]["table_width_max_cm"]
        if total > limit + 1e-6:
            raise StationError(f"表格總寬 {total} cm 超過 {limit} cm")
        self.para()
        return table

    def _grid_style(self):
        # The TAME templates define no table grid style, so borders are set on each
        # table instead (see grid()); a style is used only if one happens to exist.
        for name in ("Table Grid", "表格格線", "表格 格線 1"):
            try:
                return self.d.styles[name]
            except KeyError:
                continue
        return None

    @staticmethod
    def grid(table):
        """0.5 pt single borders on every edge, independent of any style."""
        pr = table._tbl.tblPr
        borders = OxmlElement("w:tblBorders")
        for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
            line = OxmlElement(f"w:{edge}")
            line.set(qn("w:val"), "single")
            line.set(qn("w:sz"), "4")
            line.set(qn("w:space"), "0")
            line.set(qn("w:color"), "000000")
            borders.append(line)
        pr.append(borders)

    @staticmethod
    def _shade(cell):
        pr = cell._tc.get_or_add_tcPr()
        shd = OxmlElement("w:shd")
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), HEADER_FILL)
        pr.append(shd)


def checkboxes(rules, chosen):
    return "　".join(("■ " if key == chosen else "□ ") + v["name"] for key, v in rules["station_types"].items())


def check_station(s: dict, rules: dict):
    """Refuse content that breaks a hard rule before anything is written."""
    lim = rules["limits"]
    problems = []
    if s["station_type"] not in rules["station_types"]:
        problems.append(f"station_type 必須是 {list(rules['station_types'])}")
    if len(s["sign"]) > lim["sign_patient_info_chars"]:
        problems.append(f"告示牌病患資訊 {len(s['sign'])} 字，上限 {lim['sign_patient_info_chars']}")
    if len(s["candidate"]["background"]) > lim["candidate_background_chars"]:
        problems.append(f"背景資料 {len(s['candidate']['background'])} 字，上限 {lim['candidate_background_chars']}")
    if len(s["candidate"]["tasks"]) > lim["candidate_tasks_max"]:
        problems.append(f"測驗主題 {len(s['candidate']['tasks'])} 個，上限 {lim['candidate_tasks_max']}")
    if len(s["examiner"]["differentials"]) < lim["differentials_min"]:
        problems.append(f"鑑別診斷少於 {lim['differentials_min']} 個")
    mode = s.get("rubric", "checklist")
    if mode == "checklist":
        c = rules["checklist"]
        n = len(s["checklist"])
        stars = sum(1 for i in s["checklist"] if i.get("star"))
        if not c["items_min"] <= n <= c["items_max"]:
            problems.append(f"評分項目 {n} 項，範圍 {c['items_min']}–{c['items_max']}")
        if not c["high_discrimination_min"] <= stars <= c["high_discrimination_max"]:
            problems.append(f"★ {stars} 項，範圍 {c['high_discrimination_min']}–{c['high_discrimination_max']}")
    questions = sum(1 for row in s["sp"]["dialogue"] if row.get("question"))
    if questions > rules["sp"]["dialogue_question_rows_max"]:
        problems.append(f"對白表提問列 {questions} 列，上限 {rules['sp']['dialogue_question_rows_max']}")
    if rules["station_types"].get(s["station_type"], {}).get("teach_back_required"):
        if not any("teach" in row.get("frame", "").lower() or "回述" in row.get("frame", "")
                   for row in s["sp"]["dialogue"]):
            problems.append("溝通／病情解釋站需要 Teach-back 對白列（frame 寫 Teach-back）")
    if problems:
        raise StationError("教案內容違反硬規格：\n- " + "\n- ".join(problems))


def build(station: dict, rules: dict, template_dir: Path):
    check_station(station, rules)
    stype = rules["station_types"][station["station_type"]]
    template = template_dir / stype["template"]
    if not template.is_file():
        raise StationError(f"找不到範本：{template}")
    w = Writer(blank_from_template(template, rules), rules)
    f = rules["fonts_pt"]
    cand = station["candidate"]

    # 一、告示牌
    w.heading("告示牌")
    sign = w.d.add_table(rows=2, cols=1)
    sign.style = w._grid_style()
    w.grid(sign)
    sign.alignment = WD_TABLE_ALIGNMENT.CENTER
    number = str(station.get("number") or "").strip() or "　　"   # blank: filled in on exam day
    for row, (text, size) in enumerate(((f"第{number}站", f["sign_station_number"]),
                                         (station["sign"], f["sign_patient_info"]))):
        cell = sign.cell(row, 0)
        cell.width = Cm(rules["page"]["table_width_max_cm"])
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = cell.paragraphs[0].add_run(text)
        run.font.size = Pt(size)
        run.bold = True
    w.page_break()

    # 二、考生指引
    w.heading("考生指引")
    w.para(f"■背景資料：{cand['background']}", f["candidate_body"])
    w.para("■測驗主題：", f["candidate_body"])
    for task in cand["tasks"]:
        w.para(f"● {task}", f["candidate_body"], red=True)
    for note in cand.get("notes", []):
        w.para(f"※ {note}", f["candidate_body"])
    w.para(f"■測驗時間：{rules['station']['minutes']} 分鐘", f["candidate_body"])
    w.para("■相關檢查報告", f["candidate_body"])
    w.para("（黏貼固定於診間桌面上）", f["room_documents"])
    report = cand["report"]
    w.table([[f"生命徵象：{report['vitals']}", f"主要症狀：{report['symptoms']}"],
             [f"過去病史：{report.get('history', '須由考生自行詢問')}",
              f"藥物史：{report.get('medications', '須由考生自行詢問')}"],
             [report.get("other", ""), report.get("other_2", "")]],
            [8.5, 8.5], header=False, size=f["room_documents"])
    w.page_break()

    # 三、評分表
    w.heading("評分表")
    mode = station.get("rubric", "checklist")
    if mode == "checklist":
        n = len(station["checklist"])
        w.para(f"滿分：{2 * n} 分", f["score_header"], bold=True)
    else:
        w.para(f"評量方式：敘事醫學質性評量規準（滿分 {osce_rules.narrative_total(rules)} 分）",
               f["score_header"], bold=True)
    w.para("總得分：　　　 分", f["score_header"])
    w.para("准考證編號：")
    w.para("本題測驗項目：" + checkboxes(rules, station["station_type"]))
    w.para(f"測驗時間：{rules['station']['minutes']} 分鐘")
    if mode == "checklist":
        header = [rules["checklist"]["columns"][0].replace("N", str(n))] + rules["checklist"]["columns"][1:]
        rows = [header] + [[f"{i}. {'★' if item.get('star') else ''}{item['text'].lstrip('★')}", "", "", "", ""]
                           for i, item in enumerate(station["checklist"], 1)]
        w.table(rows, rules["checklist"]["columns_cm"])
    else:
        nar = rules["narrative"]
        levels = [f"{name} ({score}分)" for score, name in sorted(nar["levels"].items(), reverse=True)]
        rows = [["敘事評量向度"] + levels]
        for dim in nar["scored_dimensions"]:
            anchors = station["narrative"][dim["name"]]
            rows.append([dim["name"]] + [anchors[level] for level in ("4", "3", "2", "1")])
        w.table(rows, nar["columns_cm"])
        w.table([["關鍵互動觀察紀錄（Critical Incidents）", "質性反思與教學回饋建議（Reflective Feedback）"],
                 ["", ""]], [8.5, 8.5])
    names = rules["global_rating"]
    w.para("您認為考生整體表現如何：")
    w.table([["整體表現"] + [f"{name} {i}分" for i, name in enumerate(names, 1)], [""] * (len(names) + 1)],
            [2.0] + [3.0] * len(names))
    w.para("※試評考官認為本題難易度：" + "　".join("□" + d for d in rules["station"]["difficulty"]))
    w.para("評分考官簽名：", f["score_header"])
    w.page_break()

    # 四、考官指引
    ex = station["examiner"]
    w.heading("考官指引")
    w.para("本題測驗項目：" + checkboxes(rules, station["station_type"]))
    w.para("考官任務提示", bold=True)
    for i, prompt in enumerate(rules["station"]["examiner_prompts"], 1):
        w.para(f"{i}. {prompt}")
    w.para(f"測驗場景：{ex['setting']}")
    w.para(f"標準化病人基本資料：{ex['sp_profile']}")
    w.para(f"標準化病人起始姿勢：{ex['start_position']}")
    w.para("病情摘要", bold=True)
    w.para(ex["summary"])
    w.para("鑑別診斷／照護焦點（依可能性排序）", bold=True)
    for i, dx in enumerate(ex["differentials"], 1):
        w.para(f"{i}. {dx}")
    w.para(f"道具：{ex.get('props', '無')}")
    if mode == "checklist":
        w.para("評分說明", bold=True)
        cap = rules["sp"]["prompted_item_score_cap"]
        for i, item in enumerate(station["checklist"], 1):
            w.para(f"{i}. {item['text']}", bold=True)
            for level, label in (("2", "完全做到"), ("1", "部分做到"), ("0", "沒有做到")):
                w.para(f"　{label}：{item['anchors'][level]}")
            if item.get("sp_prompted"):
                w.para(f"　※ 經 SP 提問後才說明者，最多給 {cap} 分（部份做到）。")
    w.para("SP 劇本摘要", bold=True)
    w.para(station["sp"]["summary"])
    w.page_break()

    # 五、SP 指引
    sp = station["sp"]
    w.heading("SP 指引（劇本）")
    for label, key in (("場景", "setting"), ("起始姿勢", "start_position"), ("情緒", "emotion"),
                       ("表情與肢體", "manner"), ("說話風格", "voice")):
        w.para(f"{label}：{sp[key]}")
    w.para(f"■人員／道具：{sp.get('props', ex.get('props', '無'))}", red=True)
    w.para("回應考生原則", bold=True)
    w.para(sp["principles"])
    w.para("劇情摘要", bold=True)
    w.para(sp["summary"])
    w.para("劇本對白例句", bold=True)
    columns = rules["sp"]["dialogue_columns"][:2] + [stype["dialogue_third_column"]]
    w.table([columns] + [[row["frame"], row["candidate"], row["sp"]] for row in sp["dialogue"]],
            rules["sp"]["dialogue_columns_cm"])
    w.para("診間示意圖", bold=True)
    w.table([[sp["room_diagram"]]], [rules["page"]["table_width_max_cm"]], header=False)
    return w.d


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("station")
    parser.add_argument("-o", "--output", required=True)
    parser.add_argument("--template-dir", default=str(REPO / "templates"))
    args = parser.parse_args(argv)
    output = Path(args.output)
    if output.exists():
        print(f"{output} 已存在；修訂請用新檔名，不覆蓋。", file=sys.stderr)
        return 2
    try:
        document = build(load_station(Path(args.station)), osce_rules.load(), Path(args.template_dir))
    except StationError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    output.parent.mkdir(parents=True, exist_ok=True)
    document.save(str(output))
    print(f"已產出 {output}。下一步：python scripts/validate_station.py \"{output}\"，並逐頁看渲染結果。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
