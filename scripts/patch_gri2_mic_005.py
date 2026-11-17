#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
patch_gri2_mic_005.py - Apply polished localization for grisaia2/mic_005 (M3.4.05).
737 lines: L73556 to L74292 (0-indexed lines 73555 to 74291).
"""

import os
import sys

# Import the 4 parts
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tmp.mic_005_p1 import P1
from tmp.mic_005_p2 import P2
from tmp.mic_005_p3 import P3
from tmp.mic_005_p4 import P4

def main():
    mic_005_cn = P1 + P2 + P3 + P4
    assert len(mic_005_cn) == 737, f"Expected 737 lines, got {len(mic_005_cn)}"

    cn_path = 'ALL_TEXT_cn.txt'
    with open(cn_path, 'r', encoding='utf-8') as f:
        cn_lines = f.readlines()

    assert len(cn_lines) == 110622, f"Expected 110622 lines in ALL_TEXT_cn.txt, got {len(cn_lines)}"

    start_idx = 73555
    end_idx = 73555 + 737 # 74292 (non-inclusive)

    # Verify boundaries
    assert cn_lines[start_idx].startswith('grisaia2/mic_005#00000\t'), f"Mismatch at start: {cn_lines[start_idx][:40]}"
    assert cn_lines[end_idx - 1].startswith('grisaia2/mic_005#00736\t'), f"Mismatch at end: {cn_lines[end_idx - 1][:40]}"

    # Patch lines
    for i, new_text in enumerate(mic_005_cn):
        line_idx = start_idx + i
        tag = cn_lines[line_idx].split('\t')[0]
        cn_lines[line_idx] = f"{tag}\t{new_text}\n"

    with open(cn_path, 'w', encoding='utf-8') as f:
        f.writelines(cn_lines)

    print(f"Successfully patched {len(mic_005_cn)} lines in {cn_path} (indices {start_idx}..{end_idx-1})")

    # Export TSV
    jp_path = 'ALL_TEXT.txt'
    with open(jp_path, 'r', encoding='utf-8') as f:
        jp_lines = [l.strip().split('\t', 1) for l in f.readlines()[start_idx:end_idx]]

    tsv_path = 'tsv/mic_005.tsv'
    os.makedirs('tsv', exist_ok=True)
    with open(tsv_path, 'w', encoding='utf-8') as f:
        f.write("Tag\tJapanese\tChinese\n")
        for i in range(len(mic_005_cn)):
            tag, jp_text = jp_lines[i]
            cn_text = mic_005_cn[i]
            f.write(f"{tag}\t{jp_text}\t{cn_text}\n")

    print(f"Exported TSV to {tsv_path}")

if __name__ == '__main__':
    main()
