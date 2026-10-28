# -*- coding: utf-8 -*-
"""
Patch ALL_TEXT_cn.txt for grisaia1/mak_017 (lines 35967 - 36486, 520 lines).
"""

from scripts.mak_017_part1 import mak_017_part1
from scripts.mak_017_part2 import mak_017_part2

def main():
    new_lines = mak_017_part1 + mak_017_part2
    assert len(new_lines) == 520, f"Expected 520 lines, got {len(new_lines)}"

    with open('ALL_TEXT_cn.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    assert len(lines) == 110622, f"Expected 110622 lines, got {len(lines)}"

    start_idx = 35966
    end_idx = 36486

    for i, new_text in enumerate(new_lines):
        idx = start_idx + i
        line_id = lines[idx].split('\t')[0]
        assert line_id == f"grisaia1/mak_017#{i:05d}", f"ID mismatch at {idx}: {line_id}"
        lines[idx] = f"{line_id}\t{new_text}\n"

    with open('ALL_TEXT_cn.txt', 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print("Successfully patched mak_017 into ALL_TEXT_cn.txt")

if __name__ == '__main__':
    main()
