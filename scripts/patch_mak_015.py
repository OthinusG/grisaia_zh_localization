# -*- coding: utf-8 -*-
"""
Patch polished translation for grisaia1/mak_015 into ALL_TEXT_cn.txt.
"""
import sys
sys.path.append('scripts')
from mak_015_part1 import mak_015_part1
from mak_015_part2 import mak_015_part2

def patch_mak_015():
    combined = mak_015_part1 + mak_015_part2
    assert len(combined) == 568, f"Expected 568 lines, got {len(combined)}"

    with open('ALL_TEXT_cn.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    assert len(lines) == 110622, f"Expected 110622 lines, got {len(lines)}"

    start_idx = 34888  # line 34889
    end_idx = 35456    # line 35456 (exclusive)

    assert lines[start_idx].startswith("grisaia1/mak_015#00000\t")
    assert lines[end_idx - 1].startswith("grisaia1/mak_015#00567\t")

    for i in range(len(combined)):
        idx = start_idx + i
        line_id = lines[idx].split('\t')[0]
        lines[idx] = f"{line_id}\t{combined[i]}\n"

    with open('ALL_TEXT_cn.txt', 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print("Successfully patched mak_015 into ALL_TEXT_cn.txt!")

if __name__ == '__main__':
    patch_mak_015()
