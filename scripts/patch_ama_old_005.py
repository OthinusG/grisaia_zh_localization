# -*- coding: utf-8 -*-
from ama_old_005_all import ama_old_005_lines

with open("ALL_TEXT_cn.txt", "r", encoding="utf-8") as f:
    all_lines = f.readlines()

assert len(all_lines) == 110622, f"Expected 110622, got {len(all_lines)}"
assert len(ama_old_005_lines) == 136, f"Expected 136, got {len(ama_old_005_lines)}"

# Check boundary IDs
with open("ALL_TEXT.txt", "r", encoding="utf-8") as f:
    ja_lines = f.readlines()

for i in range(136):
    ja_id = ja_lines[9450 + i].split('\t')[0] if '\t' in ja_lines[9450 + i] else ''
    patch_id = ama_old_005_lines[i].split('\t')[0] if '\t' in ama_old_005_lines[i] else ''
    assert ja_id == patch_id, f"ID mismatch at {i}: {ja_id} != {patch_id}"

all_lines[9450:9586] = ama_old_005_lines

with open("ALL_TEXT_cn.txt", "w", encoding="utf-8") as f:
    f.writelines(all_lines)

print("Successfully applied patch to ALL_TEXT_cn.txt for ama_old_005 (136 lines).")
