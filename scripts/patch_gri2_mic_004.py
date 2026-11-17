# -*- coding: utf-8 -*-
"""
Patch ALL_TEXT_cn.txt for grisaia2/mic_004 (L73178 - L73555, 378 lines)
"""
import json

with open('tmp/mic_004_raw.json') as f:
    raw = json.load(f)

with open('tmp/mic_004_done.json') as f:
    done = json.load(f)

assert len(raw) == len(done) == 378

# Load all lines from ALL_TEXT_cn.txt
with open('ALL_TEXT_cn.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

assert len(lines) == 110622, f"Expected 110622 lines, got {len(lines)}"

start_idx = 73177
end_idx = 73177 + 378

for i in range(378):
    target_idx = start_idx + i
    prefix = lines[target_idx].split('\t')[0]
    expected_prefix = f"grisaia2/mic_004#{i:05d}"
    assert prefix == expected_prefix, f"Prefix mismatch at {target_idx}: {prefix} vs {expected_prefix}"
    lines[target_idx] = f"{prefix}\t{done[i]}\n"

with open('ALL_TEXT_cn.txt', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("ALL_TEXT_cn.txt successfully patched for mic_004!")
