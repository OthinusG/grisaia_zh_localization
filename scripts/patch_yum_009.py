# coding: utf-8
import json

with open('tmp/yum_009_done.json', 'r', encoding='utf-8') as f:
    trans = json.load(f)

assert len(trans) == 288

with open('ALL_TEXT_cn.txt', 'r', encoding='utf-8') as f:
    cn_lines = f.readlines()

start_idx = 64302
end_idx = 64590

print(f"Original line count: {len(cn_lines)}")
print(f"Patching lines {start_idx + 1} to {end_idx}...")

for i, text in enumerate(trans):
    line_idx = start_idx + i
    orig_parts = cn_lines[line_idx].rstrip('\r\n').split('\t', 1)
    line_id = orig_parts[0]
    cn_lines[line_idx] = f"{line_id}\t{text}\n"

with open('ALL_TEXT_cn.txt', 'w', encoding='utf-8') as f:
    f.writelines(cn_lines)

print("Patch complete! Verifying updated line count...")
with open('ALL_TEXT_cn.txt', 'r', encoding='utf-8') as f:
    new_lines = f.readlines()

assert len(new_lines) == 110622
print(f"Verified line count: {len(new_lines)}")
