import json
import sys
sys.path.insert(0, ".")

with open("tmp/ama_old_009_dump.json") as f:
    dump = json.load(f)

assert len(dump) == 320, f"Expected 320 lines in dump, got {len(dump)}"

from tmp.gen_ama_old_009_data import ama_old_009_polished
assert len(ama_old_009_polished) == 177, f"Expected 177 lines in polished dict, got {len(ama_old_009_polished)}"

formatted_lines = []
ne_idx = 0

for i, d in enumerate(dump):
    if not d["jp"].strip():
        text = ""
    else:
        text = ama_old_009_polished[ne_idx]
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

assert len(formatted_lines) == 320
assert ne_idx == 177

# Patch into ALL_TEXT_cn.txt
with open("ALL_TEXT_cn.txt", "r", encoding="utf-8") as f:
    orig_cn = [line.rstrip("\r\n") for line in f]

assert len(orig_cn) == 110622, f"Expected 110622 lines, got {len(orig_cn)}"

# Lines 10701 to 11020 (0-indexed 10700 to 11020)
print(f"Index 10700 in orig: {orig_cn[10700][:40]}")
print(f"Index 10700 in patch: {formatted_lines[0][:40]}")
print(f"Index 11019 in orig: {orig_cn[11019][:40]}")
print(f"Index 11019 in patch: {formatted_lines[-1][:40]}")

orig_cn[10700:11020] = formatted_lines
assert len(orig_cn) == 110622, f"Total line count changed to {len(orig_cn)}!"

with open("ALL_TEXT_cn.txt", "w", encoding="utf-8") as f:
    for line in orig_cn:
        f.write(line + "\n")

print("Successfully patched ALL_TEXT_cn.txt for ama_old_009 (320 lines)!")
