# -*- coding: utf-8 -*-
"""
Apply patch to ALL_TEXT_cn.txt for grisaia1/mak_001 (lines 26257 to 26807)
"""
import sys, os
sys.path.insert(0, os.path.abspath('.'))

from scripts.mak_001_part1 import lines_part1
from scripts.mak_001_part2 import lines_part2
from scripts.mak_001_part3 import lines_part3

all_lines = lines_part1 + lines_part2 + lines_part3
assert len(all_lines) == 551, f"Expected 551 lines, got {len(all_lines)}"

START_LINE = 26257
END_LINE = 26807

def apply_patch():
    print(f"Total patch entries: {len(all_lines)}")
    with open('ALL_TEXT_cn.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    print(f"Original line {START_LINE}: {lines[START_LINE - 1].strip()[:60]}")
    print(f"Original line {END_LINE}: {lines[END_LINE - 1].strip()[:60]}")
    
    for i, text in enumerate(all_lines):
        line_idx = START_LINE - 1 + i
        sid = f"grisaia1/mak_001#{i:05d}"
        lines[line_idx] = f"{sid}\t{text}\n"
        
    with open('ALL_TEXT_cn.txt', 'w', encoding='utf-8') as f:
        f.writelines(lines)
        
    print(f"Successfully patched grisaia1/mak_001 (lines {START_LINE} to {END_LINE})!")

if __name__ == '__main__':
    apply_patch()
