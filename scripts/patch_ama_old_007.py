import json
import sys
sys.path.insert(0, ".")

# 1. Load Part 1
import importlib.util
spec1 = importlib.util.spec_from_file_location("p1", "tmp/build_ama_old_007_p1.py")
mod1 = importlib.util.module_from_spec(spec1)
spec1.loader.exec_module(mod1)
p1_lines = mod1.p1_lines
assert len(p1_lines) == 350, f"Expected 350 lines in p1, got {len(p1_lines)}"

# 2. Build Part 2
with open("tmp/ama_old_007_dump.json") as f:
    dump = json.load(f)

p2_dump = dump[350:]
assert len(p2_dump) == 346, f"Expected 346 lines in p2_dump, got {len(p2_dump)}"

from tmp.gen_p2_data import p2_polished
p2_lines = []
ne_idx = 0
for i, d in enumerate(p2_dump):
    if not d["jp"].strip():
        p2_lines.append("")
    else:
        p2_lines.append(p2_polished[ne_idx])
        ne_idx += 1

assert len(p2_lines) == 346, f"Expected 346 lines in p2, got {len(p2_lines)}"

all_lines = p1_lines + p2_lines
assert len(all_lines) == 696, f"Expected 696 lines, got {len(all_lines)}"

# 3. Verify against dump
for i in range(696):
    d = dump[i]
    p = all_lines[i]
    d_empty = (d["jp"] == "")
    p_empty = (p == "")
    assert d_empty == p_empty, f"Line {i} mismatch: dump={d_empty}, p={p_empty}"

# 4. Format lines with IDs and tabs
formatted_lines = []
for i in range(696):
    d = dump[i]
    text = all_lines[i]
    if d["id"]:
        if d["has_tab"]:
            formatted_lines.append(f"{d['id']}\t{text}")
        else:
            formatted_lines.append(f"{d['id']}")
    else:
        formatted_lines.append(text)

assert len(formatted_lines) == 696

# 5. Read ALL_TEXT_cn.txt and patch lines 9765 to 10460 (0-indexed 9764 to 10460)
with open("ALL_TEXT_cn.txt", "r", encoding="utf-8") as f:
    orig_cn = [line.rstrip("\r\n") for line in f]

assert len(orig_cn) == 110622, f"Expected 110622 lines, got {len(orig_cn)}"

# Verify slice boundaries
# Line 9765 (index 9764) is the start of ama_old_007
# Line 10460 (index 10459) is the end of ama_old_007
print(f"Index 9764 in orig: {orig_cn[9764][:40]}")
print(f"Index 9764 in patch: {formatted_lines[0][:40]}")
print(f"Index 10459 in orig: {orig_cn[10459][:40]}")
print(f"Index 10459 in patch: {formatted_lines[-1][:40]}")

orig_cn[9764:10460] = formatted_lines
assert len(orig_cn) == 110622, f"Total line count changed to {len(orig_cn)}!"

with open("ALL_TEXT_cn.txt", "w", encoding="utf-8") as f:
    for line in orig_cn:
        f.write(line + "\n")

print("Successfully patched ALL_TEXT_cn.txt for ama_old_007 (696 lines)!")
