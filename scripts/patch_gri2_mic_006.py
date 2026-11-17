#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch script for Grisaia 2 (The Labyrinth of Grisaia) - Michiru After Story Chapter 6 (mic_006)
Lines: 74293 - 74579 (0-indexed: 74292 - 74578, total 287 lines)
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tmp'))
import mic_006_h1
import mic_006_h2

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cn_path = os.path.join(root, 'ALL_TEXT_cn.txt')
    jp_path = os.path.join(root, 'ALL_TEXT.txt')
    tsv_path = os.path.join(root, 'tsv', 'mic_006.tsv')

    with open(cn_path, 'r', encoding='utf-8') as f:
        cn_lines = f.readlines()

    with open(jp_path, 'r', encoding='utf-8') as f:
        jp_lines = f.readlines()

    start_idx = 74292
    end_idx = 74579
    count = end_idx - start_idx
    assert count == 287, f"Expected 287 lines, got {count}"

    all_polished = mic_006_h1.H1 + mic_006_h2.H2
    assert len(all_polished) == 287, f"Expected 287 polished lines, got {len(all_polished)}"

    tsv_rows = []
    tsv_rows.append("Line_ID\tJapanese\tChinese_Polished\n")

    for i in range(count):
        idx = start_idx + i
        jp_parts = jp_lines[idx].strip().split('\t')
        cn_parts = cn_lines[idx].strip().split('\t')
        line_id = jp_parts[0]
        assert cn_parts[0] == line_id, f"Line ID mismatch at {idx}: {line_id} vs {cn_parts[0]}"
        jp_text = jp_parts[1] if len(jp_parts) > 1 else ''
        polished_text = all_polished[i]

        cn_lines[idx] = f"{line_id}\t{polished_text}\n"
        tsv_rows.append(f"{line_id}\t{jp_text}\t{polished_text}\n")

    with open(cn_path, 'w', encoding='utf-8') as f:
        f.writelines(cn_lines)

    os.makedirs(os.path.join(root, 'tsv'), exist_ok=True)
    with open(tsv_path, 'w', encoding='utf-8') as f:
        f.writelines(tsv_rows)

    print(f"Successfully patched mic_006 ({count} lines, indices {start_idx}..{end_idx-1}) and generated {tsv_path}")

if __name__ == '__main__':
    main()
