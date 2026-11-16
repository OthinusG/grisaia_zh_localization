# -*- coding: utf-8 -*-
import os, sys, json

def main():
    sys.path.insert(0, os.path.abspath('.'))
    with open('tmp/mak_007_raw.json', 'r', encoding='utf-8') as f:
        raw = json.load(f)

    from tmp.build_mak_007 import lines

    assert len(lines) == len(raw)

    with open('ALL_TEXT_cn.txt', 'r', encoding='utf-8') as f:
        all_cn = f.readlines()

    for r, new_text in zip(raw, lines):
        idx = r['line'] - 1
        old_line = all_cn[idx].rstrip('\r\n')
        parts = old_line.split('\t')
        assert len(parts) == 2, f"Invalid line {idx+1}: {old_line}"
        all_cn[idx] = f"{parts[0]}\t{new_text}\n"

    with open('ALL_TEXT_cn.txt', 'w', encoding='utf-8') as f:
        f.writelines(all_cn)

    print(f"Successfully patched {len(lines)} lines for mak_007!")

if __name__ == '__main__':
    main()
