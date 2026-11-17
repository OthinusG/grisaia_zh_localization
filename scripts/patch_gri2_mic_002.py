# -*- coding: utf-8 -*-
"""
Patch script for grisaia2/mic_002 (L72286 - L72643, 358 lines)
"""
import json

def main():
    target_file = "ALL_TEXT_cn.txt"
    start_line = 72286  # 1-based
    end_line = 72643

    with open("tmp/mic_002_done.json", "r", encoding="utf-8") as f:
        polished_lines = json.load(f)

    assert len(polished_lines) == 358, f"Expected 358 lines, got {len(polished_lines)}"

    with open(target_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    total_lines = len(lines)
    assert total_lines == 110622, f"Total lines mismatch: {total_lines}"

    for idx, new_text in enumerate(polished_lines):
        line_idx = start_line - 1 + idx
        prefix = lines[line_idx].split("\t")[0]
        lines[line_idx] = f"{prefix}\t{new_text}\n"

    with open(target_file, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"Successfully patched {len(polished_lines)} lines in {target_file} ({start_line} - {end_line})")

if __name__ == "__main__":
    main()
