# -*- coding: utf-8 -*-
"""
Patch polished translation for grisaia1/mak_h into ALL_TEXT_cn.txt.
Slice: lines 37098 to 37184 (index 37097 to 37184, 87 lines).
"""

from scripts.mak_h_all import mak_h_lines

ALL_TEXT_CN = "ALL_TEXT_cn.txt"
START_IDX = 37097
END_IDX = 37184
EXPECTED_COUNT = 87

def patch():
    assert len(mak_h_lines) == EXPECTED_COUNT, f"Expected {EXPECTED_COUNT} lines, got {len(mak_h_lines)}"
    
    with open(ALL_TEXT_CN, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    assert len(lines) == 110622, f"Total lines mismatch: {len(lines)}"
    
    # Check current slice IDs
    first_id = lines[START_IDX].split("\t")[0]
    last_id = lines[END_IDX - 1].split("\t")[0]
    assert first_id == "grisaia1/mak_h#00000", f"Unexpected first id: {first_id}"
    assert last_id == "grisaia1/mak_h#00086", f"Unexpected last id: {last_id}"
    
    patched_count = 0
    for i, polished_text in enumerate(mak_h_lines):
        idx = START_IDX + i
        line_id = lines[idx].split("\t")[0]
        lines[idx] = f"{line_id}\t{polished_text}\n"
        patched_count += 1
        
    with open(ALL_TEXT_CN, "w", encoding="utf-8") as f:
        f.writelines(lines)
        
    print(f"Successfully patched {patched_count} lines into {ALL_TEXT_CN} (L{START_IDX+1} - L{END_IDX}).")

if __name__ == "__main__":
    patch()
