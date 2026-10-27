#!/usr/bin/env python3
"""
Patch Manager for Grisaia Localization scripts.
Supports extracting line ranges/scenes and applying patches atomically.
"""

import sys
import shutil
import os
import argparse
from verify_alignment import verify

def extract(start_line, end_line, out_file):
    with open("ALL_TEXT.txt", "r", encoding="utf-8") as fj, open("ALL_TEXT_cn.txt", "r", encoding="utf-8") as fc:
        ja_lines = fj.readlines()
        cn_lines = fc.readlines()

    with open(out_file, "w", encoding="utf-8") as fo:
        for idx in range(start_line - 1, min(end_line, len(ja_lines))):
            fo.write(f"// LINE {idx+1}\n")
            fo.write(f"JA: {ja_lines[idx]}")
            fo.write(f"CN: {cn_lines[idx]}\n")
    print(f"Extracted lines {start_line} to {end_line} to {out_file}")

def apply_patch(patch_file, start_line, end_line):
    # patch_file must contain lines in `<id>\t<text>` or empty/continuation lines
    with open(patch_file, "r", encoding="utf-8") as fp:
        patch_lines = [l.rstrip("\r\n") for l in fp]

    expected_count = end_line - start_line + 1
    if len(patch_lines) != expected_count:
        print(f"[FAIL] Patch line count ({len(patch_lines)}) != expected ({expected_count})")
        return False

    with open("ALL_TEXT_cn.txt", "r", encoding="utf-8") as fc:
        cn_lines = [l.rstrip("\r\n") for l in fc]

    # Backup
    backup_path = "ALL_TEXT_cn.txt.bak"
    shutil.copyfile("ALL_TEXT_cn.txt", backup_path)

    # Replace lines
    cn_lines[start_line - 1 : end_line] = patch_lines

    # Write back
    with open("ALL_TEXT_cn.txt", "w", encoding="utf-8") as fc:
        for l in cn_lines:
            fc.write(l + "\n")

    # Verify
    if verify():
        print(f"[SUCCESS] Applied patch for lines {start_line}-{end_line}. Verification passed!")
        if os.path.exists(backup_path):
            os.remove(backup_path)
        return True
    else:
        print(f"[FAIL] Verification failed! Rolling back from backup...")
        shutil.copyfile(backup_path, "ALL_TEXT_cn.txt")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="cmd")

    p_extract = subparsers.add_parser("extract")
    p_extract.add_argument("--start", type=int, required=True)
    p_extract.add_argument("--end", type=int, required=True)
    p_extract.add_argument("--out", type=str, required=True)

    p_apply = subparsers.add_parser("apply")
    p_apply.add_argument("--patch", type=str, required=True)
    p_apply.add_argument("--start", type=int, required=True)
    p_apply.add_argument("--end", type=int, required=True)

    args = parser.parse_args()
    if args.cmd == "extract":
        extract(args.start, args.end, args.out)
    elif args.cmd == "apply":
        apply_patch(args.patch, args.start, args.end)
    else:
        parser.print_help()
