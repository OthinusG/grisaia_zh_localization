#!/usr/bin/env python3
import json
import csv
import os

def main():
    with open("ALL_TEXT.txt", "r", encoding="utf-8") as f:
        jp_lines = f.readlines()

    with open("ALL_TEXT_cn.txt", "r", encoding="utf-8") as f:
        cn_lines = f.readlines()

    assert len(jp_lines) == 110622, f"Expected 110622 jp lines, got {len(jp_lines)}"
    assert len(cn_lines) == 110622, f"Expected 110622 cn lines, got {len(cn_lines)}"

    with open("tmp/yuj_015_p1_done.json", "r", encoding="utf-8") as f:
        polished = json.load(f)

    start_idx = 84593 # 1-based
    end_idx = 85264   # 1-based

    os.makedirs("tsv", exist_ok=True)
    tsv_path = "tsv/yuj_015_p1.tsv"

    tsv_rows = []
    tsv_rows.append(["line_idx", "line_id", "jp_text", "old_cn", "new_cn"])

    for idx in range(start_idx, end_idx + 1):
        line_0based = idx - 1
        jp_line = jp_lines[line_0based].rstrip("\r\n")
        old_cn_line = cn_lines[line_0based].rstrip("\r\n")

        # Determine line_id and raw text
        if "\t" in jp_line:
            line_id, jp_text = jp_line.split("\t", 1)
        else:
            line_id = ""
            jp_text = jp_line

        if "\t" in old_cn_line:
            _, old_cn_text = old_cn_line.split("\t", 1)
        else:
            old_cn_text = old_cn_line

        new_cn_text = polished[str(idx)]

        if line_id:
            new_cn_line = f"{line_id}\t{new_cn_text}\n"
        else:
            new_cn_line = f"{new_cn_text}\n"

        cn_lines[line_0based] = new_cn_line
        tsv_rows.append([str(idx), line_id, jp_text, old_cn_text, new_cn_text])

    with open("ALL_TEXT_cn.txt", "w", encoding="utf-8") as f:
        f.writelines(cn_lines)

    with open(tsv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerows(tsv_rows)

    print(f"Patched lines {start_idx} to {end_idx}. Exported {tsv_path}.")

if __name__ == "__main__":
    main()
