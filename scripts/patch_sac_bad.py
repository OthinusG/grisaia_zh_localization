# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, ".")

from tmp.sac_bad_data import data

with open("ALL_TEXT.txt", "r", encoding="utf-8") as f:
    ja_lines = f.readlines()

with open("ALL_TEXT_cn.txt", "r", encoding="utf-8") as f:
    cn_lines = f.readlines()

assert len(ja_lines) == 110622, f"Expected 110622 lines, got {len(ja_lines)}"
assert len(cn_lines) == 110622, f"Expected 110622 lines, got {len(cn_lines)}"

mod_count = 0
for lnum, new_text in data.items():
    idx = lnum - 1
    ja_raw = ja_lines[idx].rstrip("\r\n")
    cn_raw = cn_lines[idx].rstrip("\r\n")
    
    if "\t" in ja_raw:
        code = ja_raw.split("\t")[0]
        old_text = cn_raw.split("\t")[1] if "\t" in cn_raw else cn_raw
        if old_text != new_text:
            cn_lines[idx] = f"{code}\t{new_text}\n"
            mod_count += 1
    else:
        if cn_raw != new_text:
            cn_lines[idx] = f"{new_text}\n"
            mod_count += 1

print(f"Total lines modified in sac_bad: {mod_count}")

with open("ALL_TEXT_cn.txt", "w", encoding="utf-8") as f:
    f.writelines(cn_lines)

print("Patching complete.")
