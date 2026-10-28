# -*- coding: utf-8 -*-
"""
Patch ALL_TEXT_cn.txt for grisaia1/mak_019 (lines 36714 - 37097, 384 lines).
"""

from scripts.mak_019_part1 import mak_019_part1
from scripts.mak_019_part2 import mak_019_part2

def main():
    new_lines = mak_019_part1 + mak_019_part2
    assert len(new_lines) == 384, f"Expected 384 lines, got {len(new_lines)}"

    with open('ALL_TEXT_cn.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    assert len(lines) == 110622, f"Expected 110622 lines, got {len(lines)}"

    start_idx = 36713
    end_idx = 37097

    for i, new_text in enumerate(new_lines):
        idx = start_idx + i
        line_id = lines[idx].split('\t')[0]
        assert line_id == f"grisaia1/mak_019#{i:05d}", f"ID mismatch at {idx}: {line_id}"
        lines[idx] = f"{line_id}\t{new_text}\n"

    with open('ALL_TEXT_cn.txt', 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print("Successfully patched mak_019 into ALL_TEXT_cn.txt")

if __name__ == '__main__':
    main()
