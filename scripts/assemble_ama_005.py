# -*- coding: utf-8 -*-
import importlib.util

spec1 = importlib.util.spec_from_file_location('p1', 'tmp/ama_005_p1.py')
p1 = importlib.util.module_from_spec(spec1)
spec1.loader.exec_module(p1)

spec2 = importlib.util.spec_from_file_location('p2', 'tmp/ama_005_p2.py')
p2 = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(p2)

spec3 = importlib.util.spec_from_file_location('p3', 'tmp/ama_005_p3.py')
p3 = importlib.util.module_from_spec(spec3)
spec3.loader.exec_module(p3)

print('p1:', len(p1.part1_lines))
print('p2:', len(p2.part2_lines))
print('p3:', len(p3.part3_lines))

all_lines = p1.part1_lines + p2.part2_lines + p3.part3_lines
assert len(all_lines) == 779, f'Expected 779 lines, got {len(all_lines)}'

with open('scripts/ama_005_all.py', 'w', encoding='utf-8') as f:
    f.write('# -*- coding: utf-8 -*-\n')
    f.write('ama_005_lines = [\n')
    for l in all_lines:
        f.write('    ' + repr(l) + ',\n')
    f.write(']\n')

print('Wrote scripts/ama_005_all.py successfully with 779 lines!')
