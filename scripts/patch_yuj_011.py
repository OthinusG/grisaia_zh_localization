#!/usr/bin/env python3
"""
Patch ALL_TEXT_cn.txt with polished yuj_011 (L83036 - L83231, 196 lines),
and export tsv/yuj_011.tsv.
"""

import json

def main():
    polished = json.load(open("tmp/yuj_011_done.json", "r", encoding="utf-8"))
    raw_items = json.load(open("tmp/yuj_011_raw.json", "r", encoding="utf-8"))
    assert len(polished) == len(raw_items) == 196

    with open("ALL_TEXT_cn.txt", "r", encoding="utf-8") as f:
        cn_lines = [line.rstrip("\r\n") for line in f]

    assert len(cn_lines) == 110622

    tsv_rows = ["line\tja_sid\tcn_sid\tja\tcn_orig\tcn_polished"]

    for raw_item, pol_text in zip(raw_items, polished):
        line_idx = raw_item["line"] - 1
        expected_sid = raw_item["cn_sid"]

        orig_cn_line = cn_lines[line_idx]
        sid, orig_text = orig_cn_line.split("\t", 1)
        assert sid == expected_sid, f"SID mismatch at line {raw_item['line']}: {sid} vs {expected_sid}"

        # Update cn_lines
        cn_lines[line_idx] = f"{sid}\t{pol_text}"

        # Record TSV
        tsv_rows.append(f"{raw_item['line']}\t{raw_item['ja_sid']}\t{expected_sid}\t{raw_item['ja']}\t{orig_text}\t{pol_text}")

    with open("ALL_TEXT_cn.txt", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(cn_lines) + "\n")

    with open("tsv/yuj_011.tsv", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(tsv_rows) + "\n")

    print(f"Successfully patched {len(polished)} lines in ALL_TEXT_cn.txt (L83036 - L83231).")
    print("Wrote tsv/yuj_011.tsv successfully.")

if __name__ == "__main__":
    main()
