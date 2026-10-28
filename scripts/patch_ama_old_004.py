# -*- coding: utf-8 -*-
"""
Patch ama_old_004 into ALL_TEXT_cn.txt
Slice: 8972:9450 (478 lines, Line 8973 to Line 9450)
"""
import sys
sys.path.insert(0, 'scripts')
from ama_old_004_all import ama_old_004_lines

with open('ALL_TEXT.txt', 'r', encoding='utf-8') as f:
    jp_lines = [l.rstrip('\r\n') for l in f]

with open('ALL_TEXT_cn.txt', 'r', encoding='utf-8') as f:
    cn_lines = [l.rstrip('\r\n') for l in f]

assert len(jp_lines) == 110622
assert len(cn_lines) == 110622

start_idx = 8972
end_idx = 9450
total_lines = end_idx - start_idx
assert total_lines == 478
assert len(ama_old_004_lines) == 478

new_cn_slice = []
for i in range(total_lines):
    idx = start_idx + i
    jp_line = jp_lines[idx]
    old_cn_line = cn_lines[idx]
    pol_text = ama_old_004_lines[i]

    if '\t' in jp_line:
        jp_id, jp_content = jp_line.split('\t', 1)
        if '\t' in old_cn_line:
            cn_id, _ = old_cn_line.split('\t', 1)
            assert jp_id == cn_id, f"ID mismatch at {idx}: {jp_id} vs {cn_id}"
        else:
            cn_id = jp_id
        new_line = f"{cn_id}\t{pol_text}"
    else:
        new_line = pol_text
    new_cn_slice.append(new_line)

cn_lines[start_idx:end_idx] = new_cn_slice
assert len(cn_lines) == 110622

with open('ALL_TEXT_cn.txt', 'w', encoding='utf-8') as f:
    for l in cn_lines:
        f.write(l + '\n')

print(f"Successfully patched ama_old_004 ({total_lines} lines) into ALL_TEXT_cn.txt!")
