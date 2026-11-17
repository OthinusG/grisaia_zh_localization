#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch script for Grisaia 2 (The Labyrinth of Grisaia) - Michiru Short Story 3 (michiruss3)
Lines: 74766 - 74874 (0-indexed: 74765 - 74873, total 109 lines)
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tmp'))
import michiruss3_all

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cn_path = os.path.join(root, 'ALL_TEXT_cn.txt')
    jp_path = os.path.join(root, 'ALL_TEXT.txt')
    tsv_path = os.path.join(root, 'tsv', 'michiruss3.tsv')

    with open(cn_path, 'r', encoding='utf-8') as f:
        cn_lines = f.readlines()

    with open(jp_path, 'r', encoding='utf-8') as f:
        jp_lines = f.readlines()

    start_idx = 74765
    end_idx = 74874
    count = end_idx - start_idx
    assert count == 109, f"Expected 109 lines, got {count}"

    all_polished = michiruss3_all.ALL_LINES
    assert len(all_polished) == 109, f"Expected 109 polished lines, got {len(all_polished)}"

    tsv_rows = []
    tsv_rows.append("Line_ID\tJapanese\tChinese_Polished\n")

    for i in range(count):
        idx = start_idx + i
        jp_raw = jp_lines[idx].rstrip('\r\n')
        cn_raw = cn_lines[idx].rstrip('\r\n')
        polished_text = all_polished[i]

        jp_parts = jp_raw.split('\t', 1)
        cn_parts = cn_raw.split('\t', 1)
        line_id = jp_parts[0]
        assert cn_parts[0] == line_id, f"Line ID mismatch at {idx}: {line_id} vs {cn_parts[0]}"
        jp_text = jp_parts[1] if len(jp_parts) > 1 else ''

        cn_lines[idx] = f"{line_id}\t{polished_text}\n"
        tsv_rows.append(f"{line_id}\t{jp_text}\t{polished_text}\n")

    with open(cn_path, 'w', encoding='utf-8') as f:
        f.writelines(cn_lines)

    os.makedirs(os.path.join(root, 'tsv'), exist_ok=True)
    with open(tsv_path, 'w', encoding='utf-8') as f:
        f.writelines(tsv_rows)

    print(f"Successfully patched michiruss3 ({count} lines, indices {start_idx}..{end_idx-1}) and generated {tsv_path}")

if __name__ == '__main__':
    main()
