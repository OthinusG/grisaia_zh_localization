# -*- coding: utf-8 -*-
"""
Apply polished translation for grisaia1/mak_008b (lines 30696 to 31466, total 771 lines).
"""

from mak_008b_part1 import mak_008b_part1
from mak_008b_part2 import mak_008b_part2

full_new_cn = mak_008b_part1 + mak_008b_part2
assert len(full_new_cn) == 771, f"Expected 771 lines, got {len(full_new_cn)}"

with open("scratch_mak_008b.tsv", "r", encoding="utf-8") as f:
    tsv_lines = [l.strip("\r\n").split("\t") for l in f]
assert len(tsv_lines) == 771

with open("ALL_TEXT_cn.txt", "r", encoding="utf-8") as f:
    all_cn_lines = [l.rstrip("\r\n") for l in f]

START_IDX = 30695  # Line 30696 (0-indexed)
END_IDX = 31466    # Line 31466 inclusive -> slice [30695:31466] has 771 lines

new_slice = []
for i, (new_text, tsv_row) in enumerate(zip(full_new_cn, tsv_lines)):
    l_no, l_id, jp, old_cn = tsv_row
    if l_id:
        new_slice.append(f"{l_id}\t{new_text}")
    else:
        new_slice.append(new_text)

assert len(new_slice) == 771

all_cn_lines[START_IDX:END_IDX] = new_slice
assert len(all_cn_lines) == 110622, f"Expected 110622 lines, got {len(all_cn_lines)}"

with open("ALL_TEXT_cn.txt", "w", encoding="utf-8") as f:
    for line in all_cn_lines:
        f.write(line + "\n")

print(f"Successfully patched mak_008b ({len(new_slice)} lines) into ALL_TEXT_cn.txt!")
