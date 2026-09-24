"""Regenerate every block marked GENERATED from rules.yaml.

    python scripts/build_docs.py          # rewrite the blocks in place
    python scripts/build_docs.py --check  # CI: fail if anything is stale

A block looks like

    <!-- BEGIN GENERATED: hard-spec (edit rules.yaml, then run scripts/build_docs.py) -->
    ...
    <!-- END GENERATED: hard-spec -->

Text outside the markers is hand-written and never touched.
"""
from __future__ import annotations

import argparse
import re
import sys

import osce_rules

TARGETS = {
    "skill/SKILL.md": {"hard-spec": osce_rules.hard_spec},
    "README.md": {"hard-spec": osce_rules.hard_spec},
    "SKILL_GPT.md": {"gpt-spec": osce_rules.gpt_spec},
}


def replace_block(text: str, name: str, body: str, where: str) -> str:
    begin = re.escape(f"<!-- BEGIN GENERATED: {name}")
    end = re.escape(f"<!-- END GENERATED: {name} -->")
    pattern = re.compile(rf"({begin}[^>]*-->\n)(?:.*?\n)?({end})", re.S)
    if not pattern.search(text):
        raise SystemExit(f"{where}: missing GENERATED block '{name}'")
    return pattern.sub(lambda m: m.group(1) + body + "\n" + m.group(2), text, count=1)


def build(check: bool) -> int:
    rules = osce_rules.load()
    stale = []
    for rel, blocks in TARGETS.items():
        path = osce_rules.REPO / rel
        before = path.read_text(encoding="utf-8")
        after = before
        for name, render in blocks.items():
            after = replace_block(after, name, render(rules), rel)
        if after != before:
            stale.append(rel)
            if not check:
                path.write_text(after, encoding="utf-8", newline="\n")
    if check and stale:
        print("rules.yaml 改了但這些檔案沒有重新產生：" + "、".join(stale), file=sys.stderr)
        print("請執行 python scripts/build_docs.py", file=sys.stderr)
        return 1
    print("已更新：" + "、".join(stale) if stale else "全部是最新的。")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    sys.exit(build(parser.parse_args().check))
