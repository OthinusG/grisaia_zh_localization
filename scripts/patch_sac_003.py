#!/usr/bin/env python3
"""
Apply polished translations for grisaia1/sac_003 (L45966 - L46440, 475 lines).
"""
import os
import sys

sys.path.insert(0, os.path.abspath("."))
from tmp.build_sac_003 import generate_translations

def main():
    changes = generate_translations()
    print(f"Loaded {len(changes)} changes for sac_003.")

    with open("ALL_TEXT_cn.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    applied = 0
    for lnum, new_text in changes.items():
        idx = lnum - 1
        line = lines[idx]
        if "\t" in line:
            sid, _ = line.split("\t", 1)
            lines[idx] = f"{sid}\t{new_text}\n"
        else:
            lines[idx] = f"{new_text}\n" if new_text else "\n"
        applied += 1

    with open("ALL_TEXT_cn.txt", "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"Successfully applied {applied} changes to ALL_TEXT_cn.txt.")

if __name__ == "__main__":
    main()
