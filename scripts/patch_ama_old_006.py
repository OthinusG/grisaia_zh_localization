# -*- coding: utf-8 -*-
from ama_old_006_all import ama_old_006_lines

with open("ALL_TEXT_cn.txt", "r", encoding="utf-8") as f:
    all_lines = f.readlines()

assert len(all_lines) == 110622, f"Expected 110622, got {len(all_lines)}"
assert len(ama_old_006_lines) == 178, f"Expected 178, got {len(ama_old_006_lines)}"

# Check boundary IDs
with open("ALL_TEXT.txt", "r", encoding="utf-8") as f:
    ja_lines = f.readlines()

for i in range(178):
    ja_id = ja_lines[9586 + i].split('\t')[0] if '\t' in ja_lines[9586 + i] else ''
    patch_id = ama_old_006_lines[i].split('\t')[0] if '\t' in ama_old_006_lines[i] else ''
    assert ja_id == patch_id, f"ID mismatch at {i}: {ja_id} != {patch_id}"

all_lines[9586:9764] = ama_old_006_lines

with open("ALL_TEXT_cn.txt", "w", encoding="utf-8") as f:
    f.writelines(all_lines)

print("Successfully applied patch to ALL_TEXT_cn.txt for ama_old_006 (178 lines).")
