# Combine all 3 parts of ama_003
from tmp.ama_003_p1 import part1_lines
from tmp.ama_003_p2 import part2_lines
from tmp.ama_003_p3 import part3_lines

ama_003_lines = part1_lines + part2_lines + part3_lines
assert len(ama_003_lines) == 716, f"Expected 716 lines, got {len(ama_003_lines)}"
