#!/usr/bin/env python3
"""
Patch ALL_TEXT_cn.txt with polished yuj_012 (L83232 - L84001, 770 lines),
and export tsv/yuj_012.tsv.
"""

import json

def main():
    polished = json.load(open("tmp/yuj_012_done.json", "r", encoding="utf-8"))
    raw_items = json.load(open("tmp/yuj_012_raw.json", "r", encoding="utf-8"))
    assert len(polished) == len(raw_items) == 770

    with open("ALL_TEXT_cn.txt", "r", encoding="utf-8") as f:
        cn_lines = [line.rstrip("\r\n") for line in f]

    assert len(cn_lines) == 110622

    tsv_rows = ["line\tja_sid\tcn_sid\tja\tcn_orig\tcn_polished"]

    for raw_item, pol_text in zip(raw_items, polished):
        line_idx = raw_item["line"] - 1

        if raw_item["has_tab"]:
            expected_sid = raw_item["cn_sid"]
            orig_cn_line = cn_lines[line_idx]
            sid, orig_text = orig_cn_line.split("\t", 1)
            assert sid == expected_sid, f"SID mismatch at line {raw_item['line']}: {sid} vs {expected_sid}"

            # Update cn_lines
            cn_lines[line_idx] = f"{sid}\t{pol_text}"

            # Record TSV
            tsv_rows.append(f"{raw_item['line']}\t{raw_item['ja_sid']}\t{expected_sid}\t{raw_item['ja']}\t{orig_text}\t{pol_text}")
        else:
            orig_text = cn_lines[line_idx]
            cn_lines[line_idx] = pol_text
            tsv_rows.append(f"{raw_item['line']}\t\t\t{raw_item['ja']}\t{orig_text}\t{pol_text}")

    with open("ALL_TEXT_cn.txt", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(cn_lines) + "\n")

    with open("tsv/yuj_012.tsv", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(tsv_rows) + "\n")

    print(f"Successfully patched {len(polished)} lines in ALL_TEXT_cn.txt (L83232 - L84001).")
    print("Wrote tsv/yuj_012.tsv successfully.")

if __name__ == "__main__":
    main()
