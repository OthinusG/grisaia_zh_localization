# -*- coding: utf-8 -*-
"""Patch sac_027 (L55436 - L55715, 280 lines) in ALL_TEXT_cn.txt."""
import sys
sys.path.insert(0, '.')

from tmp.sac_027_b1 import b1_data
from tmp.sac_027_b2 import b2_data

combined_data = {}
combined_data.update(b1_data)
combined_data.update(b2_data)

assert len(combined_data) == 280, f"Expected 280 lines, got {len(combined_data)}"

with open("ALL_TEXT_cn.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

print(f"Total lines read: {len(lines)}")
assert len(lines) == 110622, f"Expected 110622 lines, got {len(lines)}"

mod_count = 0
for lnum, new_text in combined_data.items():
    idx = lnum - 1
    raw = lines[idx]
    parts = raw.rstrip("\r\n").split("\t")
    code = parts[0]
    old_text = parts[1] if len(parts) > 1 else ""
    if old_text != new_text:
        lines[idx] = f"{code}\t{new_text}\n"
        mod_count += 1

print(f"Total lines modified in sac_027: {mod_count}")

with open("ALL_TEXT_cn.txt", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("Patching complete.")
