#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patch ALL_TEXT_cn.txt for yum_006 (L61721 - L62470, 750 lines)
"""

import sys
sys.path.insert(0, 'tmp')
from trans_006_s1 import trans_slice1
from trans_006_s2 import trans_slice2
from trans_006_s3 import trans_slice3

all_trans = {}
for k, v in trans_slice1.items():
    all_trans[int(k)] = v
for k, v in trans_slice2.items():
    all_trans[int(k)] = v
for k, v in trans_slice3.items():
    all_trans[int(k)] = v

assert len(all_trans) == 750, f"Expected 750 text entries, got {len(all_trans)}"

with open('tsv/yum_006.tsv', 'r', encoding='utf-8') as f:
    tsv_lines = [l.strip('\n').split('\t') for l in f]

assert len(tsv_lines) == 750, f"Expected 750 TSV lines, got {len(tsv_lines)}"

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

print(f"Patched yum_006: {modified_count} lines updated out of 750.")
