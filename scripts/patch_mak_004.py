#!/usr/bin/env python3
"""
Patch ALL_TEXT_cn.txt with polished mak_004 text (lines 27761 to 28373, 613 lines).
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))
import scripts.mak_004_part1 as p1
import scripts.mak_004_part2 as p2

def main():
    new_lines = p1.lines_part1 + p2.lines_part2
    assert len(new_lines) == 613, f"Expected 613 lines, got {len(new_lines)}"

    with open("ALL_TEXT_cn.txt", "r", encoding="utf-8") as f:
        all_cn = [line.rstrip("\r\n") for line in f]

    start_idx = 27760  # line 27761
    end_idx = 28373    # line 28373 (inclusive)
    count = end_idx - start_idx

    assert count == 613, f"Expected range 613, got {count}"

    for i in range(count):
        idx = start_idx + i
        orig_line = all_cn[idx]
        parts = orig_line.split("\t", 1)
        line_id = parts[0]
        assert line_id.startswith("grisaia1/mak_004#"), f"Wrong ID at line {idx+1}: {line_id}"
        all_cn[idx] = f"{line_id}\t{new_lines[i]}"

    with open("ALL_TEXT_cn.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(all_cn) + "\n")

    print(f"[OK] Successfully patched {count} lines in ALL_TEXT_cn.txt (L27761-L28373)!")

if __name__ == "__main__":
    main()
