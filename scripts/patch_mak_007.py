# scripts/patch_mak_007.py
import sys
from mak_007_part1 import mak_007_part1
from mak_007_part2 import mak_007_part2

part_lines = mak_007_part1 + mak_007_part2
assert len(part_lines) == 618

with open("ALL_TEXT_cn.txt", "r", encoding="utf-8") as f:
    cn_lines = f.readlines()

assert len(cn_lines) == 110622

with open("scratch_mak_007.tsv", "r", encoding="utf-8") as f:
    tsv_lines = [line.strip("\r\n").split("\t") for line in f]

assert len(tsv_lines) == 618

# Verify line IDs match exactly
for i in range(618):
    target_idx = 29529 + i
    current_line = cn_lines[target_idx]
    tsv_id = tsv_lines[i][1]
    if "\t" in current_line:
        cid, _ = current_line.split("\t", 1)
    else:
        cid = current_line.strip("\r\n")
    assert cid == tsv_id, f"Line ID mismatch at {target_idx}: {cid} vs {tsv_id}"

# Apply patch
for i in range(618):
    target_idx = 29529 + i
    tsv_id = tsv_lines[i][1]
    new_text = part_lines[i]
    cn_lines[target_idx] = f"{tsv_id}\t{new_text}\n"

with open("ALL_TEXT_cn.txt", "w", encoding="utf-8") as f:
    f.writelines(cn_lines)

print(f"Successfully patched {len(part_lines)} lines for mak_007 (lines 29530 to 30147).")
