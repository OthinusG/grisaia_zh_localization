#!/usr/bin/env python3
"""
patch_com29.py - Apply humanized, high-quality localization polishing for grisaia1/com29
(Lines 18749 to 18832, 84 lines)

Key Highlights:
- Asako's foreign language survival philosophy: "When going to another country, learn 'Thank you' first, the rest is whatever. Even in America I survived on 'Thank you', 'Dog', and 'Pencil'!". Chickenhead slang caution.
- Broken English tutoring: Michiru almost failed English test; Makina (lived in US as kid) teaches her.
  - "Are you fish?" -> "Do I look like a fish?"
  - "Are you okay?" -> "Are you gay?" -> "Yes, I am gay." -> "Are you too?" -> "No! You wanna get beat up?!"
  - "I like fish!" -> "Are you a rabbit? Why are you laughing?"
- Tongue twisters & Compressed Memory:
  - Makina: "Michiru reads Chopin as Chopin (チョピン)! I pronounce Animal as Enimow (エニモー)! Obviously I am the teacher!"
  - Yuji tests Anomalocaris (アノマロカリス): Makina says "Aromanocaris" -> "Anoromacaris".
  - Amane tests Halogen bulb (ハロゲンバルブ): Makina says "Hageron bubble (ハゲロンバブル - 秃头泡沫)".
  - Sachi tests Man Gyong Bong (万景峰号): Makina breaks down.
- Broken English Part 2 (about Amane):
  - "Lover of lovers (恋人の中の恋人)" -> "Rubber lover (ゴムの恋人)?".
  - "Mother of mothers (母亲中的母亲)" -> "Is your mom a mummy (母ちゃんミイラ)?!".
- Conclusion: Yuji observes "Never learn English from a foreigner". Amane: "It'll work out on vibes." Lesson of the day: "English conversation is all about vibes (英会話はノリ)".
"""

import sys
import re

PATCH_DATA = {
    # 18749 - 18755: Asako's philosophy on language & Chickenhead caution
    18749: "——在动身前往语言不通的异国他乡之际，总有那么一句无论如何都必须最优先掌握的语言词汇。",
    18750: "而那句最为核心的话便是『谢谢』——这是我的师父亲手传授给我的处世真理。",
    18751: "事实上，对于行事粗枝大叶如我师父那般的豪放女性而言，她也确实打心底里只肯老老实实去死记这一句词汇罢了。",
    18752: "『总而言之先把“谢谢”给我记牢了，除此之外的全凭感觉瞎凑活就行。老娘当年哪怕在美国闯荡，光凭“Thank you”、“Dog”和“Pencil”这三个单词，不也一样平趟应付所有交谈嘛！』",
    18753: "——豪放洒脱到了这般登峰造极的地步，反倒让人打心底里觉得莫名神清气爽。",
    18754: "虽说这种单细胞思维堪比家养笨母鸡般的鸡脑子，但切记万万不可在女性面前轻佻地将『Chickenhead（鸡头/蠢货）』这类俚语随口挂在嘴边。",
    18755: "因为稍有不慎，便极容易顺着母鸡低头反复啄食饲料的滑稽姿态，被对方联想曲解为某种极其下流低俗的隐晦性暗示。",

    # 18756 - 18769: English tutoring broken dialogue
    18756: "@みちる@「（今天的晚饭是鱼。阁下是鱼吗？）」",
    18757: "@蒔菜@「（…哈？本小姐看起来长得很像一条鱼吗？）」",
    18758: "@みちる@「（是的，是鱼。阁下不要紧吗？）」",
    18759: "@蒔菜@「（…你说啥玩意儿？）」",
    18760: "@みちる@「（阁下不要紧吗？）」",
    18761: "@蒔菜@「（…你是基佬吗？）」",
    18762: "@みちる@「（是的，在下是一名纯正的基佬）」",
    18763: "@蒔菜@「（喔唷，真的假的啊，这未免也太劲爆炸裂了吧？）」",
    18764: "@みちる@「（阁下难道也是吗？）」",
    18765: "@蒔菜@「（鬼才跟你一样啦！信不信我直接一拳把你轰飞上天啊？）」",
    18766: "@みちる@「（哈？十分抱歉，还请麻烦您再重复说一遍）」",
    18767: "@蒔菜@「（你到底能不能听懂本小姐在讲些什么啊？饶了我吧真是的…）」",
    18768: "@みちる@「（在下非常喜欢吃鱼！在下深爱着它！）」",
    18769: "@蒔菜@「（你这家伙是兔子不成吗？话说你到底在那儿傻笑个什么劲儿啊）」",

    # 18770 - 18784: Yuji & Amane observe, Makina's Chopin vs Animal bragging
    18770: "@雄二@「我说，天音啊」",
    18771: "@天音@「嗯？怎么啦？」",
    18772: "@雄二@「前面那两个家伙从刚才开始到底在瞎折腾些什么名堂？」",
    18773: "@天音@「啊啊，那个呀？那是莳菜老师举办的课外特别辅导教学哦」",
    18774: "@雄二@「特别辅导教学？」",
    18775: "@天音@「你看嘛，美智留前阵子期中英语测试不是险些踩线挂科亮红灯嘛？所以就像现在这样，隔三差五便跑来让莳菜亲自给她开开小灶恶补一下咯」",
    18776: "@雄二@「让莳菜来辅导英语吗…」",
    18777: "@天音@「嘛，别看莳菜平时那副疯疯癫癫的模样，我之前应该也跟你提过吧？她小时候可是在美国实打实定居生活过好长一阵子的呢」",
    18778: "@雄二@「不知怎的…总觉得由莳菜这丫头一本正经地在讲台上给人授课传道，实在是一幅极其不可思议的超现实魔幻光景啊…」",
    18779: "@蒔菜@「你们这帮凡人休得在背后窃窃私语！不妨好好动动脑子想想看吧，诸君！」",
    18780: "@蒔菜@「听好了听仔细了！提起松岛美智留，那可是一个会把大名鼎鼎的『肖邦（Chopin）』拼音硬生生念成『乔平（Chopin）』的绝世文盲哦！而本小姐我，可是能够字正腔圆地把『动物（Animal）』发音成地道纯正『艾尼魔（Enimow）』的高贵英伦名媛啊！」",
    18781: "@蒔菜@「这两相权衡之下，无论放在谁的雪亮法眼里，本小姐理所当然都当仁不让属于居高临下的执教者一方！这难道不是不证自明、毋庸置疑的铁定真理吗！？」",
    18782: "@蒔菜@「不，毫无疑问绝对如此！这是何等精妙的反诘修辞！而且不知为何连我说话的语调都带上了一股天纵奇才般的学者风范！",
    18783: "简直臭屁自恋到了令人作呕的最高境界！」",
    18784: "@天音@「…哪有自己亲口这么吐槽自己的啊？话说既然你自己心里都门儿清的话就给我收敛节制一点啊…」",

    # 18785 - 18804: Tongue twisters: Anomalocaris, Halogen bulb, Man Gyong Bong
    18785: "@雄二@「哼…莳菜这家伙，明明连区区奇虾的名字都念不利索，居然还敢摆出一副不可一世的高傲架子…」",
    18786: "@天音@「奇虾那是啥玩意儿？」",
    18787: "@雄二@「寒武纪海洋中体型最庞大的霸主级食肉巨兽的名字。来，莳菜，念一遍给我听听看」",
    18788: "@蒔菜@「阿诺马诺虾力士！」",
    18789: "@雄二@「念错了，再来一遍」",
    18790: "@蒔菜@「阿诺罗玛虾力士！」",
    18791: "@雄二@「还是错的，是奇虾阿诺玛洛卡力斯，再念一次」",
    18792: "@蒔菜@「阿诺…玛诺…？」",
    18793: "@天音@「那来试试这个：卤素石英灯泡」",
    18794: "@蒔菜@「秃头罗曼大泡沫！」",
    18795: "@天音@「好嘞，彻底出局翻车！」",
    18796: "@蒔菜@「嗷呜痛痛痛痛！！」",
    18797: "@雄二@「…搞了半天，原来连卤素灯泡这种平平无奇的词汇都念不利索吗？」",
    18798: "@幸@「因为小莳的舌系带相对较短，加之脑内的神经回路构造略微有些与众不同，所以日常生活中确实存在着大量无法流畅精准咬字发音的生僻词汇呢」",
    18799: "@蒔菜@「才没有那回事好不好！？少在那儿瞧不起人了！？千万别把莳菜当成软柿子小瞧了啊！？」",
    18800: "@幸@「那么请跟我念——客货两用轮渡万景峰号」",
    18801: "@蒔菜@「…客、客货…万…喀！",
    18802: "　呜嗷嗷嗷——！！吵死人啦！别在旁边瞎捣乱碍手碍脚打断我的思路啊啊啊——！！」",
    18803: "@雄二@「别动不动就乱迁怒别人啊…」",
    18804: "这大概便是典型的『压缩记忆法』所遗留下来的认知缺陷后遗症吧。因为她习惯于只死记单词的首尾发音、并将中间的音节统统强行压缩打包塞进脑海，所以在面对极难通过语境自动补完生搬硬套的新潮词汇或专有名词时，往往便会暴露出极其致命的脆断短板。",

    # 18805 - 18820: English tutoring Part 2 (about Amane)
    18805: "@蒔菜@「奇露奇露——！英语口语实战演练继续！接着上课咯——！！」",
    18806: "@みちる@「吵死人啦，用不着扯开大嗓门我也能听见$[$b啦…$]」",
    18807: "@蒔菜@「很好！那么接下来以天音姐姐为描写对象的英文口语即兴造句！正式开练！」",
    18808: "@みちる@「（啊——…她的名字叫作天音）」",
    18809: "@蒔菜@「（这谁不知道啊，然后呢？）」",
    18810: "@みちる@「（她是一个极其魅力四射充满吸引力的女人）」",
    18811: "@蒔菜@「（确实呢）」",
    18812: "@みちる@「（若是能让她成为自己的恋人伴侣，必将收获无上的幸福）」",
    18813: "@蒔菜@「（那可就真不好说了吧？）」",
    18814: "@みちる@「（唯有她，才称得上是万千恋人当中当之无愧的极品恋人）」",
    18815: "@蒔菜@「（…橡胶材质充气娃娃般的塑料恋人？）」",
    18816: "@みちる@「（若是与她携手步入婚姻的殿堂，她必将蜕变成为天底下最伟大的母亲楷模）」",
    18817: "@蒔菜@「（喂！你老妈难道是一具风干风化的千年木乃伊不成吗！？）」",
    18818: "@みちる@「（是的！完全正确！）」",
    18819: "@蒔菜@「（真的假的啊，这可真是一个家庭成分炸裂的魔性家族呢…你日后的人生可千万要努力堂堂正正走在阳光大道上哦？）」",
    18820: "@雄二@「这完全行不通吧…从最根本的逻辑上来看，这俩人压根就连半点实质性的对话交流都没对齐啊…」",

    # 18821 - 18832: Asako's lesson reaffirmed, "English conversation is all about vibes"
    18821: "@雄二@「我说，天音啊」",
    18822: "@天音@「嗯？」",
    18823: "@雄二@「搞出这种前言不搭后语的荒诞过家家，真的能起到哪怕半点学习辅导的功效吗？」",
    18824: "@天音@「嗯～…天晓得呢？不过嘛，总比无所事事什么都不干强上那么一点点对吧？」",
    18825: "@雄二@「嘛，虽然话是这么说没错啦…」",
    18826: "双方对话内容风马牛不相及固然是一桩致命弊端，但莳菜口中所飙出的所谓英文，更是充斥着一堆错漏百出胡编乱造的离谱语法。",
    18827: "不仅各处发音怪诞滑稽到了极点，甚至还夹杂着大量连大洋彼岸的欧美本土居民都极少使用的冷门地下俚语黑话。这简直堪称是『千万别跟半吊子外国人学外语』的反面教材教科书式典型范例了。",
    18828: "@天音@「好啦好啦，反正最后总能车到山前必有路的啦，全凭感觉和气氛撑过去就行咯」",
    18829: "@雄二@「全凭感觉和气氛吗…」",
    18830: "确实，放眼茫茫世界之中，也真真切切存在着单凭一句『Dog』、一句『Pencil』外加一句『Thank you』便能四海为家应付一切日常交谈的豪杰之辈。",
    18831: "『英语口语，全凭感觉与气氛』——",
    18832: "而这，便是今日所收获的最深刻教训。",
}

def main():
    target_file = "ALL_TEXT_cn.txt"
    with open(target_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    start_line = 18749
    end_line = 18832
    expected_count = end_line - start_line + 1

    print(f"Total patch lines defined: {len(PATCH_DATA)}")
    assert len(PATCH_DATA) == expected_count, f"Expected {expected_count} patches, got {len(PATCH_DATA)}"

    with open("ALL_TEXT.txt", "r", encoding="utf-8") as f_ja:
        ja_lines = f_ja.readlines()

    speaker_pattern = re.compile(r"^@([^@]+)@")
    tag_pattern = re.compile(r"\$\[([^$]+)\$\]")

    mismatches = 0
    for line_num in range(start_line, end_line + 1):
        idx = line_num - 1
        ja_line = ja_lines[idx].strip()
        ja_parts = ja_line.split("\t", 1)
        ja_text = ja_parts[1] if len(ja_parts) > 1 else ""

        cn_patch_text = PATCH_DATA[line_num]
        ja_speakers = speaker_pattern.findall(ja_text)
        cn_speakers = speaker_pattern.findall(cn_patch_text)
        if ja_speakers != cn_speakers:
            print(f"[SPEAKER MISMATCH] line {line_num}: JA={ja_speakers} vs CN={cn_speakers}")
            print(f"  JA text: {ja_text}")
            print(f"  CN text: {cn_patch_text}")
            mismatches += 1

        ja_tags = tag_pattern.findall(ja_text)
        cn_tags = tag_pattern.findall(cn_patch_text)
        if len(ja_tags) != len(cn_tags):
            print(f"[TAG COUNT MISMATCH] line {line_num}: JA={ja_tags} vs CN={cn_tags}")
            print(f"  JA text: {ja_text}")
            print(f"  CN text: {cn_patch_text}")
            mismatches += 1

    print(f"Total mismatches: {mismatches}")
    if mismatches > 0:
        print("Please fix mismatches before applying!")
        sys.exit(1)

    for line_num, new_text in PATCH_DATA.items():
        idx = line_num - 1
        parts = lines[idx].split("\t", 1)
        lines[idx] = f"{parts[0]}\t{new_text}\n"

    with open(target_file, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"Successfully patched {len(PATCH_DATA)} lines in {target_file}!")

if __name__ == "__main__":
    main()
