#!/usr/bin/env python3
"""
Corpus Scanner for Grisaia localization text.
Identifies residual AI artifacts, known mistranslations, and untranslated kanji across all 110,622 lines.
"""

import re
import sys
from collections import defaultdict

SUSPICIOUS_PATTERNS = [
    (r"十德小刀", "MT of 十徳ナイフ (should be 瑞士军刀/多功能军刀)"),
    (r"蜂先生", "MT of 蜂さん (should be 蜜蜂/小蜜蜂)"),
    (r"怪气味", "MT of 気味が悪い/気味の悪い (should be 瘆人/让人心里发毛)"),
    (r"菜式数量", "MT of 場数 (should be 掌勺经验/阅历/大场面)"),
    (r"通勤妻子", "MT of 通い妻 (should be 上门服侍的小娇妻/走婚妻子)"),
    (r"犬一般死去", "MT of 犬死に (should be 枉死/白白送命)"),
    (r"贵方", "MT of 貴方 (in dialogue should be 你/您)"),
    (r"食生活", "Raw Japanese kanji borrow (should be 饮食习惯/伙食)"),
    (r"八百屋", "Raw Japanese kanji borrow (should be 蔬菜店/果蔬铺)"),
    (r"乔恩乔罗", "Literal sound transliteration of ジョンジョロ (should be 哗啦啦)"),
    (r"不用谢啦.*ノーサンキュー", "Reversal of ノーサンキュー (should be 敬谢不敏/我不需要)"),
]

def scan(cn_path="ALL_TEXT_cn.txt"):
    compiled = [(re.compile(p), desc) for p, desc in SUSPICIOUS_PATTERNS]
    found = defaultdict(list)

    with open(cn_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            line_no = idx + 1
            for reg, desc in compiled:
                if reg.search(line):
                    found[desc].append((line_no, line.strip()))

    print(f"=== Scan Results for {cn_path} ===")
    total_issues = 0
    for desc, matches in found.items():
        total_issues += len(matches)
        print(f"\n[{desc}]: {len(matches)} occurrences")
        for lno, text in matches[:5]:
            print(f"  Line {lno}: {text[:100]}")
        if len(matches) > 5:
            print(f"  ... and {len(matches) - 5} more")

    print(f"\nTotal flag count: {total_issues}")
    return total_issues

if __name__ == "__main__":
    scan()
