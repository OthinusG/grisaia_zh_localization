# -*- coding: utf-8 -*-
import sys
from scripts.ama_004_all import ama_004_lines

assert len(ama_004_lines) == 693

with open('ALL_TEXT_cn.txt', 'r', encoding='utf-8') as f:
    cn_lines = f.readlines()

total = len(cn_lines)
assert total == 110622

# Range is 2882..3575 (0-based)
slice_to_replace = cn_lines[2882:3575]
assert len(slice_to_replace) == 693
assert slice_to_replace[0].startswith('grisaia1/ama_004#00000\t')
assert slice_to_replace[-1].startswith('grisaia1/ama_004#00692\t')

new_slice = []
for i, line_text in enumerate(ama_004_lines):
    line_id = f"grisaia1/ama_004#{i:05d}"
    new_slice.append(f"{line_id}\t{line_text}\n")

cn_lines[2882:3575] = new_slice
assert len(cn_lines) == 110622

with open('ALL_TEXT_cn.txt', 'w', encoding='utf-8') as f:
    f.writelines(cn_lines)

print("Successfully patched ama_004 into ALL_TEXT_cn.txt!")
