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
