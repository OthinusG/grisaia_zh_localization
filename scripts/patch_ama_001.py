#!/usr/bin/env python3
import json
import csv
import os
import re

def main():
    with open("ALL_TEXT.txt", "r", encoding="utf-8") as f:
        jp_lines = f.readlines()

    with open("ALL_TEXT_cn.txt", "r", encoding="utf-8") as f:
        cn_lines = f.readlines()

    assert len(jp_lines) == 110622, f"Expected 110622 jp lines, got {len(jp_lines)}"
    assert len(cn_lines) == 110622, f"Expected 110622 cn lines, got {len(cn_lines)}"

    start_idx = 66165 # 1-based
    end_idx = 66690   # 1-based

    # Load all parts
    polished = {}
    for part in ["p1", "p2", "p3", "p4"]:
        with open(f"tmp/ama_001_{part}.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            polished.update(data)

    assert len(polished) == 526, f"Expected 526 lines, got {len(polished)}"

    # Save merged tmp/ama_001_done.json
    with open("tmp/ama_001_done.json", "w", encoding="utf-8") as f:
        json.dump(polished, f, ensure_ascii=False, indent=2)

    os.makedirs("tsv", exist_ok=True)
    tsv_path = "tsv/ama_001.tsv"

    tsv_rows = []
    tsv_rows.append(["line_idx", "line_id", "jp_text", "old_cn", "new_cn"])

    tag_re = re.compile(r"(\$\[.*?\$\]|\[\$b.*?\$\])")
    speaker_re = re.compile(r"^@([^@]+)@")

    for idx in range(start_idx, end_idx + 1):
        line_0based = idx - 1
        jp_line = jp_lines[line_0based].rstrip("\r\n")
        old_cn_line = cn_lines[line_0based].rstrip("\r\n")

        if "\t" in jp_line:
            line_id, jp_text = jp_line.split("\t", 1)
        else:
            line_id = ""
            jp_text = jp_line

        if "\t" in old_cn_line:
            _, old_cn_text = old_cn_line.split("\t", 1)
        else:
            old_cn_text = old_cn_line

        new_cn_text = polished[str(idx)]

        # Validate tag count
        jp_tags = tag_re.findall(jp_text)
        cn_tags = tag_re.findall(new_cn_text)
        assert len(jp_tags) == len(cn_tags), f"Line {idx} tag mismatch: JP {jp_tags} vs CN {cn_tags}"

        # Validate speaker presence
        jp_sp = speaker_re.match(jp_text)
        cn_sp = speaker_re.match(new_cn_text)
        assert bool(jp_sp) == bool(cn_sp), f"Line {idx} speaker mismatch: JP {jp_sp} vs CN {cn_sp}"

        if line_id:
            new_cn_line = f"{line_id}\t{new_cn_text}\n"
        else:
            new_cn_line = f"{new_cn_text}\n"

        cn_lines[line_0based] = new_cn_line
        tsv_rows.append([str(idx), line_id, jp_text, old_cn_text, new_cn_text])

    with open("ALL_TEXT_cn.txt", "w", encoding="utf-8") as f:
        f.writelines(cn_lines)

    with open(tsv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerows(tsv_rows)

    print(f"Successfully patched lines {start_idx} to {end_idx}. Saved {tsv_path}.")

if __name__ == "__main__":
    main()
