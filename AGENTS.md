# AGENTS.md - Grisaia Localization Project Guidelines

## Project Overview
This workspace contains extracted script text (`ALL_TEXT.txt`) and corresponding Chinese translated text (`ALL_TEXT_cn.txt`) for the Frontwing *Grisaia* (灰色系列) series (comprising *The Fruit of Grisaia* / 灰色的果实, *The Labyrinth of Grisaia* / 灰色的迷宫, *The Eden of Grisaia* / 灰色的乐园, side stories, etc.).

## Task & Objectives
1. Perform high-quality proofreading, correction, and polishing of `ALL_TEXT_cn.txt` against Japanese source `ALL_TEXT.txt`.
2. Strictly maintain character voices, franchise-specific terminology, recurring jokes/memes (neta), and military/slang nuances.
3. Eliminate machine translation / AI artifacts (AI味, mistranslations like "気味の悪い" -> "怪气味", "場数" -> "菜式数量", inverted polarity like "～と違って", etc.).
4. Strictly preserve line IDs, control tokens, speaker markers (`@Name@`), tags, and formatting so the output remains 100% structurally aligned.

## Technical Rules & Conventions
- Formats: Tab-delimited `_varstr#...` or `<scene_id>#...` followed by text.
- Line Count & Structural Invariance: Total lines (110,622) and line-by-line IDs must strictly match.
- Code & Python Scripts: Standard library Python preferred for deterministic checking, diffing, and control token verification.

## Task Checklist & Granular Execution Protocol (细粒度任务拆解与实时打钩推送规则)
1. **详尽任务清单 (Fine-Grained Task List)**：工程计划书（`grisaia_localization_project_plan.md`）必须维护全景详尽的任务清单，细化到每一个具体章节（乃至长章节的分段子任务）。
2. **主动打钩 (Autonomous Checkoff)**：每当完成一个细小任务（如单个章节的代码润色、补丁生成、全局对齐验证及索引更新），Agent 必须主动在计划书中将对应的任务项由 `[ ]` 标记为 `[x]`。
3. **完成即推 (Check-and-Push Invariance)**：打钩行为必须与翻译文本（`ALL_TEXT_cn.txt`）、修改索引（`grisaia_modification_index.md`）一并进行 Git 提交，并立即推送到远端仓库（`git commit && git push origin main`）。严禁积压大量任务后才批量打钩和推送，必须确保远端仓库随时体现最新、最精准的任务完成状态。
4. **阶段停止门禁 (Milestone Gate)**：若用户给出阶段性目标（如“做完milestone1就停下”），在完成该里程碑的所有子任务、打钩并推送到远程后，Agent 必须停下等待用户进一步指示，严禁擅自跨里程碑推进。
