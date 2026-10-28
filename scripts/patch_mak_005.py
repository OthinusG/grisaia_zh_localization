# -*- coding: utf-8 -*-
import sys
from mak_005_part1 import mak_005_part1
from mak_005_part2 import mak_005_part2

full_polished = mak_005_part1 + mak_005_part2
print(f"Total polished lines: {len(full_polished)}")

with open('ALL_TEXT.txt', 'r', encoding='utf-8') as f_jp:
    jp_lines = [line.strip('\r\n') for line in f_jp]

with open('ALL_TEXT_cn.txt', 'r', encoding='utf-8') as f_cn:
    cn_lines = [line.strip('\r\n') for line in f_cn]

start_line = 28374 - 1 # 0-indexed: 28373
end_line = 29008       # 0-indexed: 29008 (slice: 28373:29008, 635 lines)

expected_count = end_line - start_line
assert len(full_polished) == expected_count, f"Count mismatch: {len(full_polished)} vs {expected_count}"

patched_count = 0
for idx, new_text in enumerate(full_polished):
    line_idx = start_line + idx
    jp_line = jp_lines[line_idx]
    line_id = jp_line.split('\t')[0]
    new_cn_line = f"{line_id}\t{new_text}"
    cn_lines[line_idx] = new_cn_line
    patched_count += 1

with open('ALL_TEXT_cn.txt', 'w', encoding='utf-8') as f_out:
    for line in cn_lines:
        f_out.write(line + '\n')

print(f"Successfully patched {patched_count} lines in ALL_TEXT_cn.txt (lines 28374-29008)!")
