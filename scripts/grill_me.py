#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OSCE Grill Me 訪談與出題專用 Prompt 生成器 (OSCE Prompt Generator)

協助出題教師透過結構化訪談（Grill Me 模式）釐清臨床背景、職類定位與評量模式，
並自動編譯產出專屬的《OSCE 出題 Prompt》，可直接複製貼入各大 LLM 或直接啟動出題。
支援：
1. 醫學系（醫師／醫學生）：TAME 官方條列式評分（0/1/2 錨點，滿分 N×2）
2. 非醫學職類（護理、藥學、復健、醫技等）：條列式評分 或 敘事醫學方式評分（全人照護質性規準）
"""

from __future__ import annotations

import argparse
import sys
from typing import Any, Dict


PROFESSIONS = [
    "醫學系／醫師",
    "護理學系／護理師",
    "藥學系／藥師",
    "物理治療學系／物理治療師",
    "職能治療學系／職能治療師",
    "呼吸治療學系／呼吸治療師",
    "營養學系／營養師",
    "醫事檢驗學系／醫檢師",
    "醫事放射學系／放射師",
    "臨床心理學系／心理師",
    "醫務社會工作／社工師",
    "其他醫事職類",
]

STATION_TYPES = [
    "病史詢問站",
    "身體檢查／技術操作站",
    "醫病溝通與衛教站",
    "病情解釋及臨床處置站",
    "全人跨團隊照護站",
]

SCENARIOS = ["門診診間", "急診檢傷／急救室", "一般病房", "加護病房", "處置室／手術室", "衛教室", "社區／居家訪視"]


def is_medical_profession(profession: str) -> bool:
    """判斷是否為醫學系/醫師職類"""
    return "醫學系" in profession or "醫師" in profession


def build_osce_prompt(config: Dict[str, Any]) -> str:
    """根據訪談收集的配置參數，編譯組裝出完整的《OSCE 出題專用 Prompt》"""
    profession = config.get("profession", "醫學系／醫師")
    rubric_type = config.get("rubric_type", "checklist")  # "checklist" or "narrative"
    station_type = config.get("station_type", "醫病溝通與衛教站")
    learner_level = config.get("learner_level", "國考考生／PGY")
    specialty_topic = config.get("specialty_topic", "一般醫學")
    chief_complaint = config.get("chief_complaint", "主訴未填寫")
    scene = config.get("scene", "門診診間")
    time_limit = config.get("time_limit", "8 分鐘")
    
    primary_objective = config.get("primary_objective", "能進行系統性評估並展現同理溝通")
    core_task = config.get("core_task", "完成臨床評估並與病患討論後續照護方針")
    target_competencies = config.get("target_competencies", "病人照護、溝通同理、專業素養")
    primary_focus = config.get("primary_focus", "主要臨床診斷或照護焦點")
    differentials_or_context = config.get("differentials_or_context", "鑑別診斷或家庭社會生活脈絡")
    
    # 臨床素材
    history_clues = config.get("history_clues", "無特殊提示")
    findings = config.get("findings", "無特殊提示")
    reports = config.get("reports", "基本生命徵象")
    high_discrimination = config.get("high_discrimination", "關鍵同理或關鍵鑑別步驟")
    
    # 執行細節
    personnel = config.get("personnel", "SP、考官")
    sp_profile = config.get("sp_profile", "焦慮但配合之病患")
    emotional_cues = config.get("emotional_cues", "擔心生活自理能力與家庭負擔")
    item_count = config.get("item_count", 15)
    
    lines = []
    lines.append("# OSCE 出題專用 Prompt（已填入背景與規格設定）")
    lines.append("")
    lines.append("> 請複製下方整段文字，貼入支援繁體中文之 AI 大模型（如 Claude, ChatGPT, Gemini），系統即可直接依設定輸出完整五大部分之教案。")
    lines.append("")
    lines.append("```markdown")
    lines.append("幫我出一題 OSCE 專業教案，請嚴格依照台灣醫學教育學會（TAME）格式與 114 年度國考型標準規範開發。")
    lines.append("")
    lines.append("【一、職類與核心定位】")
    lines.append(f"- 考評職類：{profession}")
    lines.append(f"- 評分模式：{'敘事醫學方式評分（全人照護四大向度質性規準＋考官質性觀察回饋）' if rubric_type == 'narrative' else f'TAME 官方條列式評分（{item_count} 項 × 0/1/2 分，滿分 {item_count*2} 分）'}")
    lines.append(f"- 站型：{station_type}")
    lines.append(f"- 學員程度：{learner_level}")
    lines.append(f"- 科別與主題：{specialty_topic}")
    lines.append(f"- 病患主訴與年齡性別：{chief_complaint}")
    lines.append(f"- 測驗場景：{scene}")
    lines.append(f"- 測驗時間：{time_limit}")
    lines.append("")
    lines.append("【二、評量設計與核心目標】")
    lines.append(f"- 主要評量目標：{primary_objective}")
    lines.append(f"- 考生核心任務（{time_limit}內完成）：{core_task}")
    lines.append(f"- 目標能力領域：{target_competencies}")
    lines.append(f"- 臨床焦點／主診斷：{primary_focus}")
    lines.append(f"- 鑑別診斷／生活情境脈絡（≥3項）：{differentials_or_context}")
    lines.append("")
    lines.append("【三、臨床素材與生活世界（Lifeworld）】")
    lines.append(f"- 關鍵病史／照護危險因子：{history_clues}")
    lines.append(f"- 重要檢查發現（陽性／陰性）：{findings}")
    lines.append(f"- 診間文件／檢查報告：{reports}")
    lines.append(f"- 高鑑別力（★）考核重點：{high_discrimination}")
    lines.append(f"- 病人／家屬隱含情緒暗號與生活困境（Cues）：{emotional_cues}")
    lines.append("")
    lines.append("【四、執行人員與 SP 設定】")
    lines.append(f"- 必要人員與道具：{personnel}")
    lines.append(f"- SP 人設、情緒與起始姿態：{sp_profile}")
    lines.append("- SP 提問限制：主動發問 ≤ 5 題（其中觸及評分項目者至多 2 題）；提問必須押在考生說明告一段落後；不可讓 SP 主導會談。劇本對白例句表（三欄表格）中主動提問列至多 2 列，其餘一律只寫回應。")
    lines.append("")
    
    if rubric_type == "narrative":
        lines.append("【五、評分架構要求：敘事醫學方式評分（全人照護四大向度質性規準）】")
        lines.append("本站採用非醫學職類／全人照護專用之「敘事醫學方式評分」，不產出破碎扣分式的 0/1/2 條列打勾，改採 Rita Charon 敘事醫學四大核心向度質性評量規準（Holistic Rubric）：")
        lines.append("1. 向度一：全心傾聽與病患故事探索（Attention: Eliciting Illness Narrative）")
        lines.append("   - 評核學員能否辨識病人隱含情緒暗號（Cues）、探詢疾病對日常生活與家庭之衝擊，營造安全包容之傾聽氛圍。")
        lines.append("   - 包含四級錨點：優異 (4分)、熟練 (3分)、發展中 (2分)、未達標準 (1分)。")
        lines.append("2. 向度二：同理共鳴與處境再現（Representation: Empathic Resonance & Reflection）")
        lines.append("   - 評核學員能否運用反思性同理精準回饋病人的焦慮與脆弱，讓病人感受到自己的痛苦被全然看見與理解。")
        lines.append("   - 包含四級錨點：優異 (4分)、熟練 (3分)、發展中 (2分)、未達標準 (1分)。")
        lines.append("3. 向度三：關係締結與共同照護同盟（Affiliation: Relational Alliance & Shared Care）")
        lines.append("   - 評核學員能否展現平權互動、尊重病患價值觀，將專業建議融於病患生活脈絡，締結可行的照護同盟。")
        lines.append("   - 包含四級錨點：優異 (4分)、熟練 (3分)、發展中 (2分)、未達標準 (1分)。")
        lines.append("4. 向度四：考官質性敘事觀察與反思回饋表（Narrative Observation & Qualitative Feedback）")
        lines.append("   - 考官專用欄位，記錄考生在溝通中的「關鍵互動片段（Critical Incidents）」與「質性反思學習建議」。")
        lines.append("5. 整體表現評等（Global Rating）：5 等第（優秀5分／良好4分／普通3分／待加強2分／差1分）。")
    else:
        lines.append("【五、評分架構要求：TAME 官方條列式評分】")
        lines.append(f"- 評分項目數：共 {item_count} 項，每項 0 沒有做到／1 部分做到／2 完全做到，滿分 {item_count*2} 分。")
        lines.append("- 高鑑別力項目（★）：2–5 項；共通／通用項目 ≤ 1 項；主要評分範圍佔 ≥ 50%（至少 ⌈N/2⌉ 項）。")
        lines.append("- 錨點清晰具體，為可觀察之行為指標，避免「適當地」等主觀形容詞。")
        lines.append("- 子項目 ≤ 3 個；不重複給分；不需隱性推論。")
        lines.append("- 整體表現評等（Global Rating）：5 等第（優秀5分／良好4分／普通3分／待加強2分／差1分）。")
        
    lines.append("")
    lines.append("【六、教案輸出規範（嚴格遵守 TAME 格式五大部分）】")
    lines.append("請完整輸出繁體中文之教案五大部分：")
    lines.append("1. 告示牌：站次號（48pt粗體）＋病患資訊（36pt粗體，≤30字）。")
    lines.append("2. 考生指引（本體26pt）：背景資料（≤30字）＋測驗主題（≤3個紅色●）＋測驗時間＋相關檢查報告表格（診間文件14pt）。")
    lines.append("3. 評分表：依上述評分架構要求完整輸出表格。")
    lines.append("4. 考官指引：考官任務提示＋場景與SP起始姿態＋病情摘要＋鑑別診斷/照護焦點＋評分錨點說明＋SP劇本摘要。")
    lines.append("5. SP 指引：演出說明＋回應原則＋劇情摘要＋劇本對白例句（三欄表格：病歷架構／考生對SP說的話／SP的回應或提問）＋診間配置示意圖。")
    lines.append("```")
    lines.append("")
    return "\n".join(lines)


def run_interactive_grill_me() -> None:
    """執行命令列互動式 Grill Me 訪談"""
    print("=" * 70)
    print("  OSCE 教案開發 · Grill Me 訪談與出題專用 Prompt 生成器")
    print("  支援：醫學系條列式評分 (TAME) ＆ 非醫學職類敘事醫學質性評分")
    print("=" * 70)
    print("請依照提示回答問題；若想採用預設建議，直接按 [Enter] 即可。\n")

    config: Dict[str, Any] = {}

    # 步驟 0：職類與評分模式確認
    print("【第 0 步：確認受評職類與評分模式】")
    print("請選擇出題職類：")
    for idx, p in enumerate(PROFESSIONS, 1):
        print(f"  [{idx}] {p}")
    choice = input(f"請輸入職類編號 (預設 1: {PROFESSIONS[0]}): ").strip()
    try:
        prof_idx = int(choice) - 1 if choice else 0
        if 0 <= prof_idx < len(PROFESSIONS):
            profession = PROFESSIONS[prof_idx]
        else:
            profession = PROFESSIONS[0]
    except ValueError:
        profession = choice if choice else PROFESSIONS[0]
    config["profession"] = profession
    print(f"-> 已設定職類：{profession}\n")

    if is_medical_profession(profession):
        print("醫學系／醫師職類：自動設定為「TAME 官方條列式評分（0/1/2 錨點，滿分 N×2）」")
        config["rubric_type"] = "checklist"
        item_cnt = input("請設定評分項目數 N (國考型建議 15 項，直接按 Enter 預設 15): ").strip()
        config["item_count"] = int(item_cnt) if item_cnt.isdigit() else 15
    else:
        print("非醫學職類：可依教案屬性選擇評分方式：")
        print("  [1] 敘事醫學方式評分（推薦：全人照護四大向度質性規準＋考官質性觀察回饋）")
        print("  [2] 專業條列式評分（0/1/2 項目打勾，自訂 N 項）")
        r_choice = input("請選擇評分方式 (預設 1: 敘事醫學方式評分): ").strip()
        if r_choice == "2":
            config["rubric_type"] = "checklist"
            item_cnt = input("請設定條列評分項目數 N (建議 10-15，直接按 Enter 預設 12): ").strip()
            config["item_count"] = int(item_cnt) if item_cnt.isdigit() else 12
        else:
            config["rubric_type"] = "narrative"
            config["item_count"] = 4
            print("-> 已設定為：敘事醫學方式評分（全人照護四大向度規準）")
    print()

    # 步驟 1：站次定位
    print("【第 1 步：站次定位與場景】")
    print("請選擇站型：")
    for idx, st in enumerate(STATION_TYPES, 1):
        print(f"  [{idx}] {st}")
    st_choice = input(f"請選擇站型編號 (預設 3: {STATION_TYPES[2]}): ").strip()
    try:
        st_idx = int(st_choice) - 1 if st_choice else 2
        config["station_type"] = STATION_TYPES[st_idx] if 0 <= st_idx < len(STATION_TYPES) else STATION_TYPES[2]
    except ValueError:
        config["station_type"] = st_choice if st_choice else STATION_TYPES[2]

    lvl = input("學員程度 (如: 實習生/新進人員/PGY/國考考生，預設: 國考考生／PGY): ").strip()
    config["learner_level"] = lvl if lvl else "國考考生／PGY"

    topic = input("科別與主題 (如: 護理部傷口造口照護、藥學部用藥整合諮詢、胸腔內科呼吸困難): ").strip()
    config["specialty_topic"] = topic if topic else "臨床專業核心技能與全人溝通"

    cc = input("病患主訴／核心生活困難 (包含年齡、性別，≤30字，如: 62歲男性，中風出院前對返家自我照護極度焦慮): ").strip()
    config["chief_complaint"] = cc if cc else "60歲女性，面臨重大治療決定感到徬徨焦慮"

    print("請選擇場景：")
    for idx, sc in enumerate(SCENARIOS, 1):
        print(f"  [{idx}] {sc}")
    sc_choice = input(f"場景編號 (預設 1: {SCENARIOS[0]}): ").strip()
    try:
        sc_idx = int(sc_choice) - 1 if sc_choice else 0
        config["scene"] = SCENARIOS[sc_idx] if 0 <= sc_idx < len(SCENARIOS) else SCENARIOS[0]
    except ValueError:
        config["scene"] = sc_choice if sc_choice else SCENARIOS[0]
    config["time_limit"] = "8 分鐘"
    print()

    # 步驟 2：核心評量目標與任務
    print("【第 2 步：評量設計與核心目標】")
    obj = input("主要評量目標 (一句話：考生要能「做到什麼」): ").strip()
    config["primary_objective"] = obj if obj else "能主動傾聽病患擔憂，展現同理心並共同擬定切合生活之照護計畫"

    task = input("考生 8 分鐘內的核心任務 (如: 完成傷口評估衛教並確認理解／建立服藥同盟): ").strip()
    config["core_task"] = task if task else "完成臨床照護說明、探詢生活困難並進行 Teach-back 雙向確認"

    comp = input("目標能力領域 (如: 病人照護、同理溝通、全人反思、專業技能): ").strip()
    config["target_competencies"] = comp if comp else "同理溝通、全人照護、專業素養、病人安全"

    focus = input("主要焦點／主診斷 (如: 第二型糖尿病合併末梢神經病變／腦中風後日常生活功能調適): ").strip()
    config["primary_focus"] = focus if focus else "慢性疾病調適與居家自我照護困境"

    diff = input("重要鑑別或生活共病情境 (至少 3 項，用頓號分隔): ").strip()
    config["differentials_or_context"] = diff if diff else "獨居缺乏支持系統、經濟負擔考量、對藥物副作用過度恐懼"
    print()

    # 步驟 3：臨床素材與生活世界（Lifeworld）
    print("【第 3 步：臨床素材、生活脈絡與 SP 情緒暗號】")
    clues = input("關鍵病史／照護困難線索 (如: 過去曾有跌倒史、對胰島素施打有心理抗拒): ").strip()
    config["history_clues"] = clues if clues else "過去遵從性不佳，因擔心同住長輩知情而延誤就醫"

    finds = input("重要檢查發現 (陽性或陰性發現，如: 血糖控制不佳、步態微跛但肌力 4 分): ").strip()
    config["findings"] = finds if finds else "生命徵象平穩，外觀焦慮、眼眶泛紅，雙手緊握病歷"

    reps = input("診間報告或文件 (如: 衛教單張、檢驗報告、用藥紀錄清單): ").strip()
    config["reports"] = reps if reps else "門診檢驗報告單與近期用藥清單（固定於桌上，14pt）"

    disc = input("高鑑別力考核重點 (考生拉開差距之處，如: 能察覺病人隱忍之無助感而非單向說教): ").strip()
    config["high_discrimination"] = disc if disc else "能精準辨識病人隱藏之生活恐懼，並以病人能理解之語言進行共情與賦能"

    sp = input("SP 人設、情緒與起始姿態 (如: 60歲退休教師，神情落寞，雙手抱胸，不願主動多談): ").strip()
    config["sp_profile"] = sp if sp else "60歲女性，神色凝重焦慮，語氣保守，需待考生主動關心才釋放情緒"

    emot = input("病患／家屬隱含的情緒暗號 (Cues，如: 「我不知道這樣活著還有什麼意思」): ").strip()
    config["emotional_cues"] = emot if emot else "「吃了這麼多藥，感覺自己成了家裡的累贅…」"

    person = input("現場必要人員與道具 (如: SP、考官、血糖機、衛教模型): ").strip()
    config["personnel"] = person if person else "SP、考官、診間桌椅、衛教指引單"
    print()

    # 編譯產出 Prompt
    print("=" * 70)
    print("  訪談完成！正在編譯您的《OSCE 專屬出題 Prompt》...")
    print("=" * 70)
    output_prompt = build_osce_prompt(config)

    output_filename = "OSCE_Authoring_Prompt.md"
    try:
        with open(output_filename, "w", encoding="utf-8") as f:
            f.write(output_prompt)
        print(f"\n[OK] 專屬出題 Prompt 已成功儲存至本機檔案：{output_filename}")
    except Exception as e:
        print(f"\n[Warning] 無法寫入本機檔案 ({e})，已輸出至終端機：")

    print("\n---【產出之 Prompt 內容如下（可直接複製）】---\n")
    print(output_prompt)
    print("\n" + "=" * 70)
    print("您現在可以直接複製上方文字貼入各大 AI 模型開始出題！")
    print("=" * 70)


def main() -> None:
    parser = argparse.ArgumentParser(description="OSCE Grill Me 訪談與專屬 Prompt 生成器")
    parser.add_argument("--interactive", action="store_true", default=True, help="啟動互動式訪談模式 (預設)")
    parser.add_argument("--output", "-o", help="指定輸出 Prompt 之檔案路徑")
    args = parser.parse_args()

    run_interactive_grill_me()


if __name__ == "__main__":
    main()
