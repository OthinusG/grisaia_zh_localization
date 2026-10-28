# scripts/patch_mak_008a.py
import sys
from mak_008a_part1 import mak_008a_part1
from mak_008a_part2 import mak_008a_part2

all_polished = mak_008a_part1 + mak_008a_part2
assert len(all_polished) == 548, f"Expected 548 lines, got {len(all_polished)}"

with open("ALL_TEXT_cn.txt", "r", encoding="utf-8") as f:
    cn_lines = f.readlines()

assert len(cn_lines) == 110622, f"Expected 110622 lines, got {len(cn_lines)}"

START_LINE = 30148 - 1  # 0-indexed: 30147
END_LINE = 30695        # 0-indexed exclusive: 30695 (count = 548)

for i in range(548):
    idx = START_LINE + i
    parts = cn_lines[idx].rstrip("\r\n").split("\t")
    line_id = parts[0]
    new_text = all_polished[i]
    cn_lines[idx] = f"{line_id}\t{new_text}\n"

with open("ALL_TEXT_cn.txt", "w", encoding="utf-8") as f:
    f.writelines(cn_lines)

print(f"Successfully patched {len(all_polished)} lines in ALL_TEXT_cn.txt (L30148 - L30695)!")
