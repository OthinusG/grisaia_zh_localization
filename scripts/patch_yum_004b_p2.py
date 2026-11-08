#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch ALL_TEXT_cn.txt for yum_004b Part 2 (L60635 - L61281, 647 lines)
"""

import sys
sys.path.insert(0, 'tmp')
from trans_004b_p2_s1 import TRANS_004B_P2_S1
from trans_004b_p2_s2 import TRANS_004B_P2_S2
from trans_004b_p2_s3 import TRANS_004B_P2_S3

all_trans = {}
all_trans.update(TRANS_004B_P2_S1)
all_trans.update(TRANS_004B_P2_S2)
all_trans.update(TRANS_004B_P2_S3)

assert len(all_trans) == 317, f"Expected 317 text entries, got {len(all_trans)}"

with open('tsv/yum_004b_p2.tsv', 'r', encoding='utf-8') as f:
    tsv_lines = [l.strip('\n').split('\t') for l in f]

assert len(tsv_lines) == 647, f"Expected 647 TSV lines, got {len(tsv_lines)}"

with open('ALL_TEXT_cn.txt', 'r', encoding='utf-8') as f:
    cn_all = [l.strip('\r\n') for l in f]

assert len(cn_all) == 110622

modified_count = 0
for p in tsv_lines:
    lno = int(p[0])
    tag = p[1]
    txt = all_trans.get(lno, '')
    if tag != '<NO_TAB>':
        new_line = f"{tag}\t{txt}"
    else:
        new_line = txt
    
    idx = lno - 1
    if cn_all[idx] != new_line:
        cn_all[idx] = new_line
        modified_count += 1

with open('ALL_TEXT_cn.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(cn_all) + '\n')

print(f"Patched yum_004b Part 2: {modified_count} lines updated out of 647.")
