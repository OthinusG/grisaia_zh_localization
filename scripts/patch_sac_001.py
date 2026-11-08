#!/usr/bin/env python3
"""
Apply polished translations for grisaia1/sac_001 (L45223 - L45623, 401 lines).
"""
import os
import sys

sys.path.insert(0, os.path.abspath("."))
from tmp.prepare_sac_001 import get_sac_001_changes

def main():
    changes = get_sac_001_changes()
    print(f"Loaded {len(changes)} changes for sac_001.")

    with open("ALL_TEXT_cn.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    applied = 0
    for lnum, new_text in changes.items():
        idx = lnum - 1
        line = lines[idx]
        sid, _ = line.split("\t", 1)
        lines[idx] = f"{sid}\t{new_text}\n"
        applied += 1

    with open("ALL_TEXT_cn.txt", "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"Successfully applied {applied} changes to ALL_TEXT_cn.txt.")

if __name__ == "__main__":
    main()
