#!/usr/bin/env python3
"""
Assemble yuj_007 slices, patch ALL_TEXT_cn.txt (L81162 - L81956, 795 lines),
and export tsv/yuj_007.tsv.
"""

import json

def main():
    s1 = json.load(open("tmp/yuj_007_s1_done.json", "r", encoding="utf-8"))
    s2 = json.load(open("tmp/yuj_007_s2_done.json", "r", encoding="utf-8"))
    s3 = json.load(open("tmp/yuj_007_s3_done.json", "r", encoding="utf-8"))
    s4 = json.load(open("tmp/yuj_007_s4_done.json", "r", encoding="utf-8"))

    full_polished = s1 + s2 + s3 + s4
    assert len(full_polished) == 795, f"Expected 795 lines, got {len(full_polished)}"

    raw_items = json.load(open("tmp/yuj_007_raw.json", "r", encoding="utf-8"))
    assert len(raw_items) == 795, f"Expected 795 raw items, got {len(raw_items)}"

    with open("ALL_TEXT_cn.txt", "r", encoding="utf-8") as f:
        cn_lines = [line.rstrip("\r\n") for line in f]

    assert len(cn_lines) == 110622, f"ALL_TEXT_cn.txt has {len(cn_lines)} lines, expected 110622"

    tsv_rows = ["line\tja_sid\tcn_sid\tja\tcn_orig\tcn_polished"]

    for idx, (raw_item, pol_text) in enumerate(zip(raw_items, full_polished)):
        line_idx = raw_item["line"] - 1  # 0-indexed line number
        expected_sid = raw_item["cn_sid"]

        orig_cn_line = cn_lines[line_idx]
        sid, orig_text = orig_cn_line.split("\t", 1)
        assert sid == expected_sid, f"SID mismatch at line {raw_item['line']}: {sid} vs {expected_sid}"

        # Update cn_lines
        new_cn_line = f"{sid}\t{pol_text}"
        cn_lines[line_idx] = new_cn_line

        # Record TSV
        tsv_rows.append(f"{raw_item['line']}\t{raw_item['ja_sid']}\t{expected_sid}\t{raw_item['ja']}\t{orig_text}\t{pol_text}")

    with open("ALL_TEXT_cn.txt", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(cn_lines) + "\n")

    with open("tsv/yuj_007.tsv", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(tsv_rows) + "\n")

    json.dump(full_polished, open("tmp/yuj_007_done.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)

    print("Successfully patched ALL_TEXT_cn.txt and generated tsv/yuj_007.tsv (795 lines).")

if __name__ == "__main__":
    main()
