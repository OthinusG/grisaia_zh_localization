#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch script for Grisaia 2 (The Labyrinth of Grisaia) - Sachi After Story Chapter 5 Part 2 (sac_005 Part 2)
Lines: 76875 - 77467 (0-indexed: 76874 - 77466, total 593 lines)
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tmp'))
import sac_005_p2_s1
import sac_005_p2_s2
import sac_005_p2_s3

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cn_path = os.path.join(root, 'ALL_TEXT_cn.txt')
    jp_path = os.path.join(root, 'ALL_TEXT.txt')
    tsv_path = os.path.join(root, 'tsv', 'sac_005_p2.tsv')

    with open(cn_path, 'r', encoding='utf-8') as f:
        cn_lines = f.readlines()

    with open(jp_path, 'r', encoding='utf-8') as f:
        jp_lines = f.readlines()

    start_idx = 76874
    end_idx = 77467
    count = end_idx - start_idx
    assert count == 593, f"Expected 593 lines, got {count}"

    all_polished = sac_005_p2_s1.slice1 + sac_005_p2_s2.slice2 + sac_005_p2_s3.slice3
    assert len(all_polished) == 593, f"Expected 593 polished lines, got {len(all_polished)}"

    tsv_rows = []
    mod_count = 0

    for i in range(count):
        idx = start_idx + i
        jp_line = jp_lines[idx].rstrip('\r\n')
        orig_cn_line = cn_lines[idx].rstrip('\r\n')

        if '\t' in jp_line:
            jp_id, jp_text = jp_line.split('\t', 1)
            orig_cn_id, orig_cn_text = orig_cn_line.split('\t', 1)
            assert jp_id == orig_cn_id, f"ID mismatch at {idx}: {jp_id} vs {orig_cn_id}"

            new_text = all_polished[i]
            if new_text != orig_cn_text:
                mod_count += 1

            new_cn_line = f"{jp_id}\t{new_text}\n"
            cn_lines[idx] = new_cn_line
            tsv_rows.append(f"{jp_id}\t{jp_text}\t{orig_cn_text}\t{new_text}\n")
        else:
            jp_id = f"choice_{idx+1}"
            jp_text = jp_line
            orig_cn_text = orig_cn_line
            new_text = all_polished[i]
            if new_text != orig_cn_text:
                mod_count += 1

            new_cn_line = f"{new_text}\n"
            cn_lines[idx] = new_cn_line
            tsv_rows.append(f"{jp_id}\t{jp_text}\t{orig_cn_text}\t{new_text}\n")

    with open(cn_path, 'w', encoding='utf-8') as f:
        f.writelines(cn_lines)

    os.makedirs(os.path.dirname(tsv_path), exist_ok=True)
    with open(tsv_path, 'w', encoding='utf-8') as f:
        f.write("LineID\tJP\tOriginal_CN\tPolished_CN\n")
        f.writelines(tsv_rows)

    print(f"Successfully patched sac_005 Part 2: {count} lines processed, {mod_count} modified.")
    print(f"TSV saved to {tsv_path}")

if __name__ == '__main__':
    main()
