import json
import re

def main():
    with open('tmp/yum_010_s1_done.json', 'r', encoding='utf-8') as f:
        s1 = json.load(f)
    with open('tmp/yum_010_s2_done.json', 'r', encoding='utf-8') as f:
        s2 = json.load(f)

    full_trans = s1 + s2
    assert len(full_trans) == 587, f"Expected 587, got {len(full_trans)}"

    # Read ALL_TEXT.txt to get the line IDs for L64591 - L65177 (indices 64590 - 65176)
    with open('ALL_TEXT.txt', 'r', encoding='utf-8') as f:
        ja_lines = [next(f) for _ in range(65177)]
    
    target_ja = ja_lines[64590:65177]
    assert len(target_ja) == 587

    # Load existing ALL_TEXT_cn.txt
    with open('ALL_TEXT_cn.txt', 'r', encoding='utf-8') as f:
        cn_lines = f.readlines()

    assert len(cn_lines) == 110622, f"Expected 110622 lines in ALL_TEXT_cn.txt, got {len(cn_lines)}"

    # Patch lines
    new_cn_lines = list(cn_lines)
    for i in range(587):
        global_idx = 64590 + i
        ja_line = target_ja[i]
        ja_id = ja_line.split('\t')[0]
        new_text = full_trans[i]

        new_cn_lines[global_idx] = f"{ja_id}\t{new_text}\n"

    # Write patched file
    with open('ALL_TEXT_cn.txt', 'w', encoding='utf-8') as f:
        f.writelines(new_cn_lines)

    print("Successfully patched ALL_TEXT_cn.txt with yum_010 (587 lines)!")

if __name__ == '__main__':
    main()
