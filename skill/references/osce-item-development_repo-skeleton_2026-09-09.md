<!-- SUPERSEDED 2026-09-09. Prior Context Repo SKILL.md, kept for provenance. The live skill now carries the local 23 KB workflow as its body. -->

---
name: osce-item-development
description: >
  Develop, revise, or audit an OSCE assessment station, including competency alignment, station blueprint, candidate instructions, standardized-patient/family script, examiner guide, observable scoring anchors, TAME-style structure, and station QA. Trigger for OSCE 出題/修題/審題, SP/family scripts, candidate/examiner guides, or OSCE scoring rubrics. Do not trigger for ordinary clinical case discussion, pure VR/dry-lab simulation curriculum, reliability/statistical analysis alone, or generic teaching documents unrelated to an OSCE station.
---

# OSCE Item Development — Canonical Workflow

## Core contract
OSCE is performance-based assessment. Align `competency → task → observable behavior → scoring → SP/examiner standardization` and keep the station feasible for the stated learner and time.

The historical detailed workflow is preserved in `references/OSCE_SKILL_original_2026-08-18.md`; load it only when exact legacy/TAME formatting or Word-generation details are needed.

## Start / resume
1. Use existing station files/templates and previously agreed constraints before asking questions.
2. Resolve only missing information that materially changes the construct: learner level, station type, core task, target competency, setting, time, personnel, and output level.
3. For clerk stations, align to the applicable clerk competency/blueprint when available. If no authoritative competency source is accessible, flag the gap rather than invent a formal mapping.

## Station design
1. **Blueprint** — one primary assessment intent; learner level; time; setting; target competency/domain; pass/fail intent if applicable.
2. **Clinical scenario** — internally consistent, focused, and sufficiently informative without revealing the scoring key.
3. **Candidate task** — clear role, setting, time, available resources, and what is/not assessed; do not expose rubric wording.
4. **Examiner guide** — case summary, expected reasoning/management, required materials, scoring anchors, and standardization notes.
5. **SP/family guide** — identity, affect, baseline story, response boundaries, permitted prompts/questions, and explicit trigger behavior.
6. **Scoring** — observable behaviors only; avoid duplicate scoring, hidden inference, and overly generic professionalism items.
7. **QA** — feasibility, blueprint coverage, cue dependence, construct underrepresentation/irrelevant variance, rater usability, clinical correctness, and internal consistency.

## Default TAME-style structure
For a full station, use the five-part structure unless the user's institutional template differs:
1. 告示牌
2. 考生指引
3. 評分表
4. 考官指引
5. SP 指引

When using the user's established national-style format:
- usually 15 scored items with 0/1/2 anchors and total 30;
- define `沒有做到 / 部分做到 / 完全做到` precisely;
- keep generic/common scoring items limited and preserve most points for the station's core construct;
- include 2–5 higher-discrimination items when appropriate;
- do not force these counts when the requested exam format specifies another validated structure.

## Station-specific checks
- **History**: organize symptom inquiry and discriminating diagnostic/risk clues; avoid fragmenting mnemonic elements into excessive low-value items.
- **Physical examination**: score observable technique and clinically meaningful findings; for abdominal exam preserve inspection → auscultation → percussion → palpation unless the station intentionally tests another sequence.
- **Communication/education**: assess relationship, information organization, empathy/response to concerns, understanding, safety net, and teach-back when appropriate.
- **Explanation/management**: assess explanation of diagnosis/uncertainty, next steps, immediate safety, treatment options, shared decisions, follow-up, and patient concerns.
- **Technical/procedure**: separate safety/preparation, critical procedural steps, completion, and complication/error management.

## SP standardization
- Define what the SP may volunteer and what requires a candidate prompt.
- Keep active SP questions limited and purposeful; specify trigger conditions.
- Every SP-dependent scoring item must have a corresponding standardized response/behavior.
- Use a dialogue table when helpful: `病歷架構 | 醫師對 SP 說的話 | SP 的回應`.

## Artifact handoff
If the user requests a final Word/PDF station, finish content and QA first, then use `$artifact-production`. User-specified templates/paths override legacy local Word-COM instructions. Do not regenerate over a manually edited canonical file without preserving it.

## Boundaries
- Simulation curriculum without a summative OSCE item → `$simulation-curriculum`.
- ICC/Cronbach/item analysis only → `$clinical-statistics`.
- If performance data are used to revise the station, statistical analysis may hand back to this skill for item redesign.

## Context Repo contract
- Store final station documents in the cloud project workspace; keep durable blueprint/format decisions and handoff in the Context Repo only when this is a persistent project.
- For substantial persistent project changes, finish with `$context-closeout`.
