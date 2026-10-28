# -*- coding: utf-8 -*-
"""
Apply polished translation for grisaia1/mak_013 (lines 33607 to 34114, total 508 lines).
"""

import os
from mak_013_part1 import mak_013_part1
from mak_013_part2 import mak_013_part2

full_new_cn = mak_013_part1 + mak_013_part2
assert len(full_new_cn) == 508, f"Expected 508 lines, got {len(full_new_cn)}"

tsv_path = os.path.join("tsv", "scratch_mak_013.tsv")
with open(tsv_path, "r", encoding="utf-8") as f:
    tsv_lines = [l.strip("\r\n").split("\t") for l in f]
assert len(tsv_lines) == 508, f"Expected 508 lines in TSV, got {len(tsv_lines)}"

with open("ALL_TEXT_cn.txt", "r", encoding="utf-8") as f:
    all_cn_lines = [l.rstrip("\r\n") for l in f]

START_IDX = 33606  # Line 33607 (0-indexed)
END_IDX = 34114    # Line 34114 inclusive -> slice [33606:34114] has 508 lines

new_slice = []
for i, (new_text, tsv_row) in enumerate(zip(full_new_cn, tsv_lines)):
    l_no = tsv_row[0]
    l_id = tsv_row[1] if len(tsv_row) > 1 else ""
    if l_id:
        new_slice.append(f"{l_id}\t{new_text}" if new_text else f"{l_id}\t")
    else:
        new_slice.append(new_text)

assert len(new_slice) == 508

all_cn_lines[START_IDX:END_IDX] = new_slice
assert len(all_cn_lines) == 110622, f"Expected 110622 lines, got {len(all_cn_lines)}"

with open("ALL_TEXT_cn.txt", "w", encoding="utf-8") as f:
    for line in all_cn_lines:
        f.write(line + "\n")

print(f"Successfully patched mak_013 ({len(new_slice)} lines) into ALL_TEXT_cn.txt!")
