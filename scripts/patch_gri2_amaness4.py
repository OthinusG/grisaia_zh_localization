import json
import os

def main():
    with open("tmp/amaness4.json", "r", encoding="utf-8") as f:
        all_cn = json.load(f)

    assert len(all_cn) == 108, f"Expected 108 lines, got {len(all_cn)}"

    with open("ALL_TEXT.txt", "r", encoding="utf-8") as f:
        ja_lines = [l.rstrip("\r\n") for l in f.readlines()]

    with open("ALL_TEXT_cn.txt", "r", encoding="utf-8") as f:
        cn_lines = [l.rstrip("\r\n") for l in f.readlines()]

    assert len(ja_lines) == 110622
    assert len(cn_lines) == 110622

    # Prepare tsv
    os.makedirs("tsv", exist_ok=True)
    tsv_lines = []
    
    start_lno = 68601
    end_lno = 68708
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

    with open("ALL_TEXT_cn.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(cn_lines) + "\n")

    with open("tsv/amaness4.tsv", "w", encoding="utf-8") as f:
        f.writelines(tsv_lines)

    print(f"Successfully patched {len(all_cn)} lines (L{start_lno}-L{end_lno}) into ALL_TEXT_cn.txt and wrote tsv/amaness4.tsv")

if __name__ == "__main__":
    main()
