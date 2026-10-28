# -*- coding: utf-8 -*-
import importlib.util
import sys

spec = importlib.util.spec_from_file_location('ama_005_all', 'scripts/ama_005_all.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
ama_005_lines = mod.ama_005_lines
assert len(ama_005_lines) == 779

with open('ALL_TEXT.txt', 'r', encoding='utf-8') as f_ja:
    lines_ja = f_ja.readlines()

with open('ALL_TEXT_cn.txt', 'r', encoding='utf-8') as f_cn:
    lines_cn = f_cn.readlines()

assert len(lines_ja) == 110622
assert len(lines_cn) == 110622

start_idx = 3575
end_idx = 4354  # 4354 is exclusive, count = 779 lines: lines 3576 to 4354

slice_ja = lines_ja[start_idx:end_idx]
assert len(slice_ja) == 779

patched_cn = []
for idx, (l_ja, text_cn) in enumerate(zip(slice_ja, ama_005_lines)):
    if '\t' in l_ja:
        line_id = l_ja.split('\t')[0]
        patched_cn.append(f"{line_id}\t{text_cn}\n")
    else:
        # Continuation line without tab/ID (lines 4332, 4333, 4335)
        patched_cn.append(f"{text_cn}\n")

assert len(patched_cn) == 779

new_lines_cn = lines_cn[:start_idx] + patched_cn + lines_cn[end_idx:]
assert len(new_lines_cn) == 110622

with open('ALL_TEXT_cn.txt', 'w', encoding='utf-8') as f:
    f.writelines(new_lines_cn)

print(f"Successfully patched ALL_TEXT_cn.txt lines {start_idx+1} to {end_idx} (779 lines).")
