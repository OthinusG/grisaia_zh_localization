# -*- coding: utf-8 -*-
"""
Patch script for sac_023a (L53887 - L54349, 463 lines)
"""

import sys
sys.path.insert(0, '.')
from tmp.sac_023a_b1 import translations_b1
from tmp.sac_023a_b2 import translations_b2
from tmp.sac_023a_b3 import translations_b3
from tmp.sac_023a_b4 import translations_b4

merged = {}
merged.update(translations_b1)
merged.update(translations_b2)
merged.update(translations_b3)
merged.update(translations_b4)

START_LINE = 53886  # 0-indexed line 53887
END_LINE = 54349    # 463 lines

def patch_file(ja_path='ALL_TEXT.txt', cn_path='ALL_TEXT_cn.txt'):
    with open(ja_path, 'r', encoding='utf-8') as f:
        ja_lines = f.readlines()
    with open(cn_path, 'r', encoding='utf-8') as f:
        cn_lines = f.readlines()

    modified_count = 0
    for i in range(START_LINE, END_LINE):
        lno = i + 1
        ja_line = ja_lines[i].rstrip('\r\n')
        new_text = merged[lno]

        if ja_line.strip() == '':
            cn_lines[i] = '\n'
        elif '\t' in ja_line:
            ja_id = ja_line.split('\t', 1)[0]
            if new_text == '':
                cn_lines[i] = f"{ja_id}\t\n"
            else:
                cn_lines[i] = f"{ja_id}\t{new_text}\n"
        else:
            cn_lines[i] = f"{new_text}\n"
        modified_count += 1

    with open(cn_path, 'w', encoding='utf-8') as f:
        f.writelines(cn_lines)

    print(f"Patched {modified_count} lines in {cn_path} (range {START_LINE+1} to {END_LINE}).")

if __name__ == '__main__':
    patch_file()
