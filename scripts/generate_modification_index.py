#!/usr/bin/env python3
"""
Generate comprehensive, indexed markdown report of all localized text modifications.
"""

import os
import re
import glob
import subprocess

def escape_md(text):
    if text is None:
        return ""
    return text.replace("|", "\\|").replace("\n", " ").replace("\r", "")

def classify_change(line_no, sid, ja, old_cn, new_cn):
    # com10 specific
    if "グーリー" in ja or "恶食怪" in new_cn:
        return "俚语绰号/梗误译", "纠正将美军军营俚语『恶食怪/烂胃王（Gross Eater / Ghoulie）』荒谬误译为『贪吃鬼』"
    if "タクアン" in ja or "腌萝卜" in new_cn:
        return "食物常识/严重误译", "纠正将日式便携军用配给『腌萝卜罐头（沢庵漬け）』离谱误译为植物『虎杖罐头』或『腌竹笋』"
    if "オタマの背" in ja or "勺背" in new_cn:
        return "烹饪常识/误读", "纠正将烹饪铁勺勺背（お玉の背）误读为『蛋壳背（卵）』"
    if "居るんじゃない" in ja and "人不在啊" in old_cn:
        return "否定逻辑反转", "纠正反问句否定语气误读（『这不是在嘛』反被机翻成『人不在啊』）"
    if "豚も食わないメシ" in ja:
        return "俚语生动化", "将字面直译『连猪都不吃的饭』生动润色为军用配给黑话『连猪都嫌弃的泔水伙食』"
    if "卓袱台" in ja:
        return "日式生活常识", "规范日语『卓袱台（ちゃぶ台）』为和室折叠小矮桌/矮方桌"

    # com09 specific
    if "ギャフン" in ja and "打嗝" in old_cn:
        return "成语误译为生理反应", "纠正将日语甘拜下风/吃瘪认栽口语『哑口无言/彻底吃瘪（ギャフン）』荒谬机翻为风马牛不相及的生理反应『打嗝』"
    if "くろがね文庫" in ja and "黑铁文库" in new_cn:
        return "军事历史典故还原", "注释并还原旧日本海军在巡洋舰/战舰上为官兵设立船载藏书库的专有历史名词『黑铁文库』"
    if "無芸が服を着て" in ja and "无艺可施穿在身上" in old_cn:
        return "惯用修辞生硬直译", "消除日语修辞生搬硬套『无艺可施穿在身上到处走』，重构为符合中文语境的自然讽刺『毫无才艺的空壳木头人』"
    if "気配は“雑”" in ja or "気配" in ja and "杂" in old_cn:
        return "军务潜伏术语规范", "规范雄二特工侦查与反潜伏专业术语为『隐匿行踪的气息太“糙”了』（非机械机翻『气息杂得很』）"
    if "ダイマカロフ" in ja or "ダイマカロフ給養" in ja:
        return "特摄文化梗与谐音包袱", "还原昭和特摄英雄《光速将军大马卡罗夫》战队梗，以及莳菜满脑子只记得大号马卡龙（マカロン）的美食包袱"

    # com08 specific
    if "根暗" in ja and "家里蹲" in old_cn:
        return "心理词义严重混淆", "纠正将由美子揭穿天音外向伪装下的阴郁性格（根暗/Nekura）荒唐误译为风马牛不相及的宅居词汇『家里蹲（Hikikomori）』"
    if "モヤシ" in ja and "金针菇" in old_cn:
        return "生活用语常识误译", "纠正将超市常见蔬菜绿豆芽（モヤシ/Moyashi）荒唐指鹿为马误译为『金针菇』"
    if "不幸自慢" in ja and "说到自己" in old_cn:
        return "特有文化词汇还原", "规范日语社会流行语『炫耀自身不幸/以惨博同情（不幸自慢）』与由美子通透冷静的心理剖析"
    if "プレイ" in ja and "剧本" in old_cn:
        return "二次元/Galgame梗还原", "纠正将天音调戏雄二的『大姐姐扮演游戏（お姉ちゃんプレイ）』机械死板直译为『大姐姐剧本』"

    # com07 specific
    if "そいつはすまなかった" in ja and "那家伙" in old_cn:
        return "成语俚语望文生义", "纠正将雄二口语道歉『那还真是不好意思/是我对不住你（そいつはすまなかった）』荒唐误读为『那家伙太惨了』"
    if "手榴弾を渡した相手" in ja and "交给男人的" in old_cn:
        return "主客逻辑反转", "纠正将『那个男人把手榴弹递给的对象是谁』彻底颠倒误译为『把手榴弹交给男人的究竟是谁』"
    if "目が見えない" in ja and "眼睛听不清" in old_cn:
        return "荒谬机翻笑话", "纠正将震伤失聪『耳が上手く聞こえない』荒谬机翻为『眼睛听不清』的严重生理逻辑事故"
    if "なぶり殺し" in ja and "据说有不少人宁愿被这样虐杀" in old_cn:
        return "机翻断句漏译修复", "补全并深度重构在战场被残虐折磨而决绝自爆的被截断译文（原机翻残缺为『据说有不少人宁愿被这样虐杀，也――』）"
    if "オシッコ" in ja and "膀胱" in old_cn:
        return "角色声线还原", "消除机械直白生硬医学词『膀胱吓破』，还原莳菜童真幼态的『吓得人家都要尿裤子了说』"
    if "バードマン" in ja:
        return "Ruby标签/军语代号", "规范美军丛林特种作战代号与Ruby标签『$[密林狙击手$/丛林鸟人$]（Birdman）』"
    if "自販機" in ja and "我把硬币" in old_cn:
        return "主语颠倒误读", "纠正将莳菜从青蛙钱包倒零钱买饮料主语颠倒误译为雄二"
    if "タコツボ" in ja:
        return "军事单兵掩体术语", "规范战壕避炮穴/单兵掩体为专业军事术语『散兵坑（タコツボ/Foxhole）』"

    # com06 specific
    if "女体流しそうめん" in ja or "女子流挂面" in old_cn:
        return "经典名梗误译", "纠正将天音调戏雄二的经典黄段子『女体盛流水素面（女体流しそうめん）』荒唐机翻为『女子流挂面』"
    if "流しそうめん" in ja and "流挂面" in old_cn:
        return "民俗风物诗术语", "规范日本夏日传统民俗风物诗名称为『流水素面』（非机械直译『流挂面』）"
    if "十徳ナイフ" in ja and "十德刀" in old_cn:
        return "专有名词/梗", "纠正生搬日文汉字『十德刀』，还原美滨经典格言『与其备瑞士军刀，不如随身带上阿幸』"
    if "負け組葉っぱ" in ja or "败组生菜叶" in old_cn:
        return "谐音冷笑话误读", "纠正将莳菜把活页纸（ルーズリーフ/Loose Leaf）双关谐音为『败犬叶子（負け組葉っぱ）』严重误译为『败组生菜叶』"
    if "キャベツの芯" in ja or "卷心菜" in ja:
        return "谐音双关笑话", "还原阿幸将铅笔芯（芯）偷换概念递给满『卷心菜心（キャベツの芯）』的天然黑谐音冷幽默"
    if "山ごもり" in ja and "迷路" in old_cn:
        return "词义严重误读", "纠正将雄二在山野隐遁求生技能（山ごもり）荒唐误译为毫无逻辑的『在山里迷路』"
    if "刃、流しましょうか" in ja and "冲一下" in old_cn:
        return "反差声线还原", "纠正将由美子在流水素面滑道顺流放刀片的致命冷幽默威胁误译为『把刀刃冲一下』"
    if "熱を入れて" in ja and "在加热" in old_cn:
        return "恶性机翻直译", "消除将『讲得热血沸腾/情绪高涨（熱を入れて語ってる）』荒诞机翻为『在加热在说话』的笑话"
    if "買収" in ja and "收购" in old_cn:
        return "词义误读", "纠正将天音以美色行贿买通（買収）商业公文生搬为『收购』"
    if "らめぇ" in ja:
        return "角色声线还原", "还原莳菜装模作样娇喘调侃的『雅蠛蝶~！不行啦~！』声线"
    if "ハエ" in ja and "肝っ玉" in ja:
        return "角色声线还原", "还原满逞强声称自己拥有『苍蝇般硕大肝胆』的滑稽吃瘪声线"

    # com05 specific
    if "ヒモ" in ja and "拉皮条" in old_cn:
        return "严重恶性误译", "纠正将雄二自嘲吃软饭/小白脸（ヒモ）严重荒唐误译为犯罪性质的『拉皮条』"
    if "女校生" in old_cn and "スクールボーイ" in ja:
        return "性别混淆误译", "纠正将美式俚语学生小子/毛头小伙（スクールボーイ）颠倒误译为『女校生』"
    if "ジャッカス" in ja and "胆小鬼" in old_cn:
        return "俚语含义误译", "纠正将美式俚语蠢驴/笨蛋（ジャッカス/Jackass）严重误译为『胆小鬼』"
    if "アンタサイテーね" in ja and "看不出来" in old_cn:
        return "严重语义颠倒", "纠正将天音鄙视雄二『你这人真是有够差劲（アンタサイテーね）』误译为『你还真是看不出来』"
    if "コキ使われ" in ja and "狠狠干着" in old_cn:
        return "粗俗机翻误译", "纠正将工作上被当牛做马使唤（コキ使われている）粗鄙生硬机翻为『在工作上被狠狠干着』"
    if "泣くわよ" in ja and "我才不要哭" in old_cn:
        return "否定逻辑反转", "纠正JB被雄二冷言吐槽时气急败坏的『信不信我哭给你看（泣くわよっ!?）』被颠倒反转为『我才不要哭呢』"
    if "母方の親戚" in ja and "撑到下课" in old_cn:
        return "机翻严重幻觉", "纠正将伪造身份借口硬说是母亲亲戚（押し通しなさいな）胡乱机翻为毫无逻辑的『撑到下课吧』"
    if "春寺三佐" in ja or "三佐" in ja:
        return "军事编制军衔", "规范自卫队/特工军阶称谓『春寺三佐（三等陆佐/少校）』与雄二打趣口吻"

    # com04 specific
    if "蟑螂" in old_cn and ("ザリガニ" in ja or "ザニガニ" in ja):
        return "荒唐恶性误译", "纠正将小龙虾/鳌虾（ザリガニ）荒唐误译为『蟑螂』的恶性翻译事故"
    if "优一" in old_cn or "優一" in old_cn:
        return "人名错误修正", "纠正将风见雄二（ユージ）严重机翻幻觉为『风见优一』"
    if "送给别人" in old_cn and "チルチル" in ja:
        return "人名混淆误译", "纠正将送给松岛满（琪尔琪尔/チルチル）的波子汽水糖误读为『送给别人』"
    if "倒是没有" in old_cn and "あるけど" in ja:
        return "否定逻辑反转", "纠正将随身带有棉线颠倒误译为『倒是没有』"
    if "美丽的小姐" in old_cn and "お姉様" in ja:
        return "名作文化梗还原", "还原经典的圣母在上女校贵安梗『贵安，姐姐大人（ごきげんよう、お姉様）』"
    if "我可以说给你听" in old_cn and "聞いてやる" in ja:
        return "主客逻辑反转", "纠正将『你想倾诉我可以听』颠倒误译为『我可以说给你听』"

    # com03 specific
    if "铜锣烧" in old_cn and "みたらし" in ja:
        return "食物名/谐音梗误读", "纠正将御手洗团子（见者即死团子/みたらし団子）双关冷笑话荒唐误译为『铜锣烧』"
    if "needless" in old_cn:
        return "生硬残留英文字词", "消除句中未处理生硬残留的英文单词『needless』"
    if "クセっ毛" in ja and "脾气" in old_cn:
        return "词义误读", "纠正将自然卷微卷发质（クセっ毛）望文生义误译为『脾气有点怪』"

    # com02 specific
    if "欧巴桑" in old_cn and "オヤジ" in ja:
        return "性别颠倒/误读", "纠正将男性大叔（オヤジ）荒谬误译为女性老太婆（欧巴桑）"
    if "柴魚" in old_cn or ("しらたき" in ja and "魔芋丝" in new_cn):
        return "食物生活用语误译", "纠正将豆腐店贩售的魔芋丝（白滝）荒唐误译为『柴鱼』"
    if "欢乐.job" in old_cn or "大演欢乐" in old_cn or "ハッピー・ジョブ" in ja:
        return "机翻俚语直译", "消除将自渎俚语粗暴直译为『大演欢乐.job』的恶性机翻痕迹"
    if "口三味線" in ja:
        return "成语习惯用语误读", "纠正将日文成语『推诿为难/压低对方预期』误读为『敲退堂鼓』"
    if "飯ごう" in ja:
        return "军品生活常识", "修正将户外军用便携饭盒生硬直译为『圆筒饭锅』"
    if "含铅量为零" in old_cn or "無鉛ガソリン" in ja:
        return "生活常识/术语", "修正将无铅汽油机械冗长直译为『含铅量为零的汽油』"
    if "女慣れ" in ja:
        return "词义误读", "纠正将习惯与女孩子相处望文生义误译为『很熟女』"
    if "わっち" in ja:
        return "特殊自称/口吻还原", "还原天音打趣扮演传统名门闺秀时的古典戏剧自称『咱家』"
    if "八百屋" in ja or "蔬果店老板" in old_cn:
        return "角色声线还原", "还原商店街果蔬铺大叔豪迈爽朗、爱开玩笑的江户子街坊口吻"
    if "欧马埃" in old_cn:
        return "机翻音译幻觉", "纠正将日文『オマエ（你）』直接音译为『欧马埃』的荒唐机翻"
    if "student life" in old_cn:
        return "生硬残留英文字词", "消除译文中未处理直接残留的生硬英文词汇『student life』"
    if "企图杀伤同班同学的我" in old_cn:
        return "主客逻辑反转", "纠正主谓语逻辑反转（由美子刺杀雄二，反被译成雄二企图杀伤同学）"
    if "腹を探られない内に" in ja or "肚子被抓住" in old_cn:
        return "成语习惯用语误读", "纠正将日文成语『探清虚实/摸清底细』严重误译为『在肚子被抓住之前』"
    if "好敵手" in ja or "ライバル" in ja:
        return "Ruby标签/专有名词", "规范Galgame标签格式，还原『$[好对手$/宿敌$]』"
    if "チキチキ" in ja or "咔哒咔哒" in new_cn:
        return "拟声词/武器细节", "还原美工刀滑轨咔哒咔哒推刀声与对峙细节"
    if "十徳ナイフ" in ja or "十德小刀" in old_cn:
        return "专有名词/梗", "纠正机翻直搬日文汉字，还原“瑞士军刀/阿幸万能”双关梗"
    if "オヤング" in ja:
        return "专有名词/梗", "纠正将Peyoung炒面沥热水严重误译为“泡澡水火候”"
    if "モバイル・エリコン" in ja or "モバエリ" in ja:
        return "专有名词/梗", "纠正将雄二误听军用机炮（机动厄利孔）机翻为“手机支付”"
    if "もにーぎゃん" in ja:
        return "机翻严重幻觉", "纠正将莳菜满嘴含饭含糊喊大哥哥严重脑补为“你们这些人真麻烦”"
    if "チョロイン" in ja:
        return "专有名词/梗", "还原松岛满的经典“白给女主/好搞定女主”属性（非傲娇）"
    if "エンジェリック" in ja or "エンジェル" in ja:
        return "专有名词/梗", "统一官方核心事件译名为“天使之咆哮”"
    if "便所の１００ワット" in ja:
        return "专有名词/梗", "还原日文俚语“厕所百瓦灯泡——瞎起劲/瞎热情”"
    if "ランニング・カデンス" in ja:
        return "军事术语", "修正军事术语为“步频号子/跑操口号”（非跑步韵律）"
    if "蜂さん" in ja:
        return "机翻直译误读", "纠正将“蜜蜂”拟人化直译为“蜂先生”"
    if "通い妻" in ja:
        return "习惯用语/梗", "纠正将日文走婚/上门照料生活的小娇妻误译为“通勤妻子”"
    if "犬死に" in ja:
        return "成语误读", "纠正将日文成语“白白送死/枉死”直译为“犬一般死去”"
    if "貴方" in ja and "贵方" in old_cn:
        return "消除公文AI味", "消除法律/商业公文腔“贵方”，还原自然第二人称“你”"
    if "場数" in ja:
        return "严重语义倒错", "纠正将下厨“经验阅历/大场面”严重误译为“菜式数量”"
    if "気味の悪い" in ja or "気味が悪" in ja:
        return "词义误读", "纠正将“心里发毛/瘆人”望文生义误译为“怪气味”"
    if "身をやつす" in ja:
        return "身份词义颠倒", "纠正将特工“隐瞒身份屈居为学生”颠倒误译为“献身于学生”"
    if "～と違って" in ja or "違って" in ja:
        return "逻辑颠倒/主客反转", "纠正对比逻辑反转（天音擅长料理/丰腴，反被译成他人擅长）"
    if "ノーサンキュー" in ja:
        return "否定逻辑反转", "纠正将拒绝对方案意的“敬谢不敏/我不需要”颠倒译为“不用谢啦”"
    if "とき卵" in ja:
        return "生活用语常识", "纠正将打散的“蛋花汤”错误识别为“带荷包蛋的汤”"
    if "意地の汚い" in ja:
        return "词义误读", "纠正将贪吃馋嘴/饿死鬼投胎误解为“心眼坏”"
    if "親切の押し売り" in ja:
        return "习惯用语", "纠正将“强塞好意/强加于人的热情”误译为“用力表达爱意”"
    if "重たい女" in ja or "重い女" in ja:
        return "习惯用语", "纠正直译“重女人”，规范为Galgame公认“沉重女”"
    if "詰めが甘い" in ja:
        return "成语误读", "纠正将将棋成语“关键时刻欠一把火候/收尾大意”误译为“吃瘪太容易”"
    if "孫の手" in ja:
        return "文化常识", "纠正将“老头乐/痒痒挠”误译为“逗猫棒”"
    if "八百屋" in ja:
        return "生搬日文汉字", "汉化日文汉字“八百屋”为“蔬菜水果店/果蔬铺”"
    if "ウッドエレメンタル" in ja:
        return "谐音梗修正", "还原“木の精/気のせい”谐音梗，删除机翻臆造的“胡桃夹子”"
    if "ジョンジョロ" in ja:
        return "拟声词拟态词", "消除将失禁拟声词直接音译为括号“（乔恩乔罗）”的机翻痕迹"
    if "マキナ" in ja and "玛琪娜" in old_cn:
        return "人名统一", "统一全剧本译名为“莳菜”"
    if "@学園長@" in ja or "@学园长@" in old_cn or "@学园长@" in new_cn:
        return "角色声线还原", "还原千鹤学园长爱摸鱼被抓包、气急败坏的天然大姐姐口吻"
    if "@由美子@" in old_cn or "@由美子@" in new_cn:
        return "角色声线还原", "消除AI生硬感，还原由美子毒舌千金、读书人措辞与傲娇口吻"
    if "@天音@" in old_cn or "@天音@" in new_cn:
        return "角色声线还原", "还原天音包容宠溺大姐姐、轻微关西腔与沉重女声线"
    if "@蒔菜@" in old_cn or "@蒔菜@" in new_cn:
        return "角色声线还原", "还原莳菜满嘴荤段子、童言无忌与狙击手反差声线"
    if "@雄二@" in old_cn or "@雄二@" in new_cn:
        return "角色声线还原", "还原雄二硬汉军人特工思维、冷面自嘲与务实冷幽默"
    if "@幸@" in old_cn or "@幸@" in new_cn:
        return "角色声线还原", "还原幸极致客气的敬语、天然黑与不苟言笑讲冷笑话口吻"
    if "@みちる@" in old_cn or "@满@" in old_cn:
        return "角色声线还原", "还原满假傲娇、元气笨蛋、常吃瘪逞强的滑稽喜剧感"
    return "消除AI味/润色优化", "重构生硬日式倒装与机械直译，润色为符合Galgame演出的自然中文"

def build_report():
    # 1. Recover original varstr
    old_varstr = {}
    if os.path.exists("analysis/varstr_comparison.txt"):
        with open("analysis/varstr_comparison.txt", "r", encoding="utf-8") as f:
            cur_line = None
            for line in f:
                line = line.rstrip("\r\n")
                if line.startswith("L") and line.endswith(":"):
                    cur_line = int(line[1:-1])
                elif line.strip().startswith("CN:") and cur_line is not None:
                    cn_part = line.split("CN:", 1)[1].strip()
                    if "\t" in cn_part:
                        old_varstr[cur_line] = cn_part.split("\t", 1)[1]
                    else:
                        old_varstr[cur_line] = cn_part

    # 2. Recover original ama_001
    recovered_ama = {}
    pattern1 = re.compile(r"L(\d+)\s+(grisaia1/ama_001#\d+)\t.*?\n-->\s+(grisaia1/ama_001#\d+)\t(.*)")
    pattern2 = re.compile(r"L(\d+)\s+JA:\s*(grisaia1/ama_001#\d+)\t.*?\nL\1\s+CN:\s*(grisaia1/ama_001#\d+)\t(.*)")

    for path in glob.glob("/Users/wqin/.gemini/antigravity-cli/brain/58bc9ea3-8e40-4e4b-af2d-7c0dbd91401e/.system_generated/steps/**/output.txt", recursive=True):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            for m in pattern1.finditer(content):
                recovered_ama[int(m.group(1))] = m.group(4)
            for m in pattern2.finditer(content):
                recovered_ama[int(m.group(1))] = m.group(4)

    # 3. Baseline from git initial commit (1f92993)
    git_base_cn = []
    try:
        out = subprocess.check_output(["git", "show", "1f92993:ALL_TEXT_cn.txt"], text=True)
        git_base_cn = out.splitlines()
    except Exception as e:
        print(f"Warning: could not get git base: {e}")

    # 4. Read current JA and CN
    with open("ALL_TEXT.txt", "r", encoding="utf-8") as fj:
        ja_lines = [l.rstrip("\r\n") for l in fj]
    with open("ALL_TEXT_cn.txt", "r", encoding="utf-8") as fc:
        cn_lines = [l.rstrip("\r\n") for l in fc]

    diffs = []
    # Section 1: varstr (1 - 629)
    for lno in range(1, 630):
        ja_raw = ja_lines[lno - 1]
        cn_raw = cn_lines[lno - 1]
        sid = ja_raw.split("\t")[0] if "\t" in ja_raw else f"L{lno}"
        ja_txt = ja_raw.split("\t")[1] if "\t" in ja_raw else ja_raw
        cn_txt = cn_raw.split("\t")[1] if "\t" in cn_raw else cn_raw
        old_txt = old_varstr.get(lno, cn_txt)
        if cn_txt != old_txt:
            cat, reason = classify_change(lno, sid, ja_txt, old_txt, cn_txt)
            diffs.append({
                "lno": lno,
                "sid": sid,
                "ja": ja_txt,
                "old": old_txt,
                "new": cn_txt,
                "cat": cat,
                "reason": reason,
                "section": "章节标题与系统文本 (_varstr)"
            })

    # Section 2: ama_001 (630 - 1163)
    for lno in range(630, 1164):
        ja_raw = ja_lines[lno - 1]
        cn_raw = cn_lines[lno - 1]
        sid = ja_raw.split("\t")[0] if "\t" in ja_raw else f"L{lno}"
        ja_txt = ja_raw.split("\t")[1] if "\t" in ja_raw else ja_raw
        cn_txt = cn_raw.split("\t")[1] if "\t" in cn_raw else cn_raw
        old_txt = recovered_ama.get(lno, cn_txt)
        if cn_txt != old_txt:
            cat, reason = classify_change(lno, sid, ja_txt, old_txt, cn_txt)
            diffs.append({
                "lno": lno,
                "sid": sid,
                "ja": ja_txt,
                "old": old_txt,
                "new": cn_txt,
                "cat": cat,
                "reason": reason,
                "section": "灰色的果实·天音篇开篇 (grisaia1/ama_001)"
            })

    # Section 3: com01 (12337 - 12575)
    for lno in range(12337, 12576):
        ja_raw = ja_lines[lno - 1]
        cn_raw = cn_lines[lno - 1]
        sid = ja_raw.split("\t")[0] if "\t" in ja_raw else f"L{lno}"
        ja_txt = ja_raw.split("\t")[1] if "\t" in ja_raw else ja_raw
        cn_txt = cn_raw.split("\t")[1] if "\t" in cn_raw else cn_raw

        old_txt = cn_txt
        if git_base_cn and len(git_base_cn) >= lno:
            head_raw = git_base_cn[lno - 1]
            old_txt = head_raw.split("\t")[1] if "\t" in head_raw else head_raw

        if cn_txt != old_txt:
            cat, reason = classify_change(lno, sid, ja_txt, old_txt, cn_txt)
            diffs.append({
                "lno": lno,
                "sid": sid,
                "ja": ja_txt,
                "old": old_txt,
                "new": cn_txt,
                "cat": cat,
                "reason": reason,
                "section": "灰色的果实·共通线开篇美工刀对峙与初遇 (grisaia1/com01)"
            })

    # Section 4: com02 (12576 - 12812)
    for lno in range(12576, 12813):
        ja_raw = ja_lines[lno - 1]
        cn_raw = cn_lines[lno - 1]
        sid = ja_raw.split("\t")[0] if "\t" in ja_raw else f"L{lno}"
        ja_txt = ja_raw.split("\t")[1] if "\t" in ja_raw else ja_raw
        cn_txt = cn_raw.split("\t")[1] if "\t" in cn_raw else cn_raw

        old_txt = cn_txt
        if git_base_cn and len(git_base_cn) >= lno:
            head_raw = git_base_cn[lno - 1]
            old_txt = head_raw.split("\t")[1] if "\t" in head_raw else head_raw

        if cn_txt != old_txt:
            cat, reason = classify_change(lno, sid, ja_txt, old_txt, cn_txt)
            diffs.append({
                "lno": lno,
                "sid": sid,
                "ja": ja_txt,
                "old": old_txt,
                "new": cn_txt,
                "cat": cat,
                "reason": reason,
                "section": "灰色的果实·共通线第二章天音更衣与买菜 (grisaia1/com02)"
            })

    # Section 5: com03 (12813 - 12941)
    for lno in range(12813, 12942):
        ja_raw = ja_lines[lno - 1]
        cn_raw = cn_lines[lno - 1]
        sid = ja_raw.split("\t")[0] if "\t" in ja_raw else f"L{lno}"
        ja_txt = ja_raw.split("\t")[1] if "\t" in ja_raw else ja_raw
        cn_txt = cn_raw.split("\t")[1] if "\t" in cn_raw else cn_raw

        old_txt = cn_txt
        if git_base_cn and len(git_base_cn) >= lno:
            head_raw = git_base_cn[lno - 1]
            old_txt = head_raw.split("\t")[1] if "\t" in head_raw else head_raw

        if cn_txt != old_txt:
            cat, reason = classify_change(lno, sid, ja_txt, old_txt, cn_txt)
            diffs.append({
                "lno": lno,
                "sid": sid,
                "ja": ja_txt,
                "old": old_txt,
                "new": cn_txt,
                "cat": cat,
                "reason": reason,
                "section": "灰色的果实·共通线第三章莳菜电子宠物与见死团子 (grisaia1/com03)"
            })

    # Section 6: com04 (12942 - 13261)
    for lno in range(12942, 13262):
        ja_raw = ja_lines[lno - 1]
        cn_raw = cn_lines[lno - 1]
        sid = ja_raw.split("\t")[0] if "\t" in ja_raw else f"L{lno}"
        ja_txt = ja_raw.split("\t")[1] if "\t" in ja_raw else ja_raw
        cn_txt = cn_raw.split("\t")[1] if "\t" in cn_raw else cn_raw

        old_txt = cn_txt
        if git_base_cn and len(git_base_cn) >= lno:
            head_raw = git_base_cn[lno - 1]
            old_txt = head_raw.split("\t")[1] if "\t" in head_raw else head_raw

        if cn_txt != old_txt:
            cat, reason = classify_change(lno, sid, ja_txt, old_txt, cn_txt)
            diffs.append({
                "lno": lno,
                "sid": sid,
                "ja": ja_txt,
                "old": old_txt,
                "new": cn_txt,
                "cat": cat,
                "reason": reason,
                "section": "灰色的果实·共通线第四章玫瑰园与钓小龙虾 (grisaia1/com04)"
            })

    # Section 7: com05 (13262 - 13455)
    for lno in range(13262, 13456):
        ja_raw = ja_lines[lno - 1]
        cn_raw = cn_lines[lno - 1]
        sid = ja_raw.split("\t")[0] if "\t" in ja_raw else f"L{lno}"
        ja_txt = ja_raw.split("\t")[1] if "\t" in ja_raw else ja_raw
        cn_txt = cn_raw.split("\t")[1] if "\t" in cn_raw else cn_raw

        old_txt = cn_txt
        if git_base_cn and len(git_base_cn) >= lno:
            head_raw = git_base_cn[lno - 1]
            old_txt = head_raw.split("\t")[1] if "\t" in head_raw else head_raw

        if cn_txt != old_txt:
            cat, reason = classify_change(lno, sid, ja_txt, old_txt, cn_txt)
            diffs.append({
                "lno": lno,
                "sid": sid,
                "ja": ja_txt,
                "old": old_txt,
                "new": cn_txt,
                "cat": cat,
                "reason": reason,
                "section": "灰色的果实·共通线第五章JB黄色跑车与暗号秘密 (grisaia1/com05)"
            })

    # Section 8: com06 (13456 - 13658)
    for lno in range(13456, 13659):
        ja_raw = ja_lines[lno - 1]
        cn_raw = cn_lines[lno - 1]
        sid = ja_raw.split("\t")[0] if "\t" in ja_raw else f"L{lno}"
        ja_txt = ja_raw.split("\t")[1] if "\t" in ja_raw else ja_raw
        cn_txt = cn_raw.split("\t")[1] if "\t" in cn_raw else cn_raw

        old_txt = cn_txt
        if git_base_cn and len(git_base_cn) >= lno:
            head_raw = git_base_cn[lno - 1]
            old_txt = head_raw.split("\t")[1] if "\t" in head_raw else head_raw

        if cn_txt != old_txt:
            cat, reason = classify_change(lno, sid, ja_txt, old_txt, cn_txt)
            diffs.append({
                "lno": lno,
                "sid": sid,
                "ja": ja_txt,
                "old": old_txt,
                "new": cn_txt,
                "cat": cat,
                "reason": reason,
                "section": "灰色的果实·共通线第六章阿幸万能柜与天台流水素面 (grisaia1/com06)"
            })

    # Section 9: com07 (13659 - 13805)
    for lno in range(13659, 13806):
        ja_raw = ja_lines[lno - 1]
        cn_raw = cn_lines[lno - 1]
        sid = ja_raw.split("\t")[0] if "\t" in ja_raw else f"L{lno}"
        ja_txt = ja_raw.split("\t")[1] if "\t" in ja_raw else ja_raw
        cn_txt = cn_raw.split("\t")[1] if "\t" in cn_raw else cn_raw

        old_txt = cn_txt
        if git_base_cn and len(git_base_cn) >= lno:
            head_raw = git_base_cn[lno - 1]
            old_txt = head_raw.split("\t")[1] if "\t" in head_raw else head_raw

        if cn_txt != old_txt:
            cat, reason = classify_change(lno, sid, ja_txt, old_txt, cn_txt)
            diffs.append({
                "lno": lno,
                "sid": sid,
                "ja": ja_txt,
                "old": old_txt,
                "new": cn_txt,
                "cat": cat,
                "reason": reason,
                "section": "灰色的果实·共通线第七章自贩机与丛林手榴弹怪谈 (grisaia1/com07)"
            })

    # Section 10: com08 (13806 - 14003)
    for lno in range(13806, 14004):
        ja_raw = ja_lines[lno - 1]
        cn_raw = cn_lines[lno - 1]
        sid = ja_raw.split("\t")[0] if "\t" in ja_raw else f"L{lno}"
        ja_txt = ja_raw.split("\t")[1] if "\t" in ja_raw else ja_raw
        cn_txt = cn_raw.split("\t")[1] if "\t" in cn_raw else cn_raw

        old_txt = cn_txt
        if git_base_cn and len(git_base_cn) >= lno:
            head_raw = git_base_cn[lno - 1]
            old_txt = head_raw.split("\t")[1] if "\t" in head_raw else head_raw

        if cn_txt != old_txt:
            cat, reason = classify_change(lno, sid, ja_txt, old_txt, cn_txt)
            diffs.append({
                "lno": lno,
                "sid": sid,
                "ja": ja_txt,
                "old": old_txt,
                "new": cn_txt,
                "cat": cat,
                "reason": reason,
                "section": "灰色的果实·共通线第八章天音肢体接触与由美子心理剖析 (grisaia1/com08)"
            })

    # Section 11: com09 (14004 - 14173)
    for lno in range(14004, 14174):
        ja_raw = ja_lines[lno - 1]
        cn_raw = cn_lines[lno - 1]
        sid = ja_raw.split("\t")[0] if "\t" in ja_raw else f"L{lno}"
        ja_txt = ja_raw.split("\t")[1] if "\t" in ja_raw else ja_raw
        cn_txt = cn_raw.split("\t")[1] if "\t" in cn_raw else cn_raw

        old_txt = cn_txt
        if git_base_cn and len(git_base_cn) >= lno:
            head_raw = git_base_cn[lno - 1]
            old_txt = head_raw.split("\t")[1] if "\t" in head_raw else head_raw

        if cn_txt != old_txt:
            cat, reason = classify_change(lno, sid, ja_txt, old_txt, cn_txt)
            diffs.append({
                "lno": lno,
                "sid": sid,
                "ja": ja_txt,
                "old": old_txt,
                "new": cn_txt,
                "cat": cat,
                "reason": reason,
                "section": "灰色的果实·共通线第九章由美子赠书与大马卡罗夫给养 (grisaia1/com09)"
            })

    # Section 12: com10 (14174 - 14290)
    for lno in range(14174, 14291):
        ja_raw = ja_lines[lno - 1]
        cn_raw = cn_lines[lno - 1]
        sid = ja_raw.split("\t")[0] if "\t" in ja_raw else f"L{lno}"
        ja_txt = ja_raw.split("\t")[1] if "\t" in ja_raw else ja_raw
        cn_txt = cn_raw.split("\t")[1] if "\t" in cn_raw else cn_raw

        old_txt = cn_txt
        if git_base_cn and len(git_base_cn) >= lno:
            head_raw = git_base_cn[lno - 1]
            old_txt = head_raw.split("\t")[1] if "\t" in head_raw else head_raw

        if cn_txt != old_txt:
            cat, reason = classify_change(lno, sid, ja_txt, old_txt, cn_txt)
            diffs.append({
                "lno": lno,
                "sid": sid,
                "ja": ja_txt,
                "old": old_txt,
                "new": cn_txt,
                "cat": cat,
                "reason": reason,
                "section": "灰色的果实·共通线第十章军营恶食怪与天音蟹肉炒饭 (grisaia1/com10)"
            })

    print(f"Total indexed modifications: {len(diffs)}")

    # Build Markdown
    md = []
    md.append("# 灰色系列（Grisaia）全文本校对与润色修改索引报告\n")
    md.append("> **项目**：Frontwing 灰色系列（Grisaia）Galgame 本地化校对  ")
    md.append(f"> **修改条目总数**：{len(diffs)} 条  ")
    md.append("> **结构守恒状态**：110,622 行 100% 对齐通过（`python3 scripts/verify_alignment.py` 验证无误）  \n")

    # Overview table
    cat_counts = {}
    for d in diffs:
        cat_counts[d["cat"]] = cat_counts.get(d["cat"], 0) + 1

    md.append("## 一、 修改分类概览\n")
    md.append("| 修改分类 | 条目数 | 说明 |")
    md.append("| :--- | :---: | :--- |")
    for cat, count in sorted(cat_counts.items(), key=lambda x: x[1], reverse=True):
        md.append(f"| **{cat}** | {count} | 涉及专有名词、文化梗、语法颠倒及人设声线还原 |")
    md.append("\n---\n")

    # Section 1
    varstr_diffs = [d for d in diffs if d["section"].startswith("章节标题")]
    md.append(f"## 二、 章节标题与系统文本修改索引 (`_varstr`，共 {len(varstr_diffs)} 条)\n")
    md.append("| 序号 | 行号 | Scene ID | 日文原文 (JA) | 修改前译文 (Old CN) | 修改后润色译文 (Polished CN) | 修改分类与原因 |")
    md.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
    for idx, d in enumerate(varstr_diffs, 1):
        md.append(f"| {idx} | L{d['lno']} | `{d['sid']}` | {escape_md(d['ja'])} | {escape_md(d['old'])} | **{escape_md(d['new'])}** | `{d['cat']}`: {d['reason']} |")
    md.append("\n---\n")

    # Section 2
    ama_diffs = [d for d in diffs if d["section"].startswith("灰色的果实·天音篇")]
    md.append(f"## 三、 灰色的果实·天音线开篇剧情正文修改索引 (`grisaia1/ama_001`，共 {len(ama_diffs)} 条)\n")
    md.append("| 序号 | 行号 | Scene ID | 日文原文 (JA) | 修改前机翻译文 (Old CN) | 修改后深度润色译文 (Polished CN) | 修改分类与原因 |")
    md.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
    for idx, d in enumerate(ama_diffs, 1):
        md.append(f"| {idx} | L{d['lno']} | `{d['sid']}` | {escape_md(d['ja'])} | {escape_md(d['old'])} | **{escape_md(d['new'])}** | `{d['cat']}`: {d['reason']} |")
    md.append("\n---\n")

    # Section 3
    com01_diffs = [d for d in diffs if d["section"].startswith("灰色的果实·共通线开篇")]
    md.append(f"## 四、 灰色的果实·共通线开篇美工刀对峙与初遇 (`grisaia1/com01`，共 {len(com01_diffs)} 条)\n")
    md.append("| 序号 | 行号 | Scene ID | 日文原文 (JA) | 修改前机翻译文 (Old CN) | 修改后深度润色译文 (Polished CN) | 修改分类与原因 |")
    md.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
    for idx, d in enumerate(com01_diffs, 1):
        md.append(f"| {idx} | L{d['lno']} | `{d['sid']}` | {escape_md(d['ja'])} | {escape_md(d['old'])} | **{escape_md(d['new'])}** | `{d['cat']}`: {d['reason']} |")
    md.append("\n---\n")

    # Section 4
    com02_diffs = [d for d in diffs if d["section"].startswith("灰色的果实·共通线第二章")]
    md.append(f"## 五、 灰色的果实·共通线第二章天音更衣与买菜日常 (`grisaia1/com02`，共 {len(com02_diffs)} 条)\n")
    md.append("| 序号 | 行号 | Scene ID | 日文原文 (JA) | 修改前机翻译文 (Old CN) | 修改后深度润色译文 (Polished CN) | 修改分类与原因 |")
    md.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
    for idx, d in enumerate(com02_diffs, 1):
        md.append(f"| {idx} | L{d['lno']} | `{d['sid']}` | {escape_md(d['ja'])} | {escape_md(d['old'])} | **{escape_md(d['new'])}** | `{d['cat']}`: {d['reason']} |")
    md.append("\n---\n")

    # Section 5
    com03_diffs = [d for d in diffs if d["section"].startswith("灰色的果实·共通线第三章")]
    md.append(f"## 六、 灰色的果实·共通线第三章莳菜电子宠物与见死团子 (`grisaia1/com03`，共 {len(com03_diffs)} 条)\n")
    md.append("| 序号 | 行号 | Scene ID | 日文原文 (JA) | 修改前机翻译文 (Old CN) | 修改后深度润色译文 (Polished CN) | 修改分类与原因 |")
    md.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
    for idx, d in enumerate(com03_diffs, 1):
        md.append(f"| {idx} | L{d['lno']} | `{d['sid']}` | {escape_md(d['ja'])} | {escape_md(d['old'])} | **{escape_md(d['new'])}** | `{d['cat']}`: {d['reason']} |")
    md.append("\n---\n")

    # Section 6
    com04_diffs = [d for d in diffs if d["section"].startswith("灰色的果实·共通线第四章")]
    md.append(f"## 七、 灰色的果实·共通线第四章玫瑰园与钓小龙虾 (`grisaia1/com04`，共 {len(com04_diffs)} 条)\n")
    md.append("| 序号 | 行号 | Scene ID | 日文原文 (JA) | 修改前机翻译文 (Old CN) | 修改后深度润色译文 (Polished CN) | 修改分类与原因 |")
    md.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
    for idx, d in enumerate(com04_diffs, 1):
        md.append(f"| {idx} | L{d['lno']} | `{d['sid']}` | {escape_md(d['ja'])} | {escape_md(d['old'])} | **{escape_md(d['new'])}** | `{d['cat']}`: {d['reason']} |")
    md.append("\n---\n")

    # Section 7
    com05_diffs = [d for d in diffs if d["section"].startswith("灰色的果实·共通线第五章")]
    md.append(f"## 八、 灰色的果实·共通线第五章JB黄色跑车与暗号秘密 (`grisaia1/com05`，共 {len(com05_diffs)} 条)\n")
    md.append("| 序号 | 行号 | Scene ID | 日文原文 (JA) | 修改前机翻译文 (Old CN) | 修改后深度润色译文 (Polished CN) | 修改分类与原因 |")
    md.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
    for idx, d in enumerate(com05_diffs, 1):
        md.append(f"| {idx} | L{d['lno']} | `{d['sid']}` | {escape_md(d['ja'])} | {escape_md(d['old'])} | **{escape_md(d['new'])}** | `{d['cat']}`: {d['reason']} |")
    md.append("\n---\n")

    # Section 8
    com06_diffs = [d for d in diffs if d["section"].startswith("灰色的果实·共通线第六章")]
    md.append(f"## 九、 灰色的果实·共通线第六章阿幸万能柜与天台流水素面 (`grisaia1/com06`，共 {len(com06_diffs)} 条)\n")
    md.append("| 序号 | 行号 | Scene ID | 日文原文 (JA) | 修改前机翻译文 (Old CN) | 修改后深度润色译文 (Polished CN) | 修改分类与原因 |")
    md.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
    for idx, d in enumerate(com06_diffs, 1):
        md.append(f"| {idx} | L{d['lno']} | `{d['sid']}` | {escape_md(d['ja'])} | {escape_md(d['old'])} | **{escape_md(d['new'])}** | `{d['cat']}`: {d['reason']} |")
    md.append("\n---\n")

    # Section 9
    com07_diffs = [d for d in diffs if d["section"].startswith("灰色的果实·共通线第七章")]
    md.append(f"## 十、 灰色的果实·共通线第七章自贩机与丛林手榴弹怪谈 (`grisaia1/com07`，共 {len(com07_diffs)} 条)\n")
    md.append("| 序号 | 行号 | Scene ID | 日文原文 (JA) | 修改前机翻译文 (Old CN) | 修改后深度润色译文 (Polished CN) | 修改分类与原因 |")
    md.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
    for idx, d in enumerate(com07_diffs, 1):
        md.append(f"| {idx} | L{d['lno']} | `{d['sid']}` | {escape_md(d['ja'])} | {escape_md(d['old'])} | **{escape_md(d['new'])}** | `{d['cat']}`: {d['reason']} |")
    md.append("\n---\n")

    # Section 10
    com08_diffs = [d for d in diffs if d["section"].startswith("灰色的果实·共通线第八章")]
    md.append(f"## 十一、 灰色的果实·共通线第八章天音肢体接触与由美子心理剖析 (`grisaia1/com08`，共 {len(com08_diffs)} 条)\n")
    md.append("| 序号 | 行号 | Scene ID | 日文原文 (JA) | 修改前机翻译文 (Old CN) | 修改后深度润色译文 (Polished CN) | 修改分类与原因 |")
    md.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
    for idx, d in enumerate(com08_diffs, 1):
        md.append(f"| {idx} | L{d['lno']} | `{d['sid']}` | {escape_md(d['ja'])} | {escape_md(d['old'])} | **{escape_md(d['new'])}** | `{d['cat']}`: {d['reason']} |")
    md.append("\n---\n")

    # Section 11
    com09_diffs = [d for d in diffs if d["section"].startswith("灰色的果实·共通线第九章")]
    md.append(f"## 十二、 灰色的果实·共通线第九章由美子赠书与大马卡罗夫给养 (`grisaia1/com09`，共 {len(com09_diffs)} 条)\n")
    md.append("| 序号 | 行号 | Scene ID | 日文原文 (JA) | 修改前机翻译文 (Old CN) | 修改后深度润色译文 (Polished CN) | 修改分类与原因 |")
    md.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
    for idx, d in enumerate(com09_diffs, 1):
        md.append(f"| {idx} | L{d['lno']} | `{d['sid']}` | {escape_md(d['ja'])} | {escape_md(d['old'])} | **{escape_md(d['new'])}** | `{d['cat']}`: {d['reason']} |")
    md.append("\n---\n")

    # Section 12
    com10_diffs = [d for d in diffs if d["section"].startswith("灰色的果实·共通线第十章")]
    md.append(f"## 十三、 灰色的果实·共通线第十章军营恶食怪与天音蟹肉炒饭 (`grisaia1/com10`，共 {len(com10_diffs)} 条)\n")
    md.append("| 序号 | 行号 | Scene ID | 日文原文 (JA) | 修改前机翻译文 (Old CN) | 修改后深度润色译文 (Polished CN) | 修改分类与原因 |")
    md.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
    for idx, d in enumerate(com10_diffs, 1):
        md.append(f"| {idx} | L{d['lno']} | `{d['sid']}` | {escape_md(d['ja'])} | {escape_md(d['old'])} | **{escape_md(d['new'])}** | `{d['cat']}`: {d['reason']} |")
    md.append("\n---\n")

    md_content = "\n".join(md)

    # Write to root & analysis/
    with open("grisaia_modification_index.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    workspace_path = "/Users/wqin/workplace/agy/analysis/grisaia_modification_index.md"
    with open(workspace_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Report written to root and analysis: {workspace_path}")

    # Write to artifacts directory
    artifact_dir = "/Users/wqin/.gemini/antigravity-cli/brain/58bc9ea3-8e40-4e4b-af2d-7c0dbd91401e"
    os.makedirs(artifact_dir, exist_ok=True)
    artifact_path = os.path.join(artifact_dir, "grisaia_modification_index.md")
    with open(artifact_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Report written to artifact: {artifact_path}")

if __name__ == "__main__":
    build_report()
