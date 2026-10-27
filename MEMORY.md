# MEMORY.md - Grisaia Localization Project Context

## Project Context
- **Title**: Frontwing Grisaia Series (灰色的果实 / 灰色的迷宫 / 灰色的乐园 全合集与外传提取文本)
- **Source Files**:
  - `ALL_TEXT.txt`: 110,622 lines of Japanese script text.
  - `ALL_TEXT_cn.txt`: 110,622 lines of Chinese translated text.
- **Corpus Breakdown**:
  - `_varstr`: lines 1 - 629 (chapter select, titles, menu strings)
  - `grisaia1` (灰色的果实): lines 630 - 58,280 (57,651 lines)
  - `grisaia2` (灰色的迷宫): lines 58,281 - 81,005 (22,725 lines)
  - `grisaia3` (灰色的乐园): lines 81,006 - 106,902 (16,947 lines)
  - `side` (外传/残光/有坂老师等): lines 106,903 - 110,622 (3,696 lines)
- **Line ID Format**: `<scene/category>#<index>\t<text>` (note: Angelic Howl fullscreen presentation lines lack tabs and are structurally identical in JA and CN).

## Key Systematic MT / AI Flaws Uncovered
1. **Pervasive False-Friend & Machine Translation Tells**:
   - `オヤジ` (中年大叔/老头) mistranslated as `欧巴桑` (老太婆/欧巴桑) (gender inversion; com02 L12627, L12672).
   - `しらたき` (魔芋丝/蒟蒻丝) mistranslated as `柴鱼` (com02 L12764).
   - `ハッピー・ジョブ` (自渎俚语) brutally translated as `大演欢乐.job` (com02 L12585).
   - `飯ごう` (户外便携军用饭盒) translated as `圆筒饭锅` (com02 L12782).
   - `口三味線を弾く` (推诿为难/压低对方预期) misread as `敲退堂鼓` (com02 L12707).
   - `女慣れしてる` (习惯与女生相处) misread as `很熟女` (com02 L12639).
   - `ユージ君` hallucinated as `优一君` / `优一` (15+ occurrences across com01 & com02; should be 雄二君/雄二).
   - `オマエ` directly phonetically transliterated as `欧马埃` (disastrous MT artifact).
   - `腹を探られない内に` mistranslated literally as `在肚子被抓住之前` (should be 趁底细未被摸透/探明虚实之前).
   - Raw English words unhandled in Chinese dialogue (e.g. `student life也包括这种烦恼对吧？`, `yay`).
   - Inverted subject/agency: `クラスメイトを殺傷しようとした事` mistranslated as `企图杀伤同班同学的我` (attributing attack to Yuuji instead of Yumiko).
   - `貴方` translated literally as `贵方` (business/legal phrasing) instead of `你` / `您` (87+ occurrences in corpus).
   - `八百屋` left raw/untranslated as `八百屋` instead of `菜店` / `果蔬铺` / `果蔬摊` (26+ occurrences in corpus).
   - `場数` -> `菜式数量` (wrong; should be 掌勺经验/阅历/经历过的大场面).
   - `気味が悪い` -> `怪气味` (wrong; should be 瘆人/让人心里发毛/令人毛骨悚然).
   - `身をやつす` -> `献身于` (wrong; should be 隐瞒身份屈居为/假托于学生身份).
   - `十徳ナイフ` -> `十德小刀` (wrong; should be 瑞士军刀/多功能军刀).
   - `蜂さん` -> `蜂先生` (wrong; should be 蜜蜂/小蜜蜂).
   - `通い妻` -> `通勤妻子` (wrong; should be 上门服侍的小娇妻/走婚妻子).
   - `オヤングの湯切り` -> `泡澡水的火候` (wrong; parody of Peyoung炒面, draining hot water from cup yakisoba).
   - `ノーサンキュー` -> `不用谢啦` (wrong; polarity reversal, should be 敬谢不敏/我不需要).
   - `とき卵` -> `荷包蛋` (wrong; should be 打散的蛋花/中式蛋花汤).
   - `チョロイン` -> `傲娇少女` (wrong; should be 好搞定女主/白给女主).
   - `詰めが甘い` -> `吃瘪太容易` (wrong; should be 关键时刻欠一把火候/收尾大意).
   - `犬死に` -> `犬一般死去` (wrong; should be 枉死/白白送命).
2. **Polarity Reversal**:
   - `～と違って`: Machine translation often attributes the positive quality to the comparison target instead of the subject (e.g. L1006 inverted Amane vs Yumiko/Michiru/Makina/Sachi comparisons).

## Completed Milestones & Current State
- `_varstr` (Lines 1 - 629): 71 systematic errors corrected via `scripts/patch_varstr.py` (Angelic Howl days 1-16 "天使之咆哮", "瑞士军刀", "步频号子", "白给女主的品格", etc.).
- `grisaia1/ama_001` (Lines 630 - 1163, 534 lines): 100% polished and humanized via `scripts/apply_ama_001.py`. Completely eliminates AI taste, restores character voices, military/slang humor, and comedic timing.
- `grisaia1/com01` (Lines 12337 - 12575, 239 lines): 100% polished and humanized via `scripts/patch_com01.py`. Eradicated "欧马埃", "优一君", "在肚子被抓住之前", raw English "student life", restored box cutter ratchet clicking details, Yuuji & Chizuru banter, and mutual surname agreement with Yumiko.
- `grisaia1/com02` (Lines 12576 - 12812, 237 lines): 100% polished and humanized via `scripts/patch_com02.py`. Eradicated "欧巴桑" (reversed from オヤジ), "柴鱼" (mistranslated from しらたき), "大演欢乐.job" (slang), "含铅量为零的汽油", "很熟女" (mistranslated from 女慣れ), restored military mess tin, Asako's master teachings, and Kazuki sister mentions.
- `grisaia1/com03` (Lines 12813 - 12941, 129 lines): 100% polished and humanized via `scripts/patch_com03.py`. Eradicated "铜锣烧" (grotesquely mistranslated from みたらしだんご "见死团子" pun), raw English "needless", fixed "优一君", restored pedometer pet tech nuances, Makina's cat-like behavior, and Yuuji's phantom vanishing act on Amane.
- Total indexed modifications: 1,137 entries documented in `grisaia_modification_index.md`.
- Alignment: Full 110,622-line structural verification (`python3 scripts/verify_alignment.py`) passes 100% with zero line drift, tab drift, or tag corruption.
- Git Remote: Tracked with `git@github.com:OthinusG/grisaia_zh_localization.git`.
- Project Plan & Roadmap: Formulated comprehensive 6-milestone project plan at `analysis/grisaia_localization_project_plan.md` covering all 110,622 lines (Fruit common route -> Heroines -> Labyrinth -> Eden -> Side stories).

