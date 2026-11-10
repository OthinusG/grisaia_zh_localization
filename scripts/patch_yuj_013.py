# -*- coding: utf-8 -*-
"""
Patch yuj_013 into ALL_TEXT_cn.txt and export tsv/yuj_013.tsv.
Lines: 84002 - 84260 (259 lines)
"""
import json

with open("tmp/yuj_013_done.json", "r", encoding="utf-8") as f:
    done_items = json.load(f)

pol_by_idx = {it["line_idx"]: it for it in done_items}

with open("ALL_TEXT_cn.txt", "r", encoding="utf-8") as f:
    cn_lines = f.readlines()

tsv_rows = []
tsv_rows.append("Line\tID\tJapanese\tOld Chinese\tNew Chinese\n")

with open("tmp/yuj_013_raw.json", "r", encoding="utf-8") as f:
    raw_items = json.load(f)

raw_by_idx = {it["line_idx"]: it for it in raw_items}

patched_count = 0
for idx in range(84002, 84261):
    raw_item = raw_by_idx[idx]
    pol_item = pol_by_idx[idx]
    
    line_id = raw_item["line_id"]
    jp_text = raw_item["jp_text"]
    old_cn = raw_item["cn_text"]
    new_cn = pol_item["cn_text"]
    has_tab = raw_item["has_tab"]
    
    tsv_rows.append(f"{idx}\t{line_id}\t{jp_text}\t{old_cn}\t{new_cn}\n")
    
    if has_tab:
        cn_lines[idx - 1] = f"{line_id}\t{new_cn}\n"
    else:
        cn_lines[idx - 1] = f"{new_cn}\n"
    patched_count += 1

with open("ALL_TEXT_cn.txt", "w", encoding="utf-8") as f:
    f.writelines(cn_lines)

with open("tsv/yuj_013.tsv", "w", encoding="utf-8") as f:
    f.writelines(tsv_rows)

print(f"Successfully patched {patched_count} lines (84002-84260) and saved tsv/yuj_013.tsv")
