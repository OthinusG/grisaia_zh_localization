# -*- coding: utf-8 -*-
"""
Apply patch to ALL_TEXT_cn.txt for grisaia1/mak_002 (lines 26808 to 27296)
"""
import sys, os
sys.path.insert(0, os.path.abspath('.'))

from scripts.mak_002_part1 import lines_part1
from scripts.mak_002_part2 import lines_part2

all_lines = lines_part1 + lines_part2
assert len(all_lines) == 489, f"Expected 489 lines, got {len(all_lines)}"

START_LINE = 26808
END_LINE = 27296

def apply_patch():
    print(f"Total patch entries: {len(all_lines)}")
    with open('ALL_TEXT_cn.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"Original line {START_LINE}: {lines[START_LINE - 1].strip()[:60]}")
    print(f"Original line {END_LINE}: {lines[END_LINE - 1].strip()[:60]}")
    
    for i, text in enumerate(all_lines):
        line_idx = START_LINE - 1 + i
        sid = f"grisaia1/mak_002#{i:05d}"
        lines[line_idx] = f"{sid}\t{text}\n"
        
    with open('ALL_TEXT_cn.txt', 'w', encoding='utf-8') as f:
        f.writelines(lines)
        
    print(f"Successfully patched grisaia1/mak_002 (lines {START_LINE} to {END_LINE})!")

if __name__ == '__main__':
    apply_patch()
