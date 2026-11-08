# -*- coding: utf-8 -*-
"""
Patch script for sac_022 (L53761 - L53886, 126 lines)
"""

import sys
sys.path.insert(0, '.')
from tmp.sac_022_b1 import translations

START_LINE = 53760  # 0-indexed line 53761
END_LINE = 53886    # 126 lines

def patch_file(cn_path='ALL_TEXT_cn.txt'):
    with open(cn_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    modified_count = 0
    for i in range(START_LINE, END_LINE):
        line = lines[i]
        parts = line.rstrip('\r\n').split('\t')
        line_id = parts[0]
        if line_id in translations:
            new_text = translations[line_id]
            lines[i] = f"{line_id}\t{new_text}\n"
            modified_count += 1
        else:
            print(f"Warning: line_id {line_id} not in translations!")

    with open(cn_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"Patched {modified_count} lines in {cn_path} (range {START_LINE+1} to {END_LINE}).")

if __name__ == '__main__':
    patch_file()
