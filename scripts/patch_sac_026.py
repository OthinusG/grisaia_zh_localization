# -*- coding: utf-8 -*-
"""
Patch script for sac_026 (L55217 - L55435, 219 lines)
"""

import sys
sys.path.insert(0, '.')
from tmp.sac_026_records import records
from tmp.sac_026_b1 import translations_b1
from tmp.sac_026_b2 import translations_b2

all_translations = {}
all_translations.update(translations_b1)
all_translations.update(translations_b2)

START_LINE = 55216  # 0-indexed line 55217
END_LINE = 55435    # 219 lines

def patch_file(cn_path='ALL_TEXT_cn.txt'):
    with open(cn_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    modified_count = 0
    for idx, (lno, lid, ja, old_cn) in enumerate(records):
        line_idx = lno - 1
        line = lines[line_idx]
        parts = line.rstrip('\r\n').split('\t')
        line_id = parts[0]
        assert line_id == lid, f"Mismatch: {line_id} vs {lid} at line {lno}"

        new_text = all_translations[lno]
        lines[line_idx] = f"{line_id}\t{new_text}\n"
        modified_count += 1

    with open(cn_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print(f"Patched {modified_count} lines in {cn_path} (range {START_LINE+1} to {END_LINE}).")

if __name__ == '__main__':
    patch_file()
