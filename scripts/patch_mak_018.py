# -*- coding: utf-8 -*-
"""
Patch ALL_TEXT_cn.txt for grisaia1/mak_018 (lines 36487 - 36713, 227 lines).
"""

from scripts.mak_018_all import mak_018_lines

def main():
    assert len(mak_018_lines) == 227, f"Expected 227 lines, got {len(mak_018_lines)}"

    with open('ALL_TEXT_cn.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    assert len(lines) == 110622, f"Expected 110622 lines, got {len(lines)}"

    start_idx = 36486
    end_idx = 36713

    for i, new_text in enumerate(mak_018_lines):
        idx = start_idx + i
        line_id = lines[idx].split('\t')[0]
        assert line_id == f"grisaia1/mak_018#{i:05d}", f"ID mismatch at {idx}: {line_id}"
        lines[idx] = f"{line_id}\t{new_text}\n"

    with open('ALL_TEXT_cn.txt', 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print("Successfully patched mak_018 into ALL_TEXT_cn.txt")

if __name__ == '__main__':
    main()
