# -*- coding: utf-8 -*-
"""
Builder and validator for scripts/patch_com51.py
grisaia1/com51: Lines 25603 to 25982 (380 lines)
"""
import sys
import re

sys.path.insert(0, 'scripts')
import com51_part1
import com51_part2

POLISHED_LINES = (
    com51_part1.lines_part1 +
    com51_part2.lines_part2
)

def main():
    print(f"Total polished lines assembled: {len(POLISHED_LINES)}")
    assert len(POLISHED_LINES) == 380, f"Expected 380 lines, got {len(POLISHED_LINES)}"

    # Load scratch_com51.tsv
    with open("scratch_com51.tsv", "r", encoding="utf-8") as f:
        scratch = [line.rstrip("\n").split("\t") for line in f]

    assert len(scratch) == 380, f"scratch_com51.tsv has {len(scratch)} lines, expected 380"

    speaker_map = {
        '@雄二@': '@雄二@',
        '@天音@': '@天音@',
        '@蒔菜@': '@莳菜@',
        '@由美子@': '@由美子@',
        '@幸@': '@幸@',
        '@みちる@': '@满@',
        '@猫@': '@猫@'
    }

    tag_re = re.compile(r"(\$\[.*?\$\]|\[\$b.*?\$\]|\$d)")

    # Compare speaker markers and tags
    mismatches = 0
    for idx, (polished, sc) in enumerate(zip(POLISHED_LINES, scratch)):
        ja = sc[2]
        ja_speaker = re.match(r"^(@[^@]+@)", ja)
        pl_speaker = re.match(r"^(@[^@]+@)", polished)

        ja_sp_name = ja_speaker.group(1) if ja_speaker else None
        pl_sp_name = pl_speaker.group(1) if pl_speaker else None

        expected_pl = speaker_map.get(ja_sp_name)
        if expected_pl != pl_sp_name:
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

    print("ALL 380 LINES 100% PERFECTLY MATCHED! Writing scripts/patch_com51.py...")

    patch_py = []
    patch_py.append("# -*- coding: utf-8 -*-")
    patch_py.append('"""')
    patch_py.append("Apply patch to ALL_TEXT_cn.txt for grisaia1/com51 (lines 25603 to 25982)")
    patch_py.append('"""')
    patch_py.append("")
    patch_py.append("PATCH_ENTRIES = [")
    start_lno = 25603
    for idx, (pl, sc) in enumerate(zip(POLISHED_LINES, scratch)):
        lno = start_lno + idx
        sid = sc[1]
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
    patch_py.append("        lines[lno - 1] = f'{sid}\\t{new_text}\\n'")
    patch_py.append("    with open('ALL_TEXT_cn.txt', 'w', encoding='utf-8') as f:")
    patch_py.append("        f.writelines(lines)")
    patch_py.append("    print(f'Successfully patched grisaia1/com51 (lines {PATCH_ENTRIES[0][0]} to {PATCH_ENTRIES[-1][0]})!')")
    patch_py.append("")
    patch_py.append("if __name__ == '__main__':")
    patch_py.append("    apply_patch()")

    with open("scripts/patch_com51.py", "w", encoding="utf-8") as f:
        f.write("\n".join(patch_py) + "\n")

    print("Successfully generated scripts/patch_com51.py!")

if __name__ == "__main__":
    main()
