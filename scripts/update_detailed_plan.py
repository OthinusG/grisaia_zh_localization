# -*- coding: utf-8 -*-
"""
Generate and update grisaia_localization_project_plan.md with 329 granular tasks (<1000 lines each).
"""
import os, sys
sys.path.insert(0, os.path.abspath('.'))
from scripts.build_full_granular_checklist import generate_tasklist

def build_markdown_checklist():
    tasks = generate_tasklist()

    m0 = []
    m1 = []
    m2_mak = []
    m2_ama = []
    m2_mic = []
    m2_sac = []
    m2_yum = []
    m2_op = []
    m3_yuj = []
    m3_ama = []
    m3_mak = []
    m3_mic = []
    m3_sac = []
    m3_yum = []
    m3_ss = []
    m4_bla = []
    m4_pro = []
    m5_zan = []
    m5_other = []

    for t in tasks:
        name = t['name']
        if name == '_varstr' or name == 'grisaia1/ama_001':
            m0.append(t)
        elif 'grisaia1/com' in name:
            m1.append(t)
        elif 'grisaia1/mak' in name:
            m2_mak.append(t)
        elif 'grisaia1/ama' in name:
            m2_ama.append(t)
        elif 'grisaia1/mic' in name:
            m2_mic.append(t)
        elif 'grisaia1/sac' in name:
            m2_sac.append(t)
        elif 'grisaia1/yum' in name:
            m2_yum.append(t)
        elif 'grisaia1/op' in name:
            m2_op.append(t)
        elif 'grisaia2/yuj' in name:
            m3_yuj.append(t)
        elif 'grisaia2/ama' in name:
            m3_ama.append(t)
        elif 'grisaia2/mak' in name:
            m3_mak.append(t)
        elif 'grisaia2/mic' in name:
            m3_mic.append(t)
        elif 'grisaia2/sac' in name:
            m3_sac.append(t)
        elif 'grisaia2/yum' in name:
            m3_yum.append(t)
        elif 'grisaia2' in name:
            m3_ss.append(t)
        elif 'grisaia3/bla' in name:
            m4_bla.append(t)
        elif 'grisaia3/PRO' in name:
            m4_pro.append(t)
        elif 'side/grizan' in name:
            m5_zan.append(t)
        else:
            m5_other.append(t)

    lines = []
    lines.append("## 七、 全工程详尽细粒度任务清单（Granular Task Checklist，单项均在 1000 行以内）\n")
    lines.append("> **执行铁律**：根据 `AGENTS.md` 规范，所有任务单元严格控制在 1000 行以内；每完成一个独立任务，必须主动在本文档中将 `[ ]` 标为 `[x]`，并与翻译文本、修改索引一同提交并推送至远端仓库（`git push origin main`）。\n")

    # M0
    lines.append(f"### 【里程碑 0】工程基建与标杆建立 (共 {len(m0)} 项，已完成 {len(m0)} 项) —— 【已完成】\n")
    for idx, t in enumerate(m0, 1):
        lines.append(f"- [x] **M0.{idx:02d}** `{t['name']}` (L{t['start']} - L{t['end']}, {t['lines']}行) —— {t['topic']}")
    lines.append("- [x] **M0.03** `scripts/verify_alignment.py` 自动化对齐门禁构建与全量 110,622 行验证")
    lines.append("- [x] **M0.4** `analysis/grisaia_glossary.json` 角色声线规范与专有名词表固化")
    lines.append("- [x] **M0.05** `scripts/generate_modification_index.py` 全文本修改对比索引自动化")
    lines.append("\n---\n")

    # M1
    lines.append(f"### 【里程碑 1】《灰色的果实》美滨学园共通线全 52 话 (共 {len(m1)} 项，已完成 {len(m1)} 项) —— 【全量圆满收官】\n")
    for idx, t in enumerate(m1, 1):
        lines.append(f"- [x] **M1.{idx:02d}** `{t['name']}` (L{t['start']} - L{t['end']}, {t['lines']}行) —— {t['topic']}")
    lines.append("\n---\n")

    # M2
    total_m2 = len(m2_mak) + len(m2_ama) + len(m2_mic) + len(m2_sac) + len(m2_yum) + len(m2_op)
    lines.append(f"### 【里程碑 2】《灰色的果实》各女主个人线 (共 {total_m2} 项，已完成 1 项)\n")

    lines.append(f"#### 阶段 2.1：入巢莳菜线 (`mak_001` ~ `mak_021`，共 {len(m2_mak)} 项，已完成 1 项)\n")
    for idx, t in enumerate(m2_mak, 1):
        chk = "x" if t['name'] == 'grisaia1/mak_001' else " "
        lines.append(f"- [{chk}] **M2.1.{idx:02d}** `{t['name']}` (L{t['start']} - L{t['end']}, {t['lines']}行) —— {t['topic']}")

    lines.append(f"\n#### 阶段 2.2：周防天音线与《天使之咆哮》 (`ama_002` ~ `ama_old_010`，共 {len(m2_ama)} 项)\n")
    for idx, t in enumerate(m2_ama, 1):
        lines.append(f"- [ ] **M2.2.{idx:02d}** `{t['name']}` (L{t['start']} - L{t['end']}, {t['lines']}行) —— {t['topic']}")

    lines.append(f"\n#### 阶段 2.3：松岛满线 (`mic_001` ~ `mic_021`，共 {len(m2_mic)} 项)\n")
    for idx, t in enumerate(m2_mic, 1):
        lines.append(f"- [ ] **M2.3.{idx:02d}** `{t['name']}` (L{t['start']} - L{t['end']}, {t['lines']}行) —— {t['topic']}")

    lines.append(f"\n#### 阶段 2.4：小岭幸线 (`sac_001` ~ `sac_013`，共 {len(m2_sac)} 项)\n")
    for idx, t in enumerate(m2_sac, 1):
        lines.append(f"- [ ] **M2.4.{idx:02d}** `{t['name']}` (L{t['start']} - L{t['end']}, {t['lines']}行) —— {t['topic']}")

    lines.append(f"\n#### 阶段 2.5：榊由美子线 (`yum_001` ~ `yum_009`，共 {len(m2_yum)} 项)\n")
    for idx, t in enumerate(m2_yum, 1):
        lines.append(f"- [ ] **M2.5.{idx:02d}** `{t['name']}` (L{t['start']} - L{t['end']}, {t['lines']}行) —— {t['topic']}")

    lines.append(f"\n#### 阶段 2.6：果实序章篇 (`op_001`，共 {len(m2_op)} 项)\n")
    for idx, t in enumerate(m2_op, 1):
        lines.append(f"- [ ] **M2.6.{idx:02d}** `{t['name']}` (L{t['start']} - L{t['end']}, {t['lines']}行) —— {t['topic']}")
    lines.append("\n---\n")

    # M3
    total_m3 = len(m3_yuj) + len(m3_ama) + len(m3_mak) + len(m3_mic) + len(m3_sac) + len(m3_yum) + len(m3_ss)
    lines.append(f"### 【里程碑 3】《灰色的迷宫》雄二过去篇与各女主后日谈 (共 {total_m3} 项)\n")

    lines.append(f"#### 阶段 3.1：雄二过去篇 / 随想录 Caprice (`yuj_001` ~ `yuj_015`，共 {len(m3_yuj)} 项)\n")
    for idx, t in enumerate(m3_yuj, 1):
        lines.append(f"- [ ] **M3.1.{idx:02d}** `{t['name']}` (L{t['start']} - L{t['end']}, {t['lines']}行) —— {t['topic']}")

    lines.append(f"\n#### 阶段 3.2：周防天音 After Story (`ama_001` ~ `ama_004` / `amaness*`，共 {len(m3_ama)} 项)\n")
    for idx, t in enumerate(m3_ama, 1):
        lines.append(f"- [ ] **M3.2.{idx:02d}** `{t['name']}` (L{t['start']} - L{t['end']}, {t['lines']}行) —— {t['topic']}")

    lines.append(f"\n#### 阶段 3.3：入巢莳菜 After Story (`mak_001` ~ `mak_004` / `makinass*`，共 {len(m3_mak)} 项)\n")
    for idx, t in enumerate(m3_mak, 1):
        lines.append(f"- [ ] **M3.3.{idx:02d}** `{t['name']}` (L{t['start']} - L{t['end']}, {t['lines']}行) —— {t['topic']}")

    lines.append(f"\n#### 阶段 3.4：松岛满 After Story (`mic_001` ~ `mic_004` / `michiruss*`，共 {len(m3_mic)} 项)\n")
    for idx, t in enumerate(m3_mic, 1):
        lines.append(f"- [ ] **M3.4.{idx:02d}** `{t['name']}` (L{t['start']} - L{t['end']}, {t['lines']}行) —— {t['topic']}")

    lines.append(f"\n#### 阶段 3.5：小岭幸 After Story (`sac_001` ~ `sac_005` / `sachiss*`，共 {len(m3_sac)} 项)\n")
    for idx, t in enumerate(m3_sac, 1):
        lines.append(f"- [ ] **M3.5.{idx:02d}** `{t['name']}` (L{t['start']} - L{t['end']}, {t['lines']}行) —— {t['topic']}")

    lines.append(f"\n#### 阶段 3.6：榊由美子 After Story (`yum_001` ~ `yum_004` / `yumikoss*`，共 {len(m3_yum)} 项)\n")
    for idx, t in enumerate(m3_yum, 1):
        lines.append(f"- [ ] **M3.6.{idx:02d}** `{t['name']}` (L{t['start']} - L{t['end']}, {t['lines']}行) —— {t['topic']}")

    lines.append(f"\n#### 阶段 3.7：美滨日常短篇集与杂项篇 (`ss*` / `etcess*`，共 {len(m3_ss)} 项)\n")
    for idx, t in enumerate(m3_ss, 1):
        lines.append(f"- [ ] **M3.7.{idx:02d}** `{t['name']}` (L{t['start']} - L{t['end']}, {t['lines']}行) —— {t['topic']}")
    lines.append("\n---\n")

    # M4
    total_m4 = len(m4_bla) + len(m4_pro)
    lines.append(f"### 【里程碑 4】《灰色的乐园》白翼之茧与决战篇 (共 {total_m4} 项)\n")

    lines.append(f"#### 阶段 4.1：白翼之茧篇 (`bla_001` ~ `bla_014`，共 {len(m4_bla)} 项)\n")
    for idx, t in enumerate(m4_bla, 1):
        lines.append(f"- [ ] **M4.1.{idx:02d}** `{t['name']}` (L{t['start']} - L{t['end']}, {t['lines']}行) —— {t['topic']}")

    lines.append(f"\n#### 阶段 4.2：世界树之种 / 终章 (`PRO_001` ~ `PRO_005`，共 {len(m4_pro)} 项)\n")
    for idx, t in enumerate(m4_pro, 1):
        lines.append(f"- [ ] **M4.2.{idx:02d}** `{t['name']}` (L{t['start']} - L{t['end']}, {t['lines']}行) —— {t['topic']}")
    lines.append("\n---\n")

    # M5
    total_m5 = len(m5_zan) + len(m5_other)
    lines.append(f"### 【里程碑 5】《灰色外传集》与全量验收封包 (共 {total_m5} 项)\n")

    lines.append(f"#### 阶段 5.1：残光篇 (`grizan_001` ~ `grizan_007`，共 {len(m5_zan)} 项)\n")
    for idx, t in enumerate(m5_zan, 1):
        lines.append(f"- [ ] **M5.1.{idx:02d}** `{t['name']}` (L{t['start']} - L{t['end']}, {t['lines']}行) —— {t['topic']}")

    lines.append(f"\n#### 阶段 5.2：旋律篇与有坂秋樱花短篇 (`gri_ano03_*` / `griani_*` / `aft_*`，共 {len(m5_other)} 项)\n")
    for idx, t in enumerate(m5_other, 1):
        lines.append(f"- [ ] **M5.2.{idx:02d}** `{t['name']}` (L{t['start']} - L{t['end']}, {t['lines']}行) —— {t['topic']}")

    lines.append("\n#### 阶段 5.3：全量 110,622 行终验与 Release 封包")
    lines.append("- [ ] **M5.3.01** 全量 110,622 行再次运行 `verify_alignment.py` 结构一致性终检")
    lines.append("- [ ] **M5.3.02** 运行 `scan_issues.py` 确认特征告警全量清零")
    lines.append("- [ ] **M5.3.03** 输出全剧本终验 Release 构建物与成果报告")

    return "\n".join(lines)

def update_plan_file():
    with open('grisaia_localization_project_plan.md', 'r', encoding='utf-8') as f:
        content = f.read()

    pos = content.find("## 七、")
    if pos != -1:
        base_content = content[:pos]
    else:
        base_content = content

    checklist_md = build_markdown_checklist()
    new_plan = base_content.rstrip() + "\n\n" + checklist_md + "\n"

    with open('grisaia_localization_project_plan.md', 'w', encoding='utf-8') as f:
        f.write(new_plan)
    with open('analysis/grisaia_localization_project_plan.md', 'w', encoding='utf-8') as f:
        f.write(new_plan)

    artifact_dir = "/Users/wqin/.gemini/antigravity-cli/brain/58bc9ea3-8e40-4e4b-af2d-7c0dbd91401e"
    os.makedirs(artifact_dir, exist_ok=True)
    art_path = os.path.join(artifact_dir, "grisaia_localization_project_plan.md")
    with open(art_path, 'w', encoding='utf-8') as f:
        f.write(new_plan)

    print(f"Plan updated successfully! Total length: {len(new_plan)} chars.")

if __name__ == '__main__':
    update_plan_file()
