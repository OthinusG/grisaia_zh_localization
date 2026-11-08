# -*- coding: utf-8 -*-
import importlib.util

spec = importlib.util.spec_from_file_location("build_sac_006", "tmp/build_sac_006.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

with open("ALL_TEXT_cn.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

for lno in range(46501, 46713):
    raw = lines[lno - 1].rstrip("\r\n")
    if "\t" in raw:
        sid, _ = raw.split("\t", 1)
        lines[lno - 1] = f"{sid}\t{mod.lines[lno]}\n"
    else:
        lines[lno - 1] = f"{mod.lines[lno]}\n"

with open("ALL_TEXT_cn.txt", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("Applied patch_sac_006 to ALL_TEXT_cn.txt successfully.")
