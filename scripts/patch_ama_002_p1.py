# -*- coding: utf-8 -*-
"""
Patch polished translation for grisaia1/ama_002 Part 1 into ALL_TEXT_cn.txt.
Slice: lines 1164 to 1665 (index 1163 to 1665, 502 lines).
"""

from scripts.ama_002_p1_all import ama_002_p1_lines

ALL_TEXT_CN = "ALL_TEXT_cn.txt"
START_IDX = 1163
END_IDX = 1665
EXPECTED_COUNT = 502

def patch():
    assert len(ama_002_p1_lines) == EXPECTED_COUNT, f"Expected {EXPECTED_COUNT} lines, got {len(ama_002_p1_lines)}"
    
    with open(ALL_TEXT_CN, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    assert len(lines) == 110622, f"Total lines mismatch: {len(lines)}"
    
    # Check current slice IDs
    first_id = lines[START_IDX].split("\t")[0]
    last_id = lines[END_IDX - 1].split("\t")[0]
    assert first_id == "grisaia1/ama_002#00000", f"Unexpected first id: {first_id}"
    assert last_id == "grisaia1/ama_002#00501", f"Unexpected last id: {last_id}"
    
    patched_count = 0
    for i, polished_text in enumerate(ama_002_p1_lines):
        idx = START_IDX + i
        line_id = lines[idx].split("\t")[0]
        lines[idx] = f"{line_id}\t{polished_text}\n"
        patched_count += 1
        
    with open(ALL_TEXT_CN, "w", encoding="utf-8") as f:
        f.writelines(lines)
        
    print(f"Successfully patched {patched_count} lines into {ALL_TEXT_CN} (L{START_IDX+1} - L{END_IDX}).")

if __name__ == "__main__":
    patch()
