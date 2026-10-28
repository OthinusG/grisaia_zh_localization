# -*- coding: utf-8 -*-
"""
Builder and validator for scripts/patch_com49.py
grisaia1/com49: Lines 24378 to 25242 (865 lines)
"""
import sys
import re

sys.path.insert(0, 'scripts')
import com49_part1
import com49_part2
import com49_part3
import com49_part4

POLISHED_LINES = (
    com49_part1.PART1_LINES +
    com49_part2.PART2_LINES +
    com49_part3.PART3_LINES +
    com49_part4.PART4_LINES
)

def main():
    print(f"Total polished lines assembled: {len(POLISHED_LINES)}")
    assert len(POLISHED_LINES) == 865, f"Expected 865 lines, got {len(POLISHED_LINES)}"

    # Load scratch_com49.tsv
    with open("scratch_com49.tsv", "r", encoding="utf-8") as f:
        scratch = [line.rstrip("\n").split("\t") for line in f]

    assert len(scratch) == 865, f"scratch_com49.tsv has {len(scratch)} lines, expected 865"

    tag_re = re.compile(r"(\$\[.*?\$\]|\[\$b.*?\$\]|\$d)")

    # Compare speaker markers and tags
    mismatches = 0
    for idx, (polished, sc) in enumerate(zip(POLISHED_LINES, scratch)):
        ja = sc[2]
        ja_speaker = re.match(r"^@([^@]+)@", ja)
        pl_speaker = re.match(r"^@([^@]+)@", polished)

        ja_sp_name = ja_speaker.group(1) if ja_speaker else None
        pl_sp_name = pl_speaker.group(1) if pl_speaker else None

        if ja_sp_name != pl_sp_name:
            print(f"Speaker mismatch at index {idx} ({sc[0]} / {sc[1]}):")
            print(f"  JA: {ja}")
            print(f"  PL: {polished}")
            mismatches += 1

        ja_tags = tag_re.findall(ja)
        pl_tags = tag_re.findall(polished)
        if len(ja_tags) != len(pl_tags):
            print(f"Tag mismatch at index {idx} ({sc[0]} / {sc[1]}):")
            print(f"  JA ({len(ja_tags)}): {ja}")
            print(f"  PL ({len(pl_tags)}): {polished}")
            mismatches += 1

    if mismatches > 0:
        print(f"Found {mismatches} mismatches! Please fix.")
        return

    print("ALL 865 LINES 100% PERFECTLY MATCHED! Writing scripts/patch_com49.py...")

    patch_py = []
    patch_py.append("# -*- coding: utf-8 -*-")
    patch_py.append('"""')
    patch_py.append("Apply patch to ALL_TEXT_cn.txt for grisaia1/com49 (lines 24378 to 25242)")
    patch_py.append('"""')
    patch_py.append("")
    patch_py.append("PATCH_ENTRIES = [")
    for pl, sc in zip(POLISHED_LINES, scratch):
        lno = int(sc[0])
        sid = sc[1]
        if sid.startswith('L'):
            patch_py.append(f"    ({lno}, '', {repr(pl)}),")
        else:
            patch_py.append(f"    ({lno}, {repr(sid)}, {repr(pl)}),")
    patch_py.append("]")
    patch_py.append("")
    patch_py.append("def apply_patch():")
    patch_py.append("    print(f'Total patch entries: {len(PATCH_ENTRIES)}')")
    patch_py.append("    with open('ALL_TEXT_cn.txt', 'r', encoding='utf-8') as f:")
    patch_py.append("        lines = f.readlines()")
    patch_py.append("    print(f'Original line {PATCH_ENTRIES[0][0]}: {lines[PATCH_ENTRIES[0][0] - 1].strip()}')")
    patch_py.append("    print(f'Original line {PATCH_ENTRIES[-1][0]}: {lines[PATCH_ENTRIES[-1][0] - 1].strip()}')")
    patch_py.append("    for lno, sid, new_text in PATCH_ENTRIES:")
    patch_py.append("        if sid:")
    patch_py.append("            lines[lno - 1] = f'{sid}\\t{new_text}\\n'")
    patch_py.append("        else:")
    patch_py.append("            lines[lno - 1] = f'{new_text}\\n'")
    patch_py.append("    with open('ALL_TEXT_cn.txt', 'w', encoding='utf-8') as f:")
    patch_py.append("        f.writelines(lines)")
    patch_py.append("    print(f'Successfully patched grisaia1/com49 (lines {PATCH_ENTRIES[0][0]} to {PATCH_ENTRIES[-1][0]})!')")
    patch_py.append("")
    patch_py.append("if __name__ == '__main__':")
    patch_py.append("    apply_patch()")

    with open("scripts/patch_com49.py", "w", encoding="utf-8") as f:
        f.write("\n".join(patch_py) + "\n")

    print("Successfully generated scripts/patch_com49.py!")

if __name__ == "__main__":
    main()
