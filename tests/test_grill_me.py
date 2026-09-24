#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for OSCE Grill Me prompt generator and profession/rubric branching."""

import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location(
    "grill_me", Path(__file__).resolve().parents[1] / "scripts/grill_me.py"
)
grill_me = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grill_me)


class TestGrillMePromptGenerator(unittest.TestCase):
    def test_is_medical_profession(self):
        self.assertTrue(grill_me.is_medical_profession("醫學系／醫師"))
        self.assertTrue(grill_me.is_medical_profession("一般外科醫師"))
        self.assertFalse(grill_me.is_medical_profession("護理學系／護理師"))
        self.assertFalse(grill_me.is_medical_profession("藥學系／藥師"))
        self.assertFalse(grill_me.is_medical_profession("物理治療學系／物理治療師"))
        self.assertFalse(grill_me.is_medical_profession("呼吸治療學系／呼吸治療師"))

    def test_medical_profession_checklist_prompt(self):
        config = {
            "profession": "醫學系／醫師",
            "rubric_type": "checklist",
            "item_count": 15,
            "station_type": "病史詢問站",
            "learner_level": "國考考生",
            "specialty_topic": "一般外科 急性腹痛",
            "chief_complaint": "28歲男性，突發性右下腹轉移性疼痛",
            "scene": "急診檢傷／急救室",
            "primary_objective": "能進行系統性病史詢問並做出精確鑑別診斷",
            "core_task": "完成病史詢問、危險因子探詢並擬定初步檢查方針",
            "target_competencies": "臨床推理、病人照護",
            "primary_focus": "急性闌尾炎",
            "differentials_or_context": "急性憩室炎、腎結石、泌尿道感染",
            "high_discrimination": "轉移痛時序、伴隨症狀之陰性鑑別",
            "sp_profile": "痛苦蜷曲躺於推床，呻吟但能配合回答",
        }
        prompt = grill_me.build_osce_prompt(config)

        self.assertIn("考評職類：醫學系／醫師", prompt)
        self.assertIn("TAME 官方條列式評分", prompt)
        self.assertIn("15 項 × 0/1/2 分，滿分 30 分", prompt)
        self.assertIn("★高鑑別力 **2–5 項**", prompt)
        self.assertIn("主要評分範圍 **≥50%**", prompt)
        self.assertIn("SP 主動提問 **≤5 題**", prompt)
        self.assertIn("告示牌站次號 48pt、病患資訊 36pt", prompt)
        self.assertIn("考生指引本體 26pt", prompt)
        self.assertIn("LQQOPERA 群組 **≤30%**", prompt)
        self.assertNotIn("全心傾聽與病患故事探索（Attention", prompt)

    def test_non_medical_profession_narrative_medicine_prompt(self):
        config = {
            "profession": "護理學系／護理師",
            "rubric_type": "narrative",
            "station_type": "醫病溝通與衛教站",
            "learner_level": "二年期護理師（N2）",
            "specialty_topic": "腫瘤外科 腸造口術後照護與心理支持",
            "chief_complaint": "52歲男性，直腸癌術後造口抗拒且拒絕直視",
            "scene": "一般病房",
            "primary_objective": "能敏銳察覺病人之生活恐懼，以反思性同理締結照護同盟",
            "core_task": "完成心理評估、同理共鳴並與病患共同擬定造口照護步調",
            "target_competencies": "全人照護、同理溝通、關係締結",
            "primary_focus": "人工造口身體心像紊亂與返家自我照護障礙",
            "differentials_or_context": "家庭經濟壓力、擔心職場異樣眼光、家庭支持系統不足",
            "emotional_cues": "「黏著這個袋子，我跟廢人有什麼兩樣…」",
            "high_discrimination": "能接住病人的情緒脆弱點而非單向衛教說教",
            "sp_profile": "抑鬱保守，眼神迴避腹部傷口",
        }
        prompt = grill_me.build_osce_prompt(config)

        self.assertIn("考評職類：護理學系／護理師", prompt)
        self.assertIn("敘事醫學方式評分", prompt)
        self.assertIn("向度1：全心傾聽與病患故事探索（Attention: Eliciting Illness Narrative）", prompt)
        self.assertIn("向度2：同理共鳴與處境再現（Representation: Empathic Resonance & Reflection）", prompt)
        self.assertIn("向度3：關係締結與共同照護同盟（Affiliation: Relational Alliance & Shared Care）", prompt)
        self.assertIn("向度4：考官質性敘事觀察與反思回饋（Narrative Observation & Qualitative Feedback）", prompt)
        self.assertIn("優異（4分）／熟練（3分）／發展中（2分）／未達標準（1分）", prompt)
        self.assertIn("滿分 12 分", prompt)
        self.assertIn("關鍵互動片段（Critical Incidents）", prompt)
        self.assertIn("SP 主動提問 **≤5 題**", prompt)
        self.assertNotIn("15 項 × 0/1/2 分", prompt)

    def test_non_medical_profession_checklist_prompt(self):
        config = {
            "profession": "藥學系／藥師",
            "rubric_type": "checklist",
            "item_count": 12,
            "station_type": "醫病溝通與衛教站",
            "learner_level": "實習藥師",
            "specialty_topic": "門診藥事諮詢 抗凝血劑高風險用藥指導",
            "chief_complaint": "68歲女性，心房顫動新開立抗凝血劑前來領藥諮詢",
            "scene": "門診診間",
            "primary_objective": "能完整評估病人用藥認知、解釋出血風險並完成 Teach-back",
            "core_task": "進行藥物交互作用排查、生活飲食衛教並確認理解",
            "target_competencies": "病人安全、專業素養、溝通衛教",
            "primary_focus": "新型口服抗凝血劑（NOAC）安全用藥",
            "differentials_or_context": "平時常自行服用中草藥與保健食品、跌倒風險、忘記服藥處理方式",
        }
        prompt = grill_me.build_osce_prompt(config)

        self.assertIn("考評職類：藥學系／藥師", prompt)
        self.assertIn("TAME 官方條列式評分（12 項 × 0/1/2 分，滿分 24 分）", prompt)
        self.assertIn("本站評分項目數：共 12 項，滿分 24 分", prompt)
        self.assertNotIn("全心傾聽與病患故事探索（Attention", prompt)


if __name__ == "__main__":
    unittest.main()


class TestPromptFollowsRules(unittest.TestCase):
    """Change a number in rules.yaml and the generated prompt must follow."""

    def test_every_rule_number_comes_from_rules_yaml(self):
        rules = grill_me.RULES
        prompt = grill_me.build_osce_prompt({"rubric_type": "checklist", "item_count": 12})
        self.assertIn(f"SP 主動提問 **≤{rules['sp']['questions_max']} 題**", prompt)
        self.assertIn(f"告示牌站次號 {rules['fonts_pt']['sign_station_number']}pt", prompt)
        self.assertIn("N=12→≤3", prompt)

    def test_rules_appear_once(self):
        prompt = grill_me.build_osce_prompt({"rubric_type": "checklist", "item_count": 15})
        self.assertEqual(prompt.count("SP 主動提問"), 1)
        self.assertEqual(prompt.count("★高鑑別力"), 1)
