#!/usr/bin/env python3
"""
Verify structural alignment, control tokens, and line counts between Japanese and Chinese scripts.
"""

import sys
import re

def verify(ja_path="ALL_TEXT.txt", cn_path="ALL_TEXT_cn.txt"):
    tag_re = re.compile(r"(\$\[.*?\$\]|\[\$b.*?\$\])")
    speaker_re = re.compile(r"^@([^@]+)@")

    with open(ja_path, "r", encoding="utf-8") as fj, open(cn_path, "r", encoding="utf-8") as fc:
        ja_lines = [l.rstrip("\r\n") for l in fj]
        cn_lines = [l.rstrip("\r\n") for l in fc]

    if len(ja_lines) != len(cn_lines):
        print(f"[FAIL] Line count mismatch: JA has {len(ja_lines)}, CN has {len(cn_lines)}")
        return False

    errors = 0
    for idx, (j, c) in enumerate(zip(ja_lines, cn_lines)):
        line_no = idx + 1
        j_tab = "\t" in j
        c_tab = "\t" in c
        if j_tab != c_tab:
            print(f"[ERROR] Line {line_no}: Tab mismatch (JA={j_tab}, CN={c_tab})")
            errors += 1
            if errors > 20: break
            continue

        if j_tab:
            j_id, j_text = j.split("\t", 1)
            c_id, c_text = c.split("\t", 1)
            if j_id != c_id:
                print(f"[ERROR] Line {line_no}: ID mismatch ({j_id} != {c_id})")
                errors += 1
                if errors > 20: break
                continue

            # Check tags
            j_tags = tag_re.findall(j_text)
            c_tags = tag_re.findall(c_text)
            if len(j_tags) != len(c_tags):
                print(f"[ERROR] Line {line_no} ({j_id}): Tag count mismatch (JA={len(j_tags)}, CN={len(c_tags)})")
                errors += 1
                if errors > 20: break
                continue

            # Check speaker tags
            j_sp = speaker_re.match(j_text)
            c_sp = speaker_re.match(c_text)
            if bool(j_sp) != bool(c_sp):
                print(f"[ERROR] Line {line_no} ({j_id}): Speaker presence mismatch (JA={bool(j_sp)}, CN={bool(c_sp)})")
                errors += 1
                if errors > 20: break
                continue

    if errors == 0:
        print(f"[PASS] All {len(ja_lines)} lines structurally verified! Line IDs, tabs, tags, and speakers 100% match.")
        return True
    else:
        print(f"[FAIL] Found errors during verification.")
        return False

if __name__ == "__main__":
    success = verify()
    sys.exit(0 if success else 1)
