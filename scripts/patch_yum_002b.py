#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch ALL_TEXT_cn.txt for yum_002b (L57390 - L57669, 280 lines)
"""

import sys
sys.path.insert(0, 'tmp')
from yum_002b_part1 import p1
from yum_002b_part2 import p2

polished = p1 + p2
assert len(polished) == 280

start_line = 57390 # 1-indexed
end_line = 57669   # 1-indexed

with open('ALL_TEXT_cn.txt', 'r', encoding='utf-8') as f:
    lines = [line.strip('\r\n') for line in f]

assert len(lines) == 110622

modified_count = 0
for idx, pol_text in enumerate(polished):
    line_idx = (start_line - 1) + idx
    old_id, old_txt = lines[line_idx].split('\t', 1)
    if old_txt != pol_text:
        lines[line_idx] = f"{old_id}\t{pol_text}"
        modified_count += 1

with open('ALL_TEXT_cn.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines) + '\n')

print(f"Patched yum_002b: {modified_count} lines updated out of 280.")
