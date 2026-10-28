import sys, os
sys.path.insert(0, os.path.abspath('.'))
from scripts.mak_001_part1 import lines_part1
from scripts.mak_001_part2 import lines_part2
from scripts.mak_001_part3 import lines_part3

all_lines = lines_part1 + lines_part2 + lines_part3
print(f"Total parts length: {len(lines_part1)} + {len(lines_part2)} + {len(lines_part3)} = {len(all_lines)}")

with open('scratch_mak_001.tsv', 'r', encoding='utf-8') as f:
    tsv_data = [line.strip().split('\t') for line in f if line.strip()]

print(f"Total TSV rows: {len(tsv_data)}")
assert len(all_lines) == len(tsv_data), f"Length mismatch: {len(all_lines)} vs {len(tsv_data)}"

speaker_map = {
    '雄二': '雄二',
    '蒔菜': '莳菜',
    '天音': '天音',
    '由美子': '由美子',
    '幸': '幸',
    'みちる': '满',
    'ＪＢ': 'JB',
    '学園長': '学园长',
    '生徒達': '学生们',
}

tag_found = 0
speaker_errors = 0

for idx, (trans, row) in enumerate(zip(all_lines, tsv_data)):
    id_ = row[1]
    ja = row[2]
    if ja.startswith('@') and '@' in ja[1:]:
        speaker = ja.split('@')[1]
        exp_speaker = speaker_map.get(speaker, speaker)
        if not trans.startswith(f"@{exp_speaker}@"):
            print(f"Speaker error at row {idx} ({id_}): JA='{ja}' vs Trans='{trans}'")
            speaker_errors += 1
    elif trans.startswith('@'):
        print(f"Unexpected speaker in trans at row {idx} ({id_}): JA='{ja}' vs Trans='{trans}'")
        speaker_errors += 1

    if '$[' in ja:
        print(f"Tag in JA at row {idx} ({id_}): JA='{ja}' | Trans='{trans}'")
        tag_found += 1
        assert '$[' in trans, f"Missing tag in trans at {idx}"

print(f"Speaker errors: {speaker_errors}")
print(f"Tags found and matched: {tag_found}")
if speaker_errors == 0:
    print("[PASS] mak_001 is completely valid!")
