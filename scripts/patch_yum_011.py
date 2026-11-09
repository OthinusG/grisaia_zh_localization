import json

def main():
    with open('tmp/yum_011_s1_done.json', 'r', encoding='utf-8') as f:
        s1 = json.load(f)
    with open('tmp/yum_011_s2_done.json', 'r', encoding='utf-8') as f:
        s2 = json.load(f)
    with open('tmp/yum_011_s3_done.json', 'r', encoding='utf-8') as f:
        s3 = json.load(f)

    full_trans = s1 + s2 + s3
    assert len(full_trans) == 987, f"Expected 987, got {len(full_trans)}"

    # Read ALL_TEXT.txt for range 65177 to 66164 (987 lines)
    with open('ALL_TEXT.txt', 'r', encoding='utf-8') as f:
        ja_lines = [next(f) for _ in range(66164)]
    target_ja = ja_lines[65177:66164]
    assert len(target_ja) == 987

    # Load existing ALL_TEXT_cn.txt
    with open('ALL_TEXT_cn.txt', 'r', encoding='utf-8') as f:
        cn_lines = f.readlines()
    assert len(cn_lines) == 110622, f"Expected 110622 lines in ALL_TEXT_cn.txt, got {len(cn_lines)}"

    new_cn_lines = list(cn_lines)
    for i in range(987):
        global_idx = 65177 + i
        ja_line = target_ja[i]
        trans_text = full_trans[i]

        if '\t' in ja_line:
            ja_id = ja_line.split('\t')[0]
            new_cn_lines[global_idx] = f"{ja_id}\t{trans_text}\n"
        else:
            if trans_text == "":
                new_cn_lines[global_idx] = "\n"
            else:
                new_cn_lines[global_idx] = f"{trans_text}\n"

    with open('ALL_TEXT_cn.txt', 'w', encoding='utf-8') as f:
        f.writelines(new_cn_lines)

    print("Successfully patched ALL_TEXT_cn.txt with yum_011 (987 lines)!")

if __name__ == '__main__':
    main()
