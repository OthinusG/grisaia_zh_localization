# -*- coding: utf-8 -*-
start = 27297
end = 27760
with open('ALL_TEXT.txt', 'r', encoding='utf-8') as f_ja, open('ALL_TEXT_cn.txt', 'r', encoding='utf-8') as f_cn:
    ja_lines = [f_ja.readline() for _ in range(end)]
    cn_lines = [f_cn.readline() for _ in range(end)]

rows = []
for i in range(start - 1, end):
    ja_l = ja_lines[i].strip()
    cn_l = cn_lines[i].strip()
    ja_parts = ja_l.split('\t')
    cn_parts = cn_l.split('\t')
    sid = ja_parts[0]
    ja_txt = ja_parts[1] if len(ja_parts) > 1 else ''
    cn_txt = cn_parts[1] if len(cn_parts) > 1 else ''
    rows.append(f"{i - start + 1}\t{sid}\t{ja_txt}\t{cn_parts[0]}\t{cn_txt}")

with open('scratch_mak_003.tsv', 'w', encoding='utf-8') as f_out:
    f_out.write('\n'.join(rows) + '\n')

print(f"Wrote scratch_mak_003.tsv with {len(rows)} lines")

tags = []
for idx, r in enumerate(rows):
    parts = r.split('\t')
    ja = parts[2]
    for tag in ['$[', '[$', '$d', '$S']:
        if tag in ja:
            tags.append((idx, parts[1], ja))
            break
print(f"Found {len(tags)} tags in mak_003:")
for t in tags:
    print(t)
