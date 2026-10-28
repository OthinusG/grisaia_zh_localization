import sys
from scripts.ama_003_all import ama_003_lines

CN_FILE = "ALL_TEXT_cn.txt"

with open(CN_FILE, "r", encoding="utf-8") as f:
    cn_lines = f.readlines()

assert len(cn_lines) == 110622, f"Expected 110622 lines, got {len(cn_lines)}"
assert len(ama_003_lines) == 716, f"Expected 716 lines, got {len(ama_003_lines)}"

start_idx = 2166
end_idx = 2882

assert cn_lines[start_idx].startswith("grisaia1/ama_003#00000\t")
assert cn_lines[end_idx - 1].startswith("grisaia1/ama_003#00715\t")

for i, new_text in enumerate(ama_003_lines):
    line_id = cn_lines[start_idx + i].split("\t")[0]
    cn_lines[start_idx + i] = f"{line_id}\t{new_text}\n"

with open(CN_FILE, "w", encoding="utf-8") as f:
    f.writelines(cn_lines)

print(f"Successfully patched {len(ama_003_lines)} lines in {CN_FILE} (range {start_idx}..{end_idx})")
