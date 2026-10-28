import sys

def verify_file(tsv_file, part_list, start_idx, end_idx):
    with open(tsv_file, 'r', encoding='utf-8') as f:
        tsv_lines = [line.strip('\r\n').split('\t') for line in f]

    tsv_slice = tsv_lines[start_idx:end_idx]
    print(f"Comparing {len(part_list)} lines against {len(tsv_slice)} TSV lines (index {start_idx} to {end_idx})")
    assert len(part_list) == len(tsv_slice), f"Mismatch: {len(part_list)} vs {len(tsv_slice)}"

    errors = 0
    for i, (text, tsv) in enumerate(zip(part_list, tsv_slice)):
        line_num, line_id, jp, old_cn = tsv
        # Check speaker tag
        if jp.startswith('@') and not text.startswith('@'):
            print(f"Line {line_num} ({line_id}): Missing speaker! JP: {jp[:20]}, Text: {text[:20]}")
            errors += 1
        elif not jp.startswith('@') and text.startswith('@'):
            print(f"Line {line_num} ({line_id}): Unexpected speaker! JP: {jp[:20]}, Text: {text[:20]}")
            errors += 1
        # Check control tags
        for tag in ['$[', '$]', '$d', '[$b', '$]']:
            if tag in jp and tag not in text:
                print(f"Line {line_num} ({line_id}): Missing tag {tag}! JP: {jp}, Text: {text}")
                errors += 1

    if errors == 0:
        print(f"[PASS] All {len(part_list)} lines verified with 0 errors!")
    else:
        print(f"[FAIL] {errors} errors found!")

if __name__ == '__main__':
    from mak_006_part1 import mak_006_part1
    verify_file('scratch_mak_006.tsv', mak_006_part1, 0, 261)
