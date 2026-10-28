# -*- coding: utf-8 -*-
"""
Apply polished translation for grisaia1/mak_011 (lines 32741 to 33175, total 435 lines).
"""

import os
from mak_011_part1 import mak_011_part1
from mak_011_part2 import mak_011_part2

full_new_cn = mak_011_part1 + mak_011_part2
assert len(full_new_cn) == 435, f"Expected 435 lines, got {len(full_new_cn)}"

tsv_path = os.path.join("tsv", "scratch_mak_011.tsv")
with open(tsv_path, "r", encoding="utf-8") as f:
    tsv_lines = [l.strip("\r\n").split("\t") for l in f]
assert len(tsv_lines) == 435, f"Expected 435 lines in TSV, got {len(tsv_lines)}"

with open("ALL_TEXT_cn.txt", "r", encoding="utf-8") as f:
    all_cn_lines = [l.rstrip("\r\n") for l in f]

START_IDX = 32740  # Line 32741 (0-indexed)
END_IDX = 33175    # Line 33175 inclusive -> slice [32740:33175] has 435 lines

new_slice = []
for i, (new_text, tsv_row) in enumerate(zip(full_new_cn, tsv_lines)):
    l_no, l_id, jp, old_cn = tsv_row
    if l_id:
        new_slice.append(f"{l_id}\t{new_text}" if new_text else f"{l_id}\t")
    else:
        new_slice.append(new_text)

assert len(new_slice) == 435

all_cn_lines[START_IDX:END_IDX] = new_slice
assert len(all_cn_lines) == 110622, f"Expected 110622 lines, got {len(all_cn_lines)}"

with open("ALL_TEXT_cn.txt", "w", encoding="utf-8") as f:
    for line in all_cn_lines:
        f.write(line + "\n")

print(f"Successfully patched mak_011 ({len(new_slice)} lines) into ALL_TEXT_cn.txt!")
