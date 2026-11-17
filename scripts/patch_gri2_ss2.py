#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch script for Grisaia 2 (The Labyrinth of Grisaia) - Mihama Short Story 2 (ss2)
Lines: 78056 - 78107 (0-indexed: 78055 - 78106, total 52 lines)
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tmp'))
import ss2_lines

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cn_path = os.path.join(root, 'ALL_TEXT_cn.txt')
    jp_path = os.path.join(root, 'ALL_TEXT.txt')
    tsv_path = os.path.join(root, 'tsv', 'ss2.tsv')

    with open(cn_path, 'r', encoding='utf-8') as f:
        cn_lines = f.readlines()

    with open(jp_path, 'r', encoding='utf-8') as f:
        jp_lines = f.readlines()

    start_idx = 78055
    end_idx = 78107
    count = end_idx - start_idx
    assert count == 52, f"Expected 52 lines, got {count}"

    all_polished = ss2_lines.lines
    assert len(all_polished) == 52, f"Expected 52 polished lines, got {len(all_polished)}"

    tsv_rows = []
    mod_count = 0

    for i in range(count):
        idx = start_idx + i
        jp_line = jp_lines[idx].rstrip('\r\n')
        orig_cn_line = cn_lines[idx].rstrip('\r\n')

        jp_id, jp_text = jp_line.split('\t', 1)
        orig_cn_id, orig_cn_text = orig_cn_line.split('\t', 1)
        assert jp_id == orig_cn_id, f"ID mismatch at {idx}: {jp_id} vs {orig_cn_id}"

        new_text = all_polished[i]
        if new_text != orig_cn_text:
            mod_count += 1

        new_cn_line = f"{jp_id}\t{new_text}\n"
        cn_lines[idx] = new_cn_line
        tsv_rows.append(f"{jp_id}\t{jp_text}\t{orig_cn_text}\t{new_text}\n")

    with open(cn_path, 'w', encoding='utf-8') as f:
        f.writelines(cn_lines)

    os.makedirs(os.path.dirname(tsv_path), exist_ok=True)
    with open(tsv_path, 'w', encoding='utf-8') as f:
        f.write("LineID\tJP\tOriginal_CN\tPolished_CN\n")
        f.writelines(tsv_rows)

    print(f"Successfully patched ss2: {count} lines processed, {mod_count} modified.")
    print(f"TSV saved to {tsv_path}")

if __name__ == '__main__':
    main()
