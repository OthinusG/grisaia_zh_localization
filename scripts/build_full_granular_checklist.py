# -*- coding: utf-8 -*-
"""
Generate complete exhaustive task list where every task is <= 1000 lines.
"""

def generate_tasklist():
    with open('ALL_TEXT.txt', 'r', encoding='utf-8') as f:
        ja_lines = [l.strip() for l in f]
    with open('ALL_TEXT_cn.txt', 'r', encoding='utf-8') as f:
        cn_lines = [l.strip() for l in f]

    scenes = []
    current_scene = None
    start_lno = 1
    count = 0

    for idx, line in enumerate(ja_lines, 1):
        if '\t' in line:
            sid = line.split('\t')[0]
            scene = sid.split('#')[0]
        else:
            scene = current_scene if current_scene is not None else 'UNKNOWN'
        
        if scene != current_scene:
            if current_scene is not None:
                scenes.append((current_scene, start_lno, idx - 1, count))
            current_scene = scene
            start_lno = idx
            count = 1
        else:
            count += 1
            
    if current_scene is not None:
        scenes.append((current_scene, start_lno, len(ja_lines), count))

    # Known scene manual topic descriptions
    known_topics = {
        '_varstr': '系统菜单、章节名与标题系统性纠正',
        'grisaia1/ama_001': '天音线示范标杆与声线/幽默感确立',
        'grisaia1/com01': '雄二初入美滨、美工刀初战由美子',
        'grisaia1/com02': '宿舍首夜、户外饭盒煮饭教学、麻子教导与一姬回忆',
        'grisaia1/com03': '见死团子梗纠偏、万步计宠物游戏、莳菜小猫般粘人',
        'grisaia1/com04': '钓鳌虾小龙虾梗纠偏、圣母在上梗还原、莳菜依恋与姐妹相谈',
        'grisaia1/com05': '课堂日常与美滨五女个性展开',
        'grisaia1/com06': '幸的死脑筋女仆测试与忠诚命令执行',
        'grisaia1/com07': '天音早安攻势与美滨宿舍清晨互动',
        'grisaia1/com08': '满的假傲娇白给演练与金枪鱼罐头',
        'grisaia1/com09': '由美子图书馆暗影与深层警戒心',
        'grisaia1/com10': '雄二的日常侦查与学园结界',
        'grisaia1/com11': '莳菜下头荤段子与天台特工反侦察',
        'grisaia1/com12': '幸的极端家政与无厘头侍从',
        'grisaia1/com13': '满的柠檬汽水与笨蛋属性爆发',
        'grisaia1/com14': '由美子美工刀对峙与微小破冰',
        'grisaia1/com15': '天音的溺爱与关西腔护犊',
        'grisaia1/com16': '课堂数学与自习插科打诨',
        'grisaia1/com17': '午餐争夺战与小食堂漫才',
        'grisaia1/com18': '雄二身体检查与千鹤校长密谈',
        'grisaia1/com19': '幸的极端保洁与全校消毒',
        'grisaia1/com20': '海滩合宿提案与泳衣采购骚动',
        'grisaia1/com21': '海滩合宿启程、全员泳装登场与沙滩排球',
        'grisaia1/com22': '由美子防晒霜修罗场、雄二硬汉推油',
        'grisaia1/com23': '海边烧烤BBQ与满的烤焦惨剧',
        'grisaia1/com24': '试胆大会森林探险与由美子落单',
        'grisaia1/com25': '海边深夜谈心、雄二守夜与由美子月下心声',
        'grisaia1/com26': '合宿归来后夜祭、温泉洗浴修罗场',
        'grisaia1/com27': '学园祭提案与全员脑洞大会',
        'grisaia1/com28': '女仆咖啡厅策划、幸的女仆装大批发',
        'grisaia1/com29': '莳菜的恶搞看板与由美子的警戒',
        'grisaia1/com30': '学园祭开幕前夜、雄二安全防卫巡视',
        'grisaia1/com31': '学园祭迎宾开幕与外校骚动',
        'grisaia1/com32': '幸的完美迎宾服务与由美子的咖啡手艺',
        'grisaia1/com33': '莳菜的小狗装扮与满的舞台翻车',
        'grisaia1/com34': '学园祭收尾与后夜祭篝火',
        'grisaia1/com35': '体育祭备战、借物赛跑与全员狂奔',
        'grisaia1/com36': '体育祭借物赛跑修罗场、雄二借人惩罚',
        'grisaia1/com37': '家长参观日骚乱前奏',
        'grisaia1/com38': '家长日突发事件与千鹤校长出面',
        'grisaia1/com39': '雄二特工背景初露端倪、JB电话初现',
        'grisaia1/com40': '天台密报与美滨五女日常升温',
        'grisaia1/com41': '幸的极端家政训练与自制防盗报警装置',
        'grisaia1/com42': '莳菜的零食秘密基地与雄二投喂',
        'grisaia1/com43': '满的假洋娃娃身世与双马尾执念',
        'grisaia1/com44': '由美子与雄二图书室静默陪伴与默契',
        'grisaia1/com45': '天音大姐姐的深夜心事与沉重爱意',
        'grisaia1/com46': '共通线后半风暴前夕、全员羁绊深化',
        'grisaia1/com46b': '分支选择前奏、日常裂痕初显',
        'grisaia1/com47a': '各女主线前置分支探索与心理试探',
        'grisaia1/com47b': '共通线终局前夜准备与各自决断',
        'grisaia1/com48': '手机原始人红外交换与糖果窒息海姆立克急救、七千万支票买父世界为敌誓约',
        'grisaia1/com49': 'B级特勤日出保洁下水道歼敌、纸尿裤眼肌相声、阿斯顿马丁车门亲吻封口与天音初吻契约',
        'grisaia1/com50': '共通线各分支终结走向',
        'grisaia1/com51': '空尖弹与牛气管软骨恶搞、防波堤黑满现身与第一吻契约',
        'grisaia1/com52': '可丽饼店跟踪大作战与由美子吃相反差萌（里程碑一圆满收官）',
        'grisaia1/mak_001': '铝热剂炸门晨吻修罗场、全班宣布父女契约、JB天台密谈与放学鲷鱼烧约会',
        'grisaia1/mak_002': '第二会议室蒙面匿名审判大会',
    }

    def get_summary(s, e):
        for i in range(s - 1, min(e, s + 15)):
            l = cn_lines[i]
            t = l.split('\t')[1] if '\t' in l else l
            if t and not t.startswith('@') and not t.startswith('★'):
                clean = t.replace('――', '').replace('…', '').strip()
                if len(clean) >= 6:
                    return clean[:30]
        for i in range(s - 1, min(e, s + 15)):
            l = cn_lines[i]
            t = l.split('\t')[1] if '\t' in l else l
            if t:
                clean = t.replace('――', '').replace('…', '').strip()
                if len(clean) >= 4:
                    return clean[:30]
        return '剧本剧情推进'

    # Build tasks strictly <= 1000 lines
    raw_tasks = []
    for name, start, end, lines in scenes:
        if lines <= 1000:
            topic = known_topics.get(name, get_summary(start, end))
            raw_tasks.append({
                'name': name,
                'start': start,
                'end': end,
                'lines': lines,
                'topic': topic,
                'part': None
            })
        else:
            num_parts = (lines + 999) // 1000
            part_size = (lines + num_parts - 1) // num_parts
            cur = start
            for p in range(1, num_parts + 1):
                p_end = min(end, cur + part_size - 1)
                p_lines = p_end - cur + 1
                base_topic = known_topics.get(name, get_summary(cur, p_end))
                raw_tasks.append({
                    'name': name,
                    'start': cur,
                    'end': p_end,
                    'lines': p_lines,
                    'topic': f"{base_topic} (Part {p}/{num_parts})",
                    'part': p
                })
                cur = p_end + 1

    print(f"Generated {len(raw_tasks)} fine-grained subtasks.")
    return raw_tasks

if __name__ == '__main__':
    generate_tasklist()
