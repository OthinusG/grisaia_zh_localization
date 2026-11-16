import json
import os

def main():
    with open("tmp/ama_004_p1.json", "r", encoding="utf-8") as f:
        p1 = json.load(f)
    with open("tmp/ama_004_p2.json", "r", encoding="utf-8") as f:
        p2 = json.load(f)
    with open("tmp/ama_004_p3.json", "r", encoding="utf-8") as f:
        p3 = json.load(f)
    with open("tmp/ama_004_p4.json", "r", encoding="utf-8") as f:
        p4 = json.load(f)

    all_cn = p1 + p2 + p3 + p4
    assert len(all_cn) == 560, f"Expected 560 lines, got {len(all_cn)}"

    with open("ALL_TEXT.txt", "r", encoding="utf-8") as f:
        ja_lines = [l.rstrip("\r\n") for l in f.readlines()]

    with open("ALL_TEXT_cn.txt", "r", encoding="utf-8") as f:
        cn_lines = [l.rstrip("\r\n") for l in f.readlines()]

    assert len(ja_lines) == 110622
    assert len(cn_lines) == 110622

    # Prepare tsv
    os.makedirs("tsv", exist_ok=True)
    tsv_lines = []
    
    start_lno = 66853
    end_lno = 67412
    for idx, text in enumerate(all_cn):
        lno = start_lno + idx
        ja = ja_lines[lno - 1]
        sid = ja.split("\t")[0] if "\t" in ja else ""
        
        # Format line for ALL_TEXT_cn.txt
        if "\t" in ja:
            new_line = f"{sid}\t{text}"
            tsv_lines.append(f"{sid}\t{text}\n")
        else:
            new_line = text
            tsv_lines.append(f"{text}\n")
            
        cn_lines[lno - 1] = new_line

    with open("tsv/ama_004.tsv", "w", encoding="utf-8") as f:
        f.writelines(tsv_lines)
    print(f"Wrote {len(tsv_lines)} lines to tsv/ama_004.tsv")

    with open("ALL_TEXT_cn.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(cn_lines) + "\n")
    print(f"Updated ALL_TEXT_cn.txt lines {start_lno} to {end_lno} successfully!")

if __name__ == "__main__":
    main()
