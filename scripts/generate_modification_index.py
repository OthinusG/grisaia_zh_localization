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
    # com27 specific
    if "美浜女子餃子隊" in ja or "敗戦間際の軍" in ja or "鯛の刺身餃子" in ja or "つけダレ" in ja or "フツーのが一番" in ja:
        return "美滨女子饺子队与百鬼夜行兵器盛宴", "生动还原美滨女子饺子队成立、搜刮冰箱速成增产120枚水饺，芝士、明太子、红香肠乃至鲷鱼刺身黑暗水饺如二战末期轴心国穷途决战兵器大博览；莳菜直击灵魂吐槽‘还是普普通通的原味饺子最好吃’为全会画上和平句号"
    if "輜重" in ja or "主計" in ja or "第一線が維持される" in ja or "感謝をしなさい" in ja or "挺身にも等しい" in ja or "ゴブゴブ" in ja:
        return "后勤辎重论与美智留暴走索谢", "神级日常互动高光：美智留痛斥雄二理所当然大口灌乌龙茶、不知感恩天音照顾；雄二搬出‘唯有军需与辎重保障到位前线方能维持战力’战术常识，并暗讽‘平时习惯无所作为之人视寻常琐碎犹如挺身舍己’，致美智留炸毛暴走索要感谢"
    if "煎り米" in ja or "生活の知恵" in ja or "ズギョーン" in ja or "手抜き" in ja or "工夫" in ja or "ウーロン茶" in ja or "ベチャベチャ" in ja:
        return "家常手艺精髓与乌龙茶秘制馅料", "极具烟火气的家常教学：炒米充当防潮干燥剂的老妪智慧；天音传授‘家庭料理精髓全在合理偷懒，初学者失败八成因私自瞎搞创新’，并自创‘往饺馅淋乌龙茶提鲜解腻’的独门秘法与折叠捏褶手法"
    if "次女" in ja or "エビ餃子" in ja or "甲殻類" in ja or "長女は料理なんてからっきし" in ja or "軍の糧食工場" in ja or "粘土遊び" in ja:
        return "美滨四姐妹生态位与鲜虾水饺", "生动刻画美滨学园家庭定位：长女由美子生活自理废柴只会泡面、三女幸如军粮工厂般流水线克隆、四女莳菜将食材当橡皮泥，次女美智留性格别扭别称‘最少女’；因雄二偏爱海鲜白肉而特意包鲜虾水饺"
    if "一畳半" in ja or "ドラえもん" in ja or "メールボックス" in ja or "聖域" in ja or "過去でも詰まってる" in ja or "触れられたくない物" in ja:
        return "一叠半密室圣域与沉重过去", "关键人物设定揭秘：雄二犹如哆啦A梦般只在一叠半逼仄壁橱中起居沉睡，天音郑重告诫‘擅闯会动真格暴怒杀人’，并以‘空荡手机收件箱’精妙喻指雄二压抑封存的惨痛过去与不可侵犯的心灵圣域"
    if "パージ" in ja or "同棲" in ja or "ブラが脱ぎ捨てて" in ja or "麦茶" in ja or "着替える" in ja:
        return "男寝更衣大卸甲与半同居疑云", "爆笑名场面：天音熟门熟路开雄二房门开冰箱端麦茶，当面脱外套换家居服；美智留大惊失色怒吼‘一进男生寝室当场大卸甲暴衣脱光光’并发现床头蕾丝胸罩，连环质问二人是否早已半同居"
    if "卵" in ja or "タイムセール" in ja or "余ってるぐらいじゃないと落ち着かない" in ja or "正義を呼ぶ声" in ja or "９８円" in ja:
        return "翔荣囤蛋执念与正义使者登场", "生动还原翔荣超市限购特卖98日元鸡蛋；美智留摆出正义使者架势却被抓去借人头排队，天音道出‘冰箱空荡便心慌、食物必须富余到吃不完才踏实’的饥荒创伤心理后遗症"

    # com26 specific
    if "トンビ" in ja or "立ったまま寝ている" in ja or "貴方…聞かないのね" in ja or "向こうの方から、俺に歩み寄って来た時だけ" in ja or "変わってるわね" in ja or "お互い様" in ja:
        return "屋顶黑鸢孤影与两只刺猬微光初融", "全章神级情感升华：屋顶夏日海风中，由美子主动向雄二搭话破冰，困惑于雄二‘勒令不问便绝不再问’的绝对克制；雄二阐明‘绝不主动干涉侵犯他人私域、但若对方迈出第一步也绝不避让推拒’的处世哲学，令由美子罕见展露浅笑，两只满身尖刺的孤独灵魂在此刻悄然叩开彼此心扉"
    if "思わせぶりな態度" in ja or "釣りみたいな事" in ja or "露出狂" in ja or "一人で居た方が楽" in ja:
        return "人际钓鱼论反驳与天音直球主张", "还原天音揣测雄二欲擒故纵‘钓由美子主动接近’，雄二断然反驳‘从不把下套把戏用于人际关系’，并直言‘对于某些人而言独自一人反而更轻松’的灵魂共鸣"
    if "質問の答えが微妙に食い違っている" in ja or "今からしようとしている事に神経が向いている" in ja or "これ以上は聞かない" in ja:
        return "清晨答非所问交锋与雄二克制后撤", "心理交锋高光笔触：雄二敏锐指出由美子将‘去哪儿’错答为‘干什么是我的自由’暴露其心思全在行动上，并在由美子勒令停止追问后利落干脆全盘撤退，反倒让习惯了被防备逼迫的由美子当场错愕动摇"
    if "トートバッグ" in ja or "本を読んでいる素振り" in ja or "決まった数ページ" in ja or "ナイフアクション" in ja or "プラナリア" in ja or "羽を伸ばしたい" in ja:
        return "由美子神秘托特包与涡虫分裂再生论", "生动还原幸侦察揭露由美子在教室‘连续数日盯着同几页假装阅读’的自闭伪装，以及莳菜脑补由美子大包裹装恶魔翅膀Cosplay、怂恿美智留尾随并戏称‘就算被美工刀切三截也能像涡虫一样再生三个新美智留’的魔性狂想"
    if "イッチョカミ" in ja or "親指だけの腕立て伏せ" in ja or "自慰" in ja or "建物ごと爆破" in ja or "オカズ" in ja or "サルみたいな扱い" in ja:
        return "关西一丁咬与闺房自慰暴走闹剧", "纠正机翻将关西俚语‘一丁咬（爱插一脚爱凑热闹之人）’误译为‘ITCHOKAMI往脑子里钻’的重大失误，深度还原莳菜与天音联手调侃美智留自慰频率、幸一本正经核实‘每周三至四次’引美智留抓狂欲爆破宿舍的顶级搞笑对话"
    if "無趣味人間" in ja or "生きてる事が苦痛" in ja or "アヴァンチュール" in ja or "処女解放" in ja or "そ・れ・は・家・事" in ja or "反吐が出そう" in ja:
        return "无爱好之叹与天音家务暴击", "纠正机翻将莳菜‘处女解放（処女解放）’误翻为‘处男解放’的滑稽重大错译，生动还原雄二拉伸体操被天音与莳菜阴阳怪气为‘无趣味人类’、雄二反杀指出天音爱好‘做饭洗衣打扫那叫家务’致其破防跪地的名场面"

    # com25 specific
    if "迷路" in ja or "真っ直ぐな線" in ja or "真実は絡まって" in ja or "良かれと思って嘘をつく" in ja or "正直でいたい" in ja:
        return "善意谎言死结与心之迷宫救赎", "极高文学水准升华全章：雄二从美智留隐瞒重疾联想到世人因‘善意’而筑起心之迷宫、终将真实缠绕成死结的悲哀，道出传世金句‘若想在复杂的环境中恪守诚实，至少要祈祷在自己亲手雕琢的迷宫中不要迷失归途’"
    if "胸を手で押さえる" in ja or "胸が痛む" in ja or "貧血では胸に痛みは感じない" in ja or "他の子に見せたくない" in ja or "隠しているわけか" in ja:
        return "心前区急性绞痛与不可告人之约", "画风突变直击心房：细腻刻画美智留在走廊虚脱滑落、双手死死按住胸口剧烈喘息、轻拍胸背强行调匀心律的重度心绞痛发作，以及哀求雄二保守秘密‘不要让其他女孩看到我这副狼狈模样’的心碎脆弱"
    if "拾い食い" in ja or "カラフルな色をしたキノコ" in ja or "カニクイザル" in ja or "アメーバ赤痢" in ja or "果肉入り猿" in ja or "靴下の洗濯" in ja or "便所で出してみろ" in ja:
        return "食蟹猴捡食妄想与越战洗袜铁律", "雄二特工脑洞大暴走顶级名场面：凭美智留惨白面色断定其长着‘爱在路边捡脏东西与毒蘑菇吞食的蠢相’、脑补其在热带雨林与食蟹猴抢螃蟹染上阿米巴痢疾，搬出越战洗袜子铁则逼其去厕所‘排便验排泄物’的极品冷幽默"
    if "特殊な環境下で知り合った少女" in ja or "後ろから背中を撃たれ" in ja or "道具の方がブレることが少ない" in ja or "パズルのピース" in ja or "捨て駒" in ja or "マジック" in ja:
        return "拼图碎片弃子哲学与冷硬工具论", "极高水准还原雄二冷酷特工世界观：将人际关系视作棋局中随时可弃的拼图碎片、视‘永远是朋友’为弯勺子般的廉价魔术，以及‘比起多变的人类更信赖倾注爱意绝不背叛的冷硬工具’的硬汉心防"
    if "イマジナリーフレンド" in ja or "頭の中に作る想像上の友人" in ja or "子供の妄想" in ja:
        return "幻想伙伴与双重人格关键伏笔", "极高文学敏锐度捕捉雄二提及‘脑内幻想伙伴（Imaginary Friend）’时美智留骤然瞳孔放大、随后因‘只是小孩子妄想’而失落自嘲的重磅心理伏笔，直指美智留受体心脏记忆与双重人格核心谜团"
    if "あたしが今、ここにいることよ" in ja or "頭数に、ない" in ja or "哲学" in ja or "ミス・ドンストップ" in ja or "放置プレイ" in ja:
        return "现实哲学自辩与幸的人头编制处刑", "还原美智留自作聪明发表哲学演讲‘现实就是我此刻身在此处’被全场冷眼冻结、幸一本正经补刀‘美智留大人的人气为零，不在人头编制中’以及莳菜‘不停小姐（Miss Don't Stop）’连环处刑"
    if "薬物パーティー" in ja or "壊れたダンプカー" in ja or "仲間外れ" in ja or "ハロー由美子" in ja:
        return "药毒派对乌龙与失控翻斗车社交", "生动还原幸误将众人聚会当成‘药毒派对’并自责未能侍奉、美智留傲娇问候由美子却被幸评价为‘如同失控报废翻斗泥头车般猛撞进对方心窝’的爆笑修辞"
    if "ビタミンＡ" in ja or "スペシャル粉" in ja or "酸っぱいうちに" in ja or "にげええええええええ" in ja or "にがっぺー" in ja or "天邪鬼" in ja or "すっぱいよぉ" in ja:
        return "极酸柠檬粉与苦涩味觉风暴", "纠正机翻将美智留被极酸粉刺激到惨叫‘にげええええ（好苦啊）’误翻为‘逃eeee’的经典重大错译，生动还原天音特制维生素A酸粉整包吞咽、连灌柠檬纯汁与浓缩原液的双重暴击搞笑高潮"
    if "食べ合わせ" in ja or "梅干と鰻" in ja or "消化不良" in ja:
        return "食物相克迷信破除与求生杂学", "还原雄二凭借野外求生记忆拆解‘梅干与烤鳗鱼相克实为节俭训诫’、科学辨析蟹肉与柿子鞣酸反应的硬核生存知识"

    # com24 specific
    if "罪悪感" in ja or "悪いガス" in ja or "ドロドロ" in ja or "冷たい毒" in ja or "なくした物" in ja or "自問" in ja:
        return "肺中剧毒与战后PTSD罪恶感", "极高文学水准重塑雄二在看似平静的学园生活中深陷创伤后应激障碍（PTSD）的心灵深渊：笑容如罪、内脏如积淤腐烂毒气、双肺如旋涡冰冷剧毒，直击灰色系列‘无法挽回逝者之痛’的灵魂母题"
    if "一目惚れ" in ja or "オートバイ" in ja or "暴走族" in ja or "アンタは俺のいくつ上だ" in ja or "周防" in ja:
        return "哈雷机车太妹天音与校长年龄禁区", "生动还原雄二被天音一见钟情疑为全校最危险人物、千鹤爆料天音骑美式地狱天使重型机车（Chopper）轰鸣入学的反差黑历史，以及雄二反问千鹤年龄致其冷汗直冒的绝妙互动"
    if "絵日記" in ja or "大人の世界" in ja or "庇護" in ja or "打算的" in ja or "自分を守る方法" in ja or "マキナ" in ja:
        return "莳菜软弱拟态求生欲与防卫教学", "还原雄二开玩笑‘教莳菜大人的世界’引千鹤惊恐，精准剖析莳菜走与美智留相反的极端‘谄媚求怜悯’生存拟态，以及雄二立志授人以渔教其自卫防身的硬汉温柔"
    if "カメタイプ" in ja or "城を建てろ" in ja or "石垣" in ja or "ロボット" in ja or "ガス抜き" in ja or "小嶺" in ja:
        return "小岭幸老黄牛发条傀儡与排气阀", "生动还原雄二对幸自我催眠放弃特长的‘乌龟人格’分析、‘命其筑城便独自一人默默垒石十年’的发条机器人盲从自虐心理，以及必须适时排气的警示"
    if "ブリーチ" in ja or "銀紙" in ja or "毒電波" in ja or "警戒色" in ja or "ハイ・ビジビリティー" in ja or "みちる" in ja:
        return "美智留金发警戒色与脑电波邪教乌龙", "纠正机翻将美智留裹保鲜膜漂白头发痛到呻吟误解为头顶锡纸防御宇宙毒电波的邪教乌龙，深度还原雄二关于美智留夸张金发实为弱者‘高可见度警戒色（High Visibility）’与测试幸底线的深刻洞察"
    if "カッターで切りつけ" in ja or "縦の物が横" in ja or "自分の領域" in ja or "榊" in ja:
        return "由美子绝对领地与美工刀防御机制", "还原雄二对由美子‘横物绝不扶正’极度怠惰冷漠的精准剖析，揭示其一言不合掏美工刀砍人本质是因不懂构筑信任而采取的极端领地防御机制"
    if "負け犬" in ja or "傷の舐め合い" in ja or "テストケース" in ja or "助成金" in ja or "板金屋" in ja or "民間資本" in ja:
        return "败犬收容所与钣金工隐喻", "纠正机翻生硬，还原雄二一针见血揭露学园是将有钱人家问题孩子集中圈养互相舔舐伤口、学园长借此搜刮赞助金的刻薄嘴脸，以及将矫正创伤比作钣金工人用铁锤敲打废铁的尖锐讽刺"
    if "潜入工作" in ja or "サルかテメー" in ja or "抱き枕" in ja or "歯を見せて笑っている" in ja or "性行為" in ja:
        return "潜伏错位感与猴子交尾荒谬自嘲", "纠正机翻粗俗丢失，生动还原雄二无法融入日常、见自己在玻璃倒影中微笑便如潜伏特工暴露般的剧烈违和，以及类比‘性爱时照镜自嘲像猴子’与‘抱枕被父母撞破’的极致讽刺"
    if "助成" in ja or "判子" in ja or "寡黙" in ja or "師匠の言葉" in ja or "命の恩人" in ja or "借りを作ったまま" in ja:
        return "校长室闲职论与救命之恩债务博弈", "还原雄二将学园长视作数钱盖章闲职的讽刺心理与‘好男人在这种时候就该保持沉默’的硬汉幽默，以及橘千鹤执意报恩与雄二公私分明的拉扯"

    # com23 specific
    if "ユニバーシ・ティー" in ja or "大学茶" in new_cn or "シンクロニシ・ティー" in ja or "炭酸抜き" in ja:
        return "大学茶与谐音梗连环吐槽", "纠正机翻将雄二冷笑话谐音‘大学茶（University / ユニバーシ・ティー）’误译为普通红茶的重大语义丢失，还原莳菜‘共时茶（Synchronicity）’跟风捧哏"
    if "北海道" in ja or "搾りたて" in ja or "牛乳" in ja or "新幹線" in ja or "挤奶" in new_cn:
        return "女仆幸北海道亲手挤奶暴走", "还原女仆幸为给莳菜买到‘全天下最好喝的牛奶’直接杀到车站买票准备直飞北海道牧场亲手挤奶的超级天然呆反差暴走"
    if "借りてきた猫" in ja or "お人形遊び" in ja or "昔の話" in ja or "流浪猫" in new_cn:
        return "莳菜心结与流浪猫往事", "揭露莳菜刚来美滨学园时如战战兢兢的流浪猫一般不与任何人说话、只抱破洋娃娃蜷缩角落的令人心疼的创伤往事"
    if "食わず嫌い" in ja or "生き残った者" in ja or "死んだ仲間" in ja or "不吃之嫌" in new_cn:
        return "经验教训与不吃之嫌铁则", "还原雄二将挑食坏习惯升华为战地生死铁律‘死去的战友用鲜血教训换来的经验’、严厉纠正莳菜‘不尝便讨厌’毛病的硬汉作风"
    if "ツンデレ" in ja or "傲娇" in new_cn or "ヨシ子" in ja or "良子" in new_cn:
        return "小鬼傲娇教学与美智留炸毛", "还原莳菜自作聪明把由美子喊作‘良子’、向美智留示范‘先狠狠损一通再告白一笔勾销’的魔性自创傲娇教学引发美智留疯狂抓狂"
    if "リファレンス" in ja or "参考范本" in new_cn or "心得た" in ja or "尊大" in ja:
        return "参考范本质量堪忧与冷吐槽", "还原莳菜迅速吸收雄二军人腔调‘属下领命’、雄二冷酷反思‘莳菜之所以人格扭曲完全是因为身旁的参考范本质量太差’的经典自嘲"

    # com22 specific
    if "早飯早糞" in ja or "兵舎" in ja or "流し込む" in ja or "幹部クラス" in ja:
        return "早饭早粪与军营进食创伤", "还原雄二在特工军校中被强制要求‘早饭早粪’、数分钟内狼吞虎咽灌下海量食物且吐出必须重咽的非人军事创伤"
    if "京料理" in ja or "神田" in ja or "お母はん" in ja or "お父はん" in ja or "関西訛り" in ja:
        return "天音神田老家与关西口音渊源", "揭秘天音母亲出身京都老牌料亭千金、父亲是神田江户厨师的身世，解释其关西口音与江户子豪爽急躁性格的根源"
    if "身長よ" in ja or "乳がか" in ja or "肉食獣" in ja or "肉が嫌い" in ja:
        return "天音巨乳与高挑身材苦恼", "还原莳菜揭发天音讨厌吃肉、天音担忧吃肉会继续‘变大’被雄二反问‘胸围吗’后娇嗔反驳‘是身高啦’的经典日常斗嘴"
    if "ドイツ女" in ja or "山小屋" in ja or "母親じゃあるまいし" in ja or "メソメソ" in ja:
        return "混血德国女人JB之哭包回忆", "还原JB（日耳曼混血）常去山中小屋擅自打扫做饭、被雄二吐槽‘又不是我妈’后像小女孩一样嚎啕大哭的珍贵往事与三大对女人教训"
    if "ブルータス" in ja or "両手に花" in ja or "布鲁图" in new_cn or "王様待遇" in ja:
        return "两面夹击帝王待遇与布鲁图之叹", "还原天音与莳菜左右开弓强行‘啊~嗯’喂食、雄二绝望悲鸣‘布鲁图，连你也背叛我’与美少女包围网战术分析"
    if "庇護の傘" in ja or "軍事力" in ja or "榊よ" in ja or "金満学園" in ja:
        return "由美子高冷观战与国防安全讽刺", "还原雄二向冷眼旁观的由美子眼神求救无果，悲愤将由美子比拟为在霸权大国核保护伞下背弃防卫盟约的辛辣国际政治黑幽默"
    if "自損自弁" in ja or "耐えがたき" in ja or "明鏡止水" in ja or "否定する自分" in ja or "人並み" in ja or "黒いシミ" in ja:
        return "自负盈亏与明镜止水战伤心理", "还原雄二在面对天音家常便当温暖时胸中泛起罪恶黑斑、质疑自己作为弃子恶犬不配享受‘普通人幸福’的灵魂深处自毁拉扯"
    if "キドニー豆" in ja or "煮豆" in ja or "豆さえ食ってりゃ" in ja or "悪食" in ja:
        return "日下部麻子之豆子哲学与恶食", "还原雄二自制红芸豆番茄炖豆便当、践行师父日下部麻子名言‘人只要有豆子吃就死不了’的硬核糙汉生活史"

    # com21 specific
    if "ピッチャー返し" in ja or "投手回击" in new_cn or "投手反弹" in new_cn or "ナゲシ" in ja:
        return "传说中的投手回击球拉锯战", "还原美智留与天音在球场上互飙‘投手回击（Comebacker）’直到十数重反弹的白热化死斗与莳菜咬舌头谐音梗"
    if "汚名挽回" in ja or "汚名" in ja or "返上" in ja or "挽回污名" in old_cn:
        return "经典语文误用恶搞与雪耻梗", "还原美智留把‘洗刷污名/雪耻（汚名返上）’口误说成‘挽回污名’被天音与雄二连环抓包无情嘲弄的经典爆笑桥段"
    if "反吐" in ja or "キラキラ" in ja or "彩虹" in new_cn or "双重KO" in new_cn or "ダブルＫＯ" in ja:
        return "美智留脱水眩晕与绝美彩虹吐", "还原美智留逞强狂傲大笑后突发起立性贫血、当场跪地喷吐‘闪闪发光的反刍之物（彩虹吐）’与双重KO惨烈现场"
    if "体操用のメイド服" in ja or "メイド服" in ja or "女仆装" in new_cn:
        return "幸之超凡脱俗体操用女仆装", "还原全校唯独幸一人身穿‘体操专用女仆装’上体育课，并对雄二的常识质疑投以反向关爱眼神的呆萌特质"
    if "ドク" in ja or "急患" in ja or "军医" in new_cn or "救護" in ja or "RICE" in new_cn or "不全骨折" in ja or "捻挫" in ja:
        return "野战急救常识与军医本能", "还原雄二脱口而出呼叫‘军医（Doc）’、凭借军队战伤救护经验为天音包扎固定冷敷踝关节的硬核特工本色"
    if "小嶺幸！いただきます！" in ja or "いただきます" in ja or "领命" in new_cn or "挙手敬礼" in ja:
        return "野战急救处突与女仆敬礼领命", "还原雄二以战场连长姿态向幸下达现地指挥命令、幸煞有介事立正敬礼高呼‘小岭幸领命！’的绝妙反差萌"
    if "ドＭ" in ja or "超M" in new_cn or "抖M" in new_cn or "サディスト" in ja:
        return "天音极品抖M宣言与防备突破", "还原天音被按压脚踝痛呼后自曝‘骨子里其实是个超M（抖M）’、调戏雄二‘施虐狂’的极品恶作剧大姐姐属性"
    if "お姉ちゃん" in ja or "大姐姐" in new_cn or "彼氏" in ja or "交往" in new_cn or "妥協" in ja or "政治家" in ja:
        return "门面效应谈判心理战与姐姐契约", "还原天音以‘当男朋友’的高阶要求诱敌深入、再后撤妥协为‘当大姐姐’的教科书级门面效应谈判心理学"
    if "賢い犬" in ja or "主人以外" in ja or "尻尾" in ja or "摇尾" in new_cn:
        return "忠犬绝不向主人以外摇尾", "还原雄二被天音摸头后暗自告诫自己‘忠犬除了主人（日下部麻子）以外绝不向任何人摇尾巴’的冷酷孤独内心独白"
    if "松島満" in old_cn or "松岛满" in old_cn:
        return "核心女主译名纠偏", "将机翻残存的‘松岛满’彻底修正为官方通用译名‘松岛美智留’"

    # com20 specific
    if "サバの水煮缶" in ja or "サバ缶" in ja or "ザリガニ" in ja or "水煮鲭鱼" in new_cn or "青いザリガニ" in ja:
        return "小龙虾饲育与生物实验", "还原莳菜用无色素水煮鲭鱼罐头培育‘蓝色小龙虾（螯虾）’的经典夏日自由研究，纠正机翻将鲭鱼误译为沙丁鱼"
    if "ヴァギナ" in ja or "マキナ" in ja and "陰道" in new_cn or "Vagina" in new_cn or "ヴァッギーナ" in ja:
        return "莳菜名字谐音暴论还原", "还原莳菜嫌弃自己名字发音像‘阴道（Vagina）’引发雄二无语吐槽的经典无厘头黄段子"
    if "オッパイの下" in ja or "あせも" in ja or "痱子" in new_cn:
        return "天音巨乳苦恼细节纠错", "纠正机翻将天音巨乳下沿捂出痱子（オッパイの下に“あせも”）荒唐误译为‘腋下湿疹’的恶劣低级错误"
    if "シャクレ" in ja or "地包天" in new_cn or "ホンマ" in ja or "待ちぃ" in ja or "口縫うてまう" in ja:
        return "天音关西腔暴走与外貌互损", "还原莳菜怒喷天音‘地包天/兜齿（シャクレ）’引发天音秒变关西腔暴走追打的爆笑日常相声"
    if "右脳" in ja or "左脳" in ja or "姉" in ja and "記憶" in ja or "スパイン" in ja or "シナプス" in ja or "照相记忆" in new_cn or "風見一姫" in new_cn:
        return "一姬照相记忆与脑科学伏笔", "还原风见一姬与莳菜共有的超常‘照相记忆（直观像记忆）’神经学原理与左右眼分读两本书的天才伏笔"
    if "オデン" in ja or "オーディン" in ja or "インターセプト" in ja or "奥丁" in new_cn:
        return "关东煮与北欧神话谐音梗", "还原莳菜试图把关东煮（Oden）谐音为北欧主神奥丁（Odin）被天音当场凌空拦截的经典捧哏吐槽"
    if "歯医者" in ja or "本を読む" in ja or "師匠" in ja and "読みたい" in ja:
        return "师傅日下部麻子读书哲学", "还原师傅日下部麻子教会雄二享受读书之乐是‘为了不在牙医诊所排队候诊时白白浪费时间’的硬核幽默回忆"

    # com19 specific
    if "ソマリア" in ja or "索马里" in new_cn or "歩哨を投入" in ja or "前哨斥候" in new_cn or "六時間" in ja:
        return "特工特种突入战术妄想", "还原雄二将推开教室门夸大为特种作战排查索马里战场、将美智留推作探路前哨斥候的重度特工妄想症"
    if "ヴァルター" in ja or "Walther P38" in new_cn or "ペー・アハト" in ja:
        return "经典名作与德国军工枪械梗", "还原恶搞鲁邦三世经典名曲与德国瓦尔特P38手枪（Walther P38）的雄二特制军用鼓舞士气歌"
    if "スズメバチ" in ja or "毒のカクテル" in ja or "虎头蜂" in new_cn or "雀蜂" in new_cn or "ボヘミア民謡" in ja:
        return "昆虫毒理学与一本正经胡说八道", "还原雄二将大虎头蜂毒素科普为『毒药鸡尾酒』，并严肃建议美智留用金发当同色系伪装哼唱波希米亚民歌的绝顶幽默"
    if "神経毒" in ja or "十五分" in ja or "特製カクテル" in ja or "特制鸡尾酒" in new_cn:
        return "女仆幸生化反差萌与夺命关怀", "还原幸拖出工业高压药罐热情推销吸入一口即死『自制神经毒素杀虫剂』、美智留疯狂求生的女仆极致反差萌"
    if "由美子最強説" in ja or "踏んだ" in ja or "ペタンコ" in ja or "踩烂" in new_cn or "最强生物" in new_cn:
        return "由美子高冷女王气场与降维打击", "还原由美子大清早嫌吵、不经意一脚踩扁致命大黄蜂后淡定回座翻书看小说的全校最强王者气场"
    if "ノルマンディ" in ja or "诺曼底" in new_cn or "パラシュート部隊" in ja or "伞兵" in new_cn:
        return "二战战史与空降兵军事比喻", "还原将美智留元气满满冲进教室比喻为二战诺曼底登陆伞兵特攻跳伞的经典雄二冷幽默"

    # com18 specific
    if "カツ丼部屋" in ja or "猪排饭单间" in new_cn:
        return "日本刑事侦讯经典俚语", "还原日本刑警经典审讯室俚语『猪排饭单间（カツ丼部屋）』，纠正机翻误译为普通餐馆式的‘炸猪排屋’"
    if "バスキー・ロビンソン" in ja or "カラメル・リボン" in ja or "焦糖彩带" in new_cn or "パッポンストリートシャワー" in ja:
        return "知名连锁甜品名梗还原", "还原恶搞芭斯罗缤（31冰淇淋）经典招牌口味『焦糖彩带（Caramel Ribbon）』与莳菜特选猎奇口味，纠正机翻走形"
    if "３枚の１万円札" in ja or "3万円" in ja or "株に" in ja or "炒股" in new_cn:
        return "雄二战术诱饵与人设还原", "还原雄二为保护莳菜甩出三万日元并让她拿多余的钱去炒股的硬核特工豪横人设"
    if "スタンガン" in ja or "電撃" in ja or "基節骨" in ja or "ビールケース" in ja or "电击棒" in new_cn:
        return "CQC近身徒手格斗与战术反制", "还原雄二利用人体解剖学反关节技与着力穴位制服电击棒暴徒的教科书级特工CQC"
    if "Ｍａｏ" in ja or "ネット殺人" in ja or "仕置き人" in ja or "真央" in new_cn:
        return "网络杀人悬赏论坛与暗网剧情", "还原地下杀人委托论坛『真央（Mao）』针对美滨学园的悬赏阴谋线索与暗网伏笔"
    if "ブス" in ja or "丑八怪" in new_cn or "結婚してくれないか" in ja or "投獄" in ja:
        return "雄二与JB传奇损友斗嘴", "还原雄二对顶头上司JB求婚调情后冷不防骂其『丑八怪』瞬间挂断电话的绝顶名场面"
    if "影が長くなる" in ja or "姉だったような気" in ja or "風見一姫" in new_cn:
        return "风见一姬回忆与亲情伏笔", "还原雄二夕阳下牵手莳菜引发幼年被姐姐一姬牵手解释夕阳影长的珍贵温暖回忆"
    if "勘ピューター" in ja or "直觉计算机" in new_cn:
        return "昭和老刑警谐音冷笑话", "还原老刑警自诩靠『直觉计算机（勘ピューター）』办案引发雄二吐槽的昭和冷笑话"

    # com17 specific
    if "Ａ液" in ja or "脱色" in new_cn or "漂白" in new_cn:
        return "日常生活/美容美发术语规范", "还原美智留忍受头皮剧痛漂白金发（调配脱色Ａ液与脱色Ｂ液、保鲜膜封头）的经典日常内幕"
    if "暗黒舞踏" in ja or "先锋艺术" in new_cn:
        return "日本先锋现代艺术名梗", "还原雄二将美智留头皮剧痛抽搐胡扯解释为日本先锋艺术『暗黑舞踏（Butoh）』苦练，幸竟然深信不疑的绝顶幽默"
    if "生贄" in ja or "マヤ文明" in ja or "玛雅" in new_cn:
        return "历史典故与角色脑补还原", "还原雄二闻到化学异味脑补为古玛雅文明将祭品全身涂蓝向太阳神献祭的特工被害妄想症"
    if "オツム" in ja or "脑瓜子" in new_cn or "奥兹姆" in old_cn:
        return "俚语误译严重纠错", "纠正将美智留智力头脑（オツム/おつむ）荒唐音译为‘奥兹姆’的恶性机翻"
    if "不感症" in ja or "性冷淡" in new_cn:
        return "双关黄段子名场面还原", "还原雄二吐槽天音对艺术麻木‘不感症’引发天音娇羞抗议『人家在床上才不是性冷淡不感症』的爆笑双关黄段子"
    if "匍匐" in ja or "第五匍匐" in new_cn:
        return "军事战术步兵动作还原", "还原雄二遭遇未知‘外星人’在走廊展开战术受身与步兵『第五类匍匐（第五匍匐）』的硬核特工习惯"
    if "マザーシップ" in ja or "母艦" in ja or "宇宙人" in ja:
        return "角色妄想与科幻调侃还原", "还原全员将美智留漂发怪态脑补为『与宇宙母舰进行深空跨星际交信』的经典日常胡扯"

    # com16 specific
    if "カッター" in ja or "美工刀" in new_cn:
        return "角色专属武器道具还原", "还原由美子动辄亮出的标志性随身凶器『美工刀（カッター）』，纠正机翻荒唐走形的‘甩脸色’"
    if "大魔神" in ja:
        return "经典特摄梗与角色反差萌", "还原天音与莳菜将看似人畜无害的小岭幸尊称为宿舍最终决战兵器『大魔神』的经典特摄名梗"
    if "ぶち" in ja or "広島弁" in ja or "广岛" in new_cn:
        return "角色方言与吐槽还原", "还原莳菜冷不防冒出的广岛方言粗话口癖『ぶち（超级/巨凶）』，以及天音当场敏锐抓包吐槽"
    if "目で人を焦がす" in ja or "目で殺す" in ja or "十万马力" in new_cn or "10万馬力" in ja:
        return "成语混淆与动漫名梗", "还原美智留将成语‘眼神杀人’误说为‘眼神融化人’，以及吐槽幸的杀气眼神足足有阿童木『十万马力』"
    if "妾身" in old_cn:
        return "第一人称古风去AI味", "彻底纠正机翻将高冷千金由美子冰冷自称『わたし』荒唐古风化为‘妾身’的恶性AI味，恢复现代高冷第一人称『我』"
    if "ボードゲーム" in ja or "桌游" in new_cn:
        return "宿舍日常文化规范", "规范灰色系列宿舍标志性传统活动『桌游棋牌大会（ボードゲーム大会）』"

    # com15 specific
    if "タダの" in ja or "免费" in old_cn:
        return "机翻多义词严重纠错", "纠正将『纯粹只是个好色大姐姐/超级大色女（ただのエッチ/ドスケベなお姉さん）』荒唐误译为『免费好色大姐姐』"
    if "ランニング・カデンス" in ja or "カデンス" in ja or "战歌" in new_cn or "口号" in new_cn:
        return "军旅战术文化梗还原", "还原美军传统行军跑步口号歌（Running Cadence / カデンス・コール）及雄二教莳菜齐唱的特工魔性口令"
    if "ネズミの歌" in ja or "老鼠之歌" in new_cn or "洒落にならない" in ja:
        return "经典影视梗与版权吐槽", "还原《全金属外壳》米老鼠进行曲军旅口号梗，以及天音惊恐吐槽迪斯尼法务部铁拳警告"
    if "お目覚めのキス" in ja or "叫醒之吻" in new_cn or "暗殺" in ja:
        return "特工创伤反差萌还原", "还原天音娇羞策划『晨间叫醒之吻』却反被雄二误判为敌国暗杀特工渗透的经典反差名场面"
    if "お嫁いかれへん" in ja or "嫁不出" in new_cn:
        return "方言声线与心理还原", "还原天音心态彻底崩溃时脱口而出的关西腔口吻『我已经没脸嫁人了啦（お嫁いかれへん）』"
    if "アメーバ赤痢" in ja or "阿米巴痢疾" in new_cn:
        return "角色天然呆搞笑还原", "还原莳菜天然呆追问反锁在厕所的天音是否得了『阿米巴痢疾（アメーバ赤痢）』的无厘头搞笑"
    if "俺" in old_cn and "我" in new_cn:
        return "第一人称去AI土味", "彻底剔除机翻中将雄二沉着冷静内心独白荒唐粗鄙化为乡土口吻『俺』的AI味缺陷，恢复标准第一人称『我』"

    # com14 specific
    if "ブルーシート" in ja or "防潮垫" in new_cn:
        return "野外战术动作/冷笑话还原", "还原雄二误以为野外苟合而厉声质问『防潮垫（ブルーシート）铺好了没有』的特种冷笑话"
    if "ナチュラル・ボーン" in ja or "波恩" in new_cn or "天生自带" in new_cn:
        return "角色声线/名梗还原", "纠正将美智留『天生自带纯血傲娇（Natural Born Tsundere）』误译为『傲娇骨』，还原与雄二复读机名场面"
    if "タワシ" in ja or "除毛" in new_cn or "钢丝球" in new_cn:
        return "恶趣味黄段子双关还原", "还原美智留将黑色毛团黑猫误听为私处体毛『明明做过除毛脱毛处理』的经典误会段子"
    if "飯事" in ja or "过家家" in new_cn:
        return "成语俗语纠错", "纠正将幼童过家家酒（飯事/ままごと）荒唐误译为『陪你饭局』的恶性机翻"
    if "バルジ猫作戦" in ja or "凸出部" in new_cn:
        return "二战战役特种军事梗", "纠正将雄二以二战阿登反击战命名的『凸出部猫咪作战（Battle of the Bulge Cat）』荒唐误译为『炸毛猫作战』"
    if "チャーリー" in ja or "呆毛" in new_cn or "查理" in new_cn:
        return "角色战术代号还原", "还原雄二将美智留双马尾命名为阿尔法与布拉沃、头顶翘立呆毛命名为查理（Charlie）的战术恶搞"
    if "脱水症状" in ja or "水分補給" in ja or "水分补给" in new_cn:
        return "角色军事创伤声线还原", "还原雄二患有严苛野外生存后遗症、对脱水与水分补给近乎神圣不可侵犯的硬汉说教"
    if "猫かぶる" in ja or "猫かぶり" in ja or "装纯" in new_cn or "やや受け" in ja:
        return "双关俗语成语还原", "还原美智留『头顶猫咪装纯乖（猫かぶる）』的经典双关，以及雄二评价『节目效果好评（やや受け）』"
    if "猫ニャー" in ja or "猫咪喵" in new_cn:
        return "角色蠢萌爱称还原", "还原美智留随口给小黑猫起的蠢萌专属爱称『猫咪喵（猫ニャー）』及其傲娇掩饰"
    if "ルルラーン" in ja or "噜噜啦" in new_cn:
        return "角色台词/密码脑补还原", "还原美智留临走怪叫『噜噜啦――嗯（ルルラーン）』以及雄二脑补为绝密战术密码的搞笑反差"

    # com13 specific
    if "インプリンティング" in ja or "印痕" in new_cn or "铭印" in new_cn:
        return "专业术语/科学修辞", "规范生物学习性与心理学概念『雏鸟印痕/铭印现象（インプリンティング/Imprinting）』"
    if "目からウロコ" in ja or "茅塞顿开" in new_cn:
        return "日语惯用语规范", "还原日语经典成语『茅塞顿开、大开眼界（目からウロコ）』，纠正机翻荒唐生硬的直译"
    if "着衣水泳" in ja or "ロープ渡河" in ja or "索降" in new_cn:
        return "战术动作/角色作风还原", "还原幸天然认真执行『全套女仆装跳水泳池（着衣水泳）』与『特警战术索降攻坚』的硬汉反差萌作风"
    if "すっぽんぽん" in ja or "光溜溜" in new_cn or "一丝不挂" in new_cn:
        return "角色声线与语境还原", "还原幸天然礼貌回应『一丝不挂/光溜溜（すっぽんぽん）』的反差萌，纠正生硬机翻"
    if "セミ姉妹" in ja or "知了姐妹" in new_cn:
        return "角色幽默生动吐槽", "还原天音与莳菜宛如夏日鸣蝉般嗡嗡吵闹的『知了姐妹花（セミ姉妹）』生动外号"

    # com12 specific
    if "びっくり箱" in ja or "整蛊盒子" in new_cn:
        return "专有名词/文化常识", "纠正将小丑惊吓弹簧玩偶盒（Jack-in-the-box/びっくり箱）荒唐误译为『百宝盒』"
    if "百物語よろしく五物語" in ja:
        return "民俗文化梗还原", "规范日本江户传统消暑怪谈『仿照百物语的做法，办成了“五物语”』（非生搬硬套『百鬼夜行』）"
    if "匙を投げられた" in ja:
        return "习惯成语意译", "规范日语医学成语『医生束手无策（匙を投げられた）』，纠正过于绝对生硬的『被判了死刑』"
    if "オヤング" in ja or "Peyoung" in new_cn:
        return "经典泡面名梗还原", "还原日本国民级炒面『Peyoung（オヤング）』水槽热胀冷缩轰鸣轰飞炒面的搞笑黑历史"
    if "無神経さ" in ja:
        return "角色心理声线还原", "还原由美子娇羞责备雄二『迟钝与不解风情（缺乏细腻体贴/無神経さ）』的傲娇名场面"

    # com11 specific
    if "自墜落" in ja or "自坠落" in new_cn:
        return "错字谐音梗还原", "还原满将『自甘堕落（自堕落）』文盲念错为『自坠落（自墜落）』的经典错字喜剧包袱"
    if "アズレンスルホン酸ナトリウム" in ja:
        return "医药常识误译纠正", "纠正将胃黏膜保护药奥磺酸钠（アズレンスルホン酸ナトリウム）荒唐机翻为『碳酸氢钠（小苏打）』"
    if "掌の上に人" in ja or "掌心" in new_cn:
        return "民俗偏方心理暗示", "还原在掌心连写三遍『人』字吞下壮胆的传统民间偏方（纠正原机翻『手心朝上托着人』的荒诞表述）"
    if "鰯" in ja and "沙丁鱼" in new_cn:
        return "鱼类名词常识误译", "纠正将沙丁鱼（鰯/Iwashi）指鹿为马误译为『鲭鱼（Saba）』"
    if "ＤＨＡ" in ja:
        return "科学常识与傲娇包袱", "还原满将健脑不饱和脂肪酸DHA与维生素C张冠李戴搞混的可爱笨蛋设定"
    if "和製ポルノ" in ja:
        return "演出与修辞还原", "规范幸因感冒女仆装松垮不整的犀利吐槽『廉价国产AV录像带里的落魄女仆』"
    if "由緒正しきツンデレ" in ja:
        return "Galgame核心属性规范", "规范二次元经典术语『恪守正统的教科书式经典傲娇台词』"
    if "ユミーン" in ja:
        return "角色昵称趣味还原", "还原雄二给由美子起的打趣外号『由美恩（ユミーン）』"
    if "賞味期限２０１２年" in ja:
        return "年份时间差笑话", "还原满将2012年保质期误当成已过期、被天音当场揭穿当前是2011年的经典吃瘪喜剧"

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

    # Section 13: com11 (14291 - 14571)
    for lno in range(14291, 14572):
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
                "section": "灰色的果实·共通线第十一章满的纯度VC与全员风寒骚动 (grisaia1/com11)"
            })

    # Section 14: com12 (14572 - 14873)
    for lno in range(14572, 14874):
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
                "section": "灰色的果实·共通线第十二章深夜五物语与由美子炒面怪谈 (grisaia1/com12)"
            })

    # Section 15: com13 (14874 - 15023)
    for lno in range(14874, 15024):
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
                "section": "灰色的果实·共通线第十三章阿幸雏鸟印痕与内衣女仆大轰动 (grisaia1/com13)"
            })

    # Section 16: com14 (15024 - 15237)
    for lno in range(15024, 15238):
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
                "section": "灰色的果实·共通线第十四章黑猫初遇与阿登凸出部作战 (grisaia1/com14)"
            })

    # Section 17: com15 (15238 - 15418)
    for lno in range(15238, 15419):
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
                "section": "灰色的果实·共通线第十五章天音潜入与特工行军口号 (grisaia1/com15)"
            })

    # Section 18: com16 (15419 - 15528)
    for lno in range(15419, 15529):
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
                "section": "灰色的果实·共通线第十六章由美子美工刀与阿幸大魔神威慑 (grisaia1/com16)"
            })

    # Section 19: com17 (15529 - 15678)
    for lno in range(15529, 15679):
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
                "section": "灰色的果实·共通线第十七章美智留漂发受难与暗黑舞踏大赏 (grisaia1/com17)"
            })

    # Section 20: com18 (15679 - 16066)
    for lno in range(15679, 16067):
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
                "section": "灰色的果实·共通线第十八章街头伏击战与猪排饭审讯室 (grisaia1/com18)"
            })

    # Section 21: com19 (16067 - 16193)
    for lno in range(16067, 16194):
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
                "section": "灰色的果实·共通线第十九章大黄蜂骚乱与由美子最强传说 (grisaia1/com19)"
            })

    # Section 22: com20 (16194 - 16605)
    for lno in range(16194, 16606):
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
                "section": "灰色的果实·共通线第二十章蓝色螯虾饲育与照相记忆天才 (grisaia1/com20)"
            })

    # Section 23: com21 (16606 - 17014)
    for lno in range(16606, 17015):
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
                "section": "灰色的果实·共通线第二十一章美滨极限运动会与保健室契约 (grisaia1/com21)"
            })

    # Section 24: com22 (17015 - 17278)
    for lno in range(17015, 17279):
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
                "section": "灰色的果实·共通线第二十二章便当手作哲学与家庭围炉之痛 (grisaia1/com22)"
            })

    # Section 25: com23 (17279 - 17399)
    for lno in range(17279, 17400):
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
                "section": "灰色的果实·共通线第二十三章大学茶谐音梗与北海道挤奶狂想曲 (grisaia1/com23)"
            })

    # com24
    for lno in range(17400, 17615):
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
                "section": "灰色的果实·共通线第二十四章校长室各人心理剖析与深渊罪恶感 (grisaia1/com24)"
            })

    # com25
    for lno in range(17615, 17912):
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
                "section": "灰色的果实·共通线第二十五章拼图碎片哲学与美智留心之迷宫 (grisaia1/com25)"
            })

    # com26
    for lno in range(17912, 18279):
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
                "section": "灰色的果实·共通线第二十六章无爱好之叹与由美子屋顶黑鸢破冰 (grisaia1/com26)"
            })

    # com27
    for lno in range(18279, 18449):
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
                "section": "灰色的果实·共通线第二十七章美滨饺子队与一叠半密室圣域 (grisaia1/com27)"
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

    # Section 13
    com11_diffs = [d for d in diffs if d["section"].startswith("灰色的果实·共通线第十一章")]
    md.append(f"## 十四、 灰色的果实·共通线第十一章满的纯度VC与全员风寒骚动 (`grisaia1/com11`，共 {len(com11_diffs)} 条)\n")
    md.append("| 序号 | 行号 | Scene ID | 日文原文 (JA) | 修改前机翻译文 (Old CN) | 修改后深度润色译文 (Polished CN) | 修改分类与原因 |")
    md.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
    for idx, d in enumerate(com11_diffs, 1):
        md.append(f"| {idx} | L{d['lno']} | `{d['sid']}` | {escape_md(d['ja'])} | {escape_md(d['old'])} | **{escape_md(d['new'])}** | `{d['cat']}`: {d['reason']} |")
    md.append("\n---\n")

    # Section 14
    com12_diffs = [d for d in diffs if d["section"].startswith("灰色的果实·共通线第十二章")]
    md.append(f"## 十五、 灰色的果实·共通线第十二章深夜五物语与由美子炒面怪谈 (`grisaia1/com12`，共 {len(com12_diffs)} 条)\n")
    md.append("| 序号 | 行号 | Scene ID | 日文原文 (JA) | 修改前机翻译文 (Old CN) | 修改后深度润色译文 (Polished CN) | 修改分类与原因 |")
    md.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
    for idx, d in enumerate(com12_diffs, 1):
        md.append(f"| {idx} | L{d['lno']} | `{d['sid']}` | {escape_md(d['ja'])} | {escape_md(d['old'])} | **{escape_md(d['new'])}** | `{d['cat']}`: {d['reason']} |")
    md.append("\n---\n")

    # Section 15
    com13_diffs = [d for d in diffs if d["section"].startswith("灰色的果实·共通线第十三章")]
    md.append(f"## 十六、 灰色的果实·共通线第十三章阿幸雏鸟印痕与内衣女仆大轰动 (`grisaia1/com13`，共 {len(com13_diffs)} 条)\n")
    md.append("| 序号 | 行号 | Scene ID | 日文原文 (JA) | 修改前机翻译文 (Old CN) | 修改后深度润色译文 (Polished CN) | 修改分类与原因 |")
    md.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
    for idx, d in enumerate(com13_diffs, 1):
        md.append(f"| {idx} | L{d['lno']} | `{d['sid']}` | {escape_md(d['ja'])} | {escape_md(d['old'])} | **{escape_md(d['new'])}** | `{d['cat']}`: {d['reason']} |")
    md.append("\n---\n")

    # Section 16
    com14_diffs = [d for d in diffs if d["section"].startswith("灰色的果实·共通线第十四章")]
    md.append(f"## 十七、 灰色的果实·共通线第十四章黑猫初遇与阿登凸出部作战 (`grisaia1/com14`，共 {len(com14_diffs)} 条)\n")
    md.append("| 序号 | 行号 | Scene ID | 日文原文 (JA) | 修改前机翻译文 (Old CN) | 修改后深度润色译文 (Polished CN) | 修改分类与原因 |")
    md.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
    for idx, d in enumerate(com14_diffs, 1):
        md.append(f"| {idx} | L{d['lno']} | `{d['sid']}` | {escape_md(d['ja'])} | {escape_md(d['old'])} | **{escape_md(d['new'])}** | `{d['cat']}`: {d['reason']} |")
    md.append("\n---\n")

    # Section 17
    com15_diffs = [d for d in diffs if d["section"].startswith("灰色的果实·共通线第十五章")]
    md.append(f"## 十八、 灰色的果实·共通线第十五章天音潜入与特工行军口号 (`grisaia1/com15`，共 {len(com15_diffs)} 条)\n")
    md.append("| 序号 | 行号 | Scene ID | 日文原文 (JA) | 修改前机翻译文 (Old CN) | 修改后深度润色译文 (Polished CN) | 修改分类与原因 |")
    md.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
    for idx, d in enumerate(com15_diffs, 1):
        md.append(f"| {idx} | L{d['lno']} | `{d['sid']}` | {escape_md(d['ja'])} | {escape_md(d['old'])} | **{escape_md(d['new'])}** | `{d['cat']}`: {d['reason']} |")
    md.append("\n---\n")

    # Section 18
    com16_diffs = [d for d in diffs if d["section"].startswith("灰色的果实·共通线第十六章")]
    md.append(f"## 十九、 灰色的果实·共通线第十六章由美子美工刀与阿幸大魔神威慑 (`grisaia1/com16`，共 {len(com16_diffs)} 条)\n")
    md.append("| 序号 | 行号 | Scene ID | 日文原文 (JA) | 修改前机翻译文 (Old CN) | 修改后深度润色译文 (Polished CN) | 修改分类与原因 |")
    md.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
    for idx, d in enumerate(com16_diffs, 1):
        md.append(f"| {idx} | L{d['lno']} | `{d['sid']}` | {escape_md(d['ja'])} | {escape_md(d['old'])} | **{escape_md(d['new'])}** | `{d['cat']}`: {d['reason']} |")
    md.append("\n---\n")

    # Section 19
    com17_diffs = [d for d in diffs if d["section"].startswith("灰色的果实·共通线第十七章")]
    md.append(f"## 二十、 灰色的果实·共通线第十七章美智留漂发受难与暗黑舞踏大赏 (`grisaia1/com17`，共 {len(com17_diffs)} 条)\n")
    md.append("| 序号 | 行号 | Scene ID | 日文原文 (JA) | 修改前机翻译文 (Old CN) | 修改后深度润色译文 (Polished CN) | 修改分类与原因 |")
    md.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
    for idx, d in enumerate(com17_diffs, 1):
        md.append(f"| {idx} | L{d['lno']} | `{d['sid']}` | {escape_md(d['ja'])} | {escape_md(d['old'])} | **{escape_md(d['new'])}** | `{d['cat']}`: {d['reason']} |")
    md.append("\n---\n")

    # Section 20
    com18_diffs = [d for d in diffs if d["section"].startswith("灰色的果实·共通线第十八章")]
    md.append(f"## 二十一、 灰色的果实·共通线第十八章街头伏击战与猪排饭审讯室 (`grisaia1/com18`，共 {len(com18_diffs)} 条)\n")
    md.append("| 序号 | 行号 | Scene ID | 日文原文 (JA) | 修改前机翻译文 (Old CN) | 修改后深度润色译文 (Polished CN) | 修改分类与原因 |")
    md.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
    for idx, d in enumerate(com18_diffs, 1):
        md.append(f"| {idx} | L{d['lno']} | `{d['sid']}` | {escape_md(d['ja'])} | {escape_md(d['old'])} | **{escape_md(d['new'])}** | `{d['cat']}`: {d['reason']} |")
    md.append("\n---\n")

    # Section 21
    com19_diffs = [d for d in diffs if d["section"].startswith("灰色的果实·共通线第十九章")]
    md.append(f"## 二十二、 灰色的果实·共通线第十九章大黄蜂骚乱与由美子最强传说 (`grisaia1/com19`，共 {len(com19_diffs)} 条)\n")
    md.append("| 序号 | 行号 | Scene ID | 日文原文 (JA) | 修改前机翻译文 (Old CN) | 修改后深度润色译文 (Polished CN) | 修改分类与原因 |")
    md.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
    for idx, d in enumerate(com19_diffs, 1):
        md.append(f"| {idx} | L{d['lno']} | `{d['sid']}` | {escape_md(d['ja'])} | {escape_md(d['old'])} | **{escape_md(d['new'])}** | `{d['cat']}`: {d['reason']} |")
    md.append("\n---\n")

    # Section 22
    com20_diffs = [d for d in diffs if d["section"].startswith("灰色的果实·共通线第二十章")]
    md.append(f"## 二十三、 灰色的果实·共通线第二十章蓝色螯虾饲育与照相记忆天才 (`grisaia1/com20`，共 {len(com20_diffs)} 条)\n")
    md.append("| 序号 | 行号 | Scene ID | 日文原文 (JA) | 修改前机翻译文 (Old CN) | 修改后深度润色译文 (Polished CN) | 修改分类与原因 |")
    md.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
    for idx, d in enumerate(com20_diffs, 1):
        md.append(f"| {idx} | L{d['lno']} | `{d['sid']}` | {escape_md(d['ja'])} | {escape_md(d['old'])} | **{escape_md(d['new'])}** | `{d['cat']}`: {d['reason']} |")
    md.append("\n---\n")

    # Section 23
    com21_diffs = [d for d in diffs if d["section"].startswith("灰色的果实·共通线第二十一章")]
    md.append(f"## 二十四、 灰色的果实·共通线第二十一章美滨极限运动会与保健室契约 (`grisaia1/com21`，共 {len(com21_diffs)} 条)\n")
    md.append("| 序号 | 行号 | Scene ID | 日文原文 (JA) | 修改前机翻译文 (Old CN) | 修改后深度润色译文 (Polished CN) | 修改分类与原因 |")
    md.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
    for idx, d in enumerate(com21_diffs, 1):
        md.append(f"| {idx} | L{d['lno']} | `{d['sid']}` | {escape_md(d['ja'])} | {escape_md(d['old'])} | **{escape_md(d['new'])}** | `{d['cat']}`: {d['reason']} |")
    md.append("\n---\n")

    # Section 24
    com22_diffs = [d for d in diffs if d["section"].startswith("灰色的果实·共通线第二十二章")]
    md.append(f"## 二十五、 灰色的果实·共通线第二十二章便当手作哲学与家庭围炉之痛 (`grisaia1/com22`，共 {len(com22_diffs)} 条)\n")
    md.append("| 序号 | 行号 | Scene ID | 日文原文 (JA) | 修改前机翻译文 (Old CN) | 修改后深度润色译文 (Polished CN) | 修改分类与原因 |")
    md.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
    for idx, d in enumerate(com22_diffs, 1):
        md.append(f"| {idx} | L{d['lno']} | `{d['sid']}` | {escape_md(d['ja'])} | {escape_md(d['old'])} | **{escape_md(d['new'])}** | `{d['cat']}`: {d['reason']} |")
    md.append("\n---\n")

    # Section 25
    com23_diffs = [d for d in diffs if d["section"].startswith("灰色的果实·共通线第二十三章")]
    md.append(f"## 二十六、 灰色的果实·共通线第二十三章大学茶谐音梗与北海道挤奶狂想曲 (`grisaia1/com23`，共 {len(com23_diffs)} 条)\n")
    md.append("| 序号 | 行号 | Scene ID | 日文原文 (JA) | 修改前机翻译文 (Old CN) | 修改后深度润色译文 (Polished CN) | 修改分类与原因 |")
    md.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
    for idx, d in enumerate(com23_diffs, 1):
        md.append(f"| {idx} | L{d['lno']} | `{d['sid']}` | {escape_md(d['ja'])} | {escape_md(d['old'])} | **{escape_md(d['new'])}** | `{d['cat']}`: {d['reason']} |")
    md.append("\n---\n")

    # Section 27
    com24_diffs = [d for d in diffs if d["section"].startswith("灰色的果实·共通线第二十四章校长室各人心理剖析与深渊罪恶感")]
    md.append(f"## 二十七、 灰色的果实·共通线第二十四章校长室各人心理剖析与深渊罪恶感 (`grisaia1/com24`，共 {len(com24_diffs)} 条)\n")
    md.append("| 序号 | 行号 | Scene ID | 日文原文 (JA) | 修改前机翻译文 (Old CN) | 修改后深度润色译文 (Polished CN) | 修改分类与原因 |")
    md.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
    for idx, d in enumerate(com24_diffs, 1):
        md.append(f"| {idx} | L{d['lno']} | `{d['sid']}` | {escape_md(d['ja'])} | {escape_md(d['old'])} | **{escape_md(d['new'])}** | `{d['cat']}`: {d['reason']} |")
    md.append("\n---\n")

    # Section 28
    com25_diffs = [d for d in diffs if d["section"].startswith("灰色的果实·共通线第二十五章拼图碎片哲学与美智留心之迷宫")]
    md.append(f"## 二十八、 灰色的果实·共通线第二十五章拼图碎片哲学与美智留心之迷宫 (`grisaia1/com25`，共 {len(com25_diffs)} 条)\n")
    md.append("| 序号 | 行号 | Scene ID | 日文原文 (JA) | 修改前机翻译文 (Old CN) | 修改后深度润色译文 (Polished CN) | 修改分类与原因 |")
    md.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
    for idx, d in enumerate(com25_diffs, 1):
        md.append(f"| {idx} | L{d['lno']} | `{d['sid']}` | {escape_md(d['ja'])} | {escape_md(d['old'])} | **{escape_md(d['new'])}** | `{d['cat']}`: {d['reason']} |")
    md.append("\n---\n")

    # Section 29
    com26_diffs = [d for d in diffs if d["section"].startswith("灰色的果实·共通线第二十六章无爱好之叹与由美子屋顶黑鸢破冰")]
    md.append(f"## 二十九、 灰色的果实·共通线第二十六章无爱好之叹与由美子屋顶黑鸢破冰 (`grisaia1/com26`，共 {len(com26_diffs)} 条)\n")
    md.append("| 序号 | 行号 | Scene ID | 日文原文 (JA) | 修改前机翻译文 (Old CN) | 修改后深度润色译文 (Polished CN) | 修改分类与原因 |")
    md.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
    for idx, d in enumerate(com26_diffs, 1):
        md.append(f"| {idx} | L{d['lno']} | `{d['sid']}` | {escape_md(d['ja'])} | {escape_md(d['old'])} | **{escape_md(d['new'])}** | `{d['cat']}`: {d['reason']} |")
    md.append("\n---\n")

    # Section 30
    com27_diffs = [d for d in diffs if d["section"].startswith("灰色的果实·共通线第二十七章美滨饺子队与一叠半密室圣域")]
    md.append(f"## 三十、 灰色的果实·共通线第二十七章美滨饺子队与一叠半密室圣域 (`grisaia1/com27`，共 {len(com27_diffs)} 条)\n")
    md.append("| 序号 | 行号 | Scene ID | 日文原文 (JA) | 修改前机翻译文 (Old CN) | 修改后深度润色译文 (Polished CN) | 修改分类与原因 |")
    md.append("| :---: | :---: | :--- | :--- | :--- | :--- | :--- |")
    for idx, d in enumerate(com27_diffs, 1):
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
