# -*- coding: utf-8 -*-
"""
Apply polished translation for grisaia1/mak_009 (lines 31467 to 32010, total 544 lines).
"""

import os
from mak_009_part1 import mak_009_part1
from mak_009_part2 import mak_009_part2

full_new_cn = mak_009_part1 + mak_009_part2
assert len(full_new_cn) == 544, f"Expected 544 lines, got {len(full_new_cn)}"

tsv_path = "scratch_mak_009.tsv" if os.path.exists("scratch_mak_009.tsv") else os.path.join("tsv", "scratch_mak_009.tsv")
with open(tsv_path, "r", encoding="utf-8") as f:
    tsv_lines = [l.strip("\r\n").split("\t") for l in f]
assert len(tsv_lines) == 544, f"Expected 544 lines in TSV, got {len(tsv_lines)}"

with open("ALL_TEXT_cn.txt", "r", encoding="utf-8") as f:
    all_cn_lines = [l.rstrip("\r\n") for l in f]

START_IDX = 31466  # Line 31467 (0-indexed)
END_IDX = 32010    # Line 32010 inclusive -> slice [31466:32010] has 544 lines

new_slice = []
for i, (new_text, tsv_row) in enumerate(zip(full_new_cn, tsv_lines)):
    l_no, l_id, jp, old_cn = tsv_row
    if l_id:
        new_slice.append(f"{l_id}\t{new_text}")
    else:
        new_slice.append(new_text)

assert len(new_slice) == 544

all_cn_lines[START_IDX:END_IDX] = new_slice
assert len(all_cn_lines) == 110622, f"Expected 110622 lines, got {len(all_cn_lines)}"

with open("ALL_TEXT_cn.txt", "w", encoding="utf-8") as f:
    for line in all_cn_lines:
        f.write(line + "\n")

print(f"Successfully patched mak_009 ({len(new_slice)} lines) into ALL_TEXT_cn.txt!")
