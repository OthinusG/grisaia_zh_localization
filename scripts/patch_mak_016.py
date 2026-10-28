# -*- coding: utf-8 -*-
"""
Patch polished translation for grisaia1/mak_016 into ALL_TEXT_cn.txt.
"""
import sys
sys.path.append('scripts')
from mak_016_part1 import mak_016_part1
from mak_016_part2 import mak_016_part2

def patch_mak_016():
    combined = mak_016_part1 + mak_016_part2
    assert len(combined) == 510, f"Expected 510 lines, got {len(combined)}"

    with open('ALL_TEXT_cn.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    assert len(lines) == 110622, f"Expected 110622 lines, got {len(lines)}"

    start_idx = 35456  # line 35457 (0-indexed)
    end_idx = 35966    # line 35966 (0-indexed exclusive)

    assert lines[start_idx].startswith("grisaia1/mak_016#00000\t")
    assert lines[end_idx - 1].startswith("grisaia1/mak_016#00509\t")

    for i in range(len(combined)):
        idx = start_idx + i
        line_id = lines[idx].split('\t')[0]
        lines[idx] = f"{line_id}\t{combined[i]}\n"

    with open('ALL_TEXT_cn.txt', 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print("Successfully patched mak_016 into ALL_TEXT_cn.txt!")

if __name__ == '__main__':
    patch_mak_016()
