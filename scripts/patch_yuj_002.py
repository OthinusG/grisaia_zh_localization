# -*- coding: utf-8 -*-
import json
import re

with open("tmp/yuj_002_raw.json", "r", encoding="utf-8") as f:
    raw_items = json.load(f)

with open("tmp/yuj_002_s1_done.json", "r", encoding="utf-8") as f:
    s1 = json.load(f)

with open("tmp/yuj_002_s2_done.json", "r", encoding="utf-8") as f:
    s2 = json.load(f)

all_polished = s1 + s2
assert len(all_polished) == len(raw_items) == 581, f"Mismatch in count: {len(all_polished)} vs {len(raw_items)}"

with open("ALL_TEXT.txt", "r", encoding="utf-8") as fj:
    ja_lines = [l.rstrip("\r\n") for l in fj]

# Verify every single line against raw Japanese for tags & speakers
tag_re = re.compile(r"(\$\[.*?\$\]|\[\$.*?\$\])")
sp_re = re.compile(r"^@.*?@")

tsv_lines = []
for idx, (raw, pol) in enumerate(zip(raw_items, all_polished)):
    line_no = raw["line"]
    j_raw = ja_lines[line_no - 1]
    
    # check speaker
    j_sp = sp_re.match(raw["ja"])
    c_sp = sp_re.match(pol)
    assert bool(j_sp) == bool(c_sp), f"Line {line_no} speaker mismatch: {raw['ja']} vs {pol}"
    
    # check tags
    j_tags = tag_re.findall(raw["ja"])
    c_tags = tag_re.findall(pol)
    assert len(j_tags) == len(c_tags), f"Line {line_no} tag count mismatch: {j_tags} vs {c_tags}"
    
    if "\t" in j_raw:
        sid = j_raw.split("\t", 1)[0]
        tsv_lines.append(f"{sid}\t{pol}\n")
    else:
        tsv_lines.append(f"{pol}\n")

# Write to tsv/yuj_002.tsv
with open("tsv/yuj_002.tsv", "w", encoding="utf-8") as f:
    f.writelines(tsv_lines)

print(f"Generated tsv/yuj_002.tsv with {len(tsv_lines)} lines.")

# Patch ALL_TEXT_cn.txt
with open("ALL_TEXT_cn.txt", "r", encoding="utf-8") as f:
    cn_lines = [l.rstrip("\r\n") for l in f]

assert len(cn_lines) == 110622, f"Expected 110622, got {len(cn_lines)}"

start_lno = 78856
end_lno = 79436
for idx, pol in enumerate(all_polished):
    lno = start_lno + idx
    j_raw = ja_lines[lno - 1]
    if "\t" in j_raw:
        sid = j_raw.split("\t", 1)[0]
        cn_lines[lno - 1] = f"{sid}\t{pol}"
    else:
        cn_lines[lno - 1] = pol

with open("ALL_TEXT_cn.txt", "w", encoding="utf-8") as f:
    for l in cn_lines:
        f.write(l + "\n")

print(f"Patched ALL_TEXT_cn.txt lines {start_lno} to {end_lno} successfully!")
