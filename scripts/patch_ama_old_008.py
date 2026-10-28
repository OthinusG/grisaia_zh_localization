import json
import sys
sys.path.insert(0, ".")

with open("tmp/ama_old_008_dump.json") as f:
    dump = json.load(f)

assert len(dump) == 240, f"Expected 240 lines in dump, got {len(dump)}"

from tmp.gen_ama_old_008_data import ama_old_008_polished
assert len(ama_old_008_polished) == 135, f"Expected 135 lines in polished dict, got {len(ama_old_008_polished)}"

formatted_lines = []
ne_idx = 0

for i, d in enumerate(dump):
    if not d["jp"].strip():
        text = ""
    else:
        text = ama_old_008_polished[ne_idx]
        ne_idx += 1
    
    # Check empty matching
    assert (d["jp"] == "") == (text == ""), f"Line {i} mismatch: jp={repr(d['jp'])} vs text={repr(text)}"
    
    if d["id"]:
        if d["has_tab"]:
            formatted_lines.append(f"{d['id']}\t{text}")
        else:
            formatted_lines.append(f"{d['id']}")
    else:
        formatted_lines.append(text)

assert len(formatted_lines) == 240
assert ne_idx == 135

# Patch into ALL_TEXT_cn.txt
with open("ALL_TEXT_cn.txt", "r", encoding="utf-8") as f:
    orig_cn = [line.rstrip("\r\n") for line in f]

assert len(orig_cn) == 110622, f"Expected 110622 lines, got {len(orig_cn)}"

# Lines 10461 to 10700 (0-indexed 10460 to 10700)
print(f"Index 10460 in orig: {orig_cn[10460][:40]}")
print(f"Index 10460 in patch: {formatted_lines[0][:40]}")
print(f"Index 10699 in orig: {orig_cn[10699][:40]}")
print(f"Index 10699 in patch: {formatted_lines[-1][:40]}")

orig_cn[10460:10700] = formatted_lines
assert len(orig_cn) == 110622, f"Total line count changed to {len(orig_cn)}!"

with open("ALL_TEXT_cn.txt", "w", encoding="utf-8") as f:
    for line in orig_cn:
        f.write(line + "\n")

print("Successfully patched ALL_TEXT_cn.txt for ama_old_008 (240 lines)!")
