# -*- coding: utf-8 -*-
"""
Apply patch for grisaia1/com19 (Lines 16067 - 16193, 127 lines).
"""
import sys
from build_com19_patch import lines_data

CN_FILE = "ALL_TEXT_cn.txt"

with open(CN_FILE, "r", encoding="utf-8") as f:
    cn_lines = f.readlines()

print(f"Original total lines: {len(cn_lines)}")
assert len(cn_lines) == 110622

# Verify start and end line IDs before replacement
first_orig_id = cn_lines[16066].split("\t")[0]
last_orig_id = cn_lines[16192].split("\t")[0]
assert first_orig_id == "grisaia1/com19#00000", f"Unexpected first id: {first_orig_id}"
assert last_orig_id == "grisaia1/com19#00126", f"Unexpected last id: {last_orig_id}"

# Apply replacement
for line_no, line_id, text in lines_data:
    idx = line_no - 1
    orig_id = cn_lines[idx].split("\t")[0]
    assert orig_id == line_id, f"ID mismatch at line {line_no}: expected {line_id}, got {orig_id}"
    cn_lines[idx] = f"{line_id}\t{text}\n"

with open(CN_FILE, "w", encoding="utf-8") as f:
    f.writelines(cn_lines)

print("Applied patch for grisaia1/com19 successfully.")
