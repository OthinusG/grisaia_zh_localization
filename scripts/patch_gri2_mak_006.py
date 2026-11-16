# -*- coding: utf-8 -*-
import sys

def main():
    with open('tmp/mak_006_raw.json', 'r', encoding='utf-8') as f:
        import json
        raw = json.load(f)

    from tmp.build_mak_006 import lines

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

    print(f"Successfully patched {len(lines)} lines for mak_006!")

if __name__ == '__main__':
    main()
