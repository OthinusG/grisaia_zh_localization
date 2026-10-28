import json

tail_polished = {
    0: "@天音@「没事啦…不过是长了点霉斑而已嘛…」",
    3: "我用筷子从滚烫的热水中捞起纯棉手巾，耐心地等待它稍稍冷却至不会烫伤皮肉的适度温热，随后用力将其拧干。",
    4: "@广冈@「…全身都…奇痒难忍…我快要被逼疯了…好难受…」",
    6: "@天音@「稍微忍耐一下下哦…我马上帮你擦洗干净」",
    9: "我用温热湿润的热毛巾小心翼翼地擦拭着广冈学姐的躯体。虽然附着在皮肤表面的白霉被一点点擦拭剥离，可在霉斑覆盖的下方，却暴露出无数因指甲反复疯狂抓挠而肿胀溃烂的猩红痕迹，宛如一条条可怖的蚯蚓般蜿蜒纵横。",
    10: "@天音@「不是千叮咛万嘱咐过绝对不许伸手抓挠的嘛…」",
    13: "抓挠得越厉害，霉菌孢子便越是以溃烂的创口为温床向四周疯狂扩散蔓延。",
    14: "@广冈@「…对不起…但我实在…无论如何…也忍不住这股钻心的奇痒…」",
    17: "大面积神经性奇痒所带来的肉体折磨，远比想象中更加难以忍受。任凭清醒时如何告诫自己绝对不能抓挠，一旦在睡梦中失去意识，双手便会本能地疯狂撕抓皮肉。",
    19: "为此，全员曾一度将彻底养成抓挠恶习的广冈学姐的双手严密捆绑束缚起来，企图剥夺她在睡眠中抓挠的可能，可谁知在半夜陷入极端奇痒的折磨中，她竟痛苦地发出凄厉惨叫疯狂扭动身躯――",
    20: "甚至不惜将自己娇嫩的皮肉在坚硬粗糙的泥地上拼命摩擦止痒，喉咙深处一声声凄厉绝望地哀嚎着『救救我、求求你们救救我』。",
    21: "@广冈@「…谢谢你周防同学…真的好舒服…」",
    24: "只要有人用热毛巾帮她擦拭身体，剧烈的奇痒便会稍稍平息退去，更重要的是那种温热的触感能带给她莫大的慰藉。",
    26: "但即便如此，这种来之不易的舒适安宁也仅仅只能维系短短一两个小时而已。",
    28: "一旦再次蜷缩进睡袋之中，体温重新上升，钻心的奇痒便又会卷土重来。而每次都要反反复复烧水替她擦洗，确实是极费心力的繁重苦工。",
    29: "@广冈@「…真的很对不起…总是给你添这么大的麻烦…实在对不起…反正我…大概很快就会死去了…在那之前…对不起…」",
    31: "@天音@「没事的啦，不许你胡思乱想说这种丧气话。替你擦拭身体这点小事，只要你想我随时都会帮你做的，所以打起精神来嘛」",
    34: "反倒不如说，面对她的苦难，自己唯一能为她做到的仅仅只有擦拭身体这种微不足道的末节，这份无力感才让我感到无比心酸与悲哀。",
    35: "@广冈@「…周防同学…我…这份天大的恩情…我将来一定会报答你的…」",
    37: "@天音@「嗯，我们可一言为定哦？所以为了履行诺言，学姐你无论如何也必须要活着回去才行，知道了吗？」",
    39: "@广冈@「……我…哪怕变成厉鬼下了地狱也绝对…永远不会忘记这份大恩大德的…好吗…？」",
    42: "话音未落，广冈学姐眼眶中的滚烫泪水宛如断线珍珠般扑簌簌滚落而下。",
    43: "@天音@「所以都说了，不要动不动就说这种不吉利的话啦。放心吧，你绝对不会死的」",
    46: "我伸出指尖，轻轻接住了顺着广冈学姐眼角滑落的那滴清澈泪珠，在失神茫然的无意识之中，将沾着泪水的手指悄然送进了自己的口中。",
    47: "广冈学姐的眼泪，尝起来依然是咸涩的…。",
    50: "那一刻，我心底深处竟然对她……产生了微末的艳羡。"
}

with open("ALL_TEXT.txt") as f_jp, open("ALL_TEXT_cn.txt") as f_cn:
    jp_lines = [l.rstrip("\r\n") for l in f_jp]
    cn_lines = [l.rstrip("\r\n") for l in f_cn]

start = 11021 - 1
end = 11071
slice_jp = jp_lines[start:end]
assert len(slice_jp) == 51

formatted_lines = []
for i in range(51):
    jp_l = slice_jp[i]
    sid = jp_l.split("\t")[0] if "\t" in jp_l else ""
    has_tab = "\t" in jp_l
    jp_txt = jp_l.split("\t")[1] if "\t" in jp_l else jp_l
    
    if not jp_txt.strip():
        text = ""
    else:
        assert i in tail_polished, f"Missing index {i}"
        text = tail_polished[i]
    
    # Check empty matching
    assert (jp_txt == "") == (text == ""), f"Mismatch at {i}: {repr(jp_txt)} vs {repr(text)}"
    
    if sid:
        if has_tab:
            formatted_lines.append(f"{sid}\t{text}")
        else:
            formatted_lines.append(sid)
    else:
        formatted_lines.append(text)

assert len(formatted_lines) == 51

# Patch into cn_lines
print(f"Index 11020 in orig: {cn_lines[11020][:40]}")
print(f"Index 11020 in patch: {formatted_lines[0][:40]}")
print(f"Index 11070 in orig: {cn_lines[11070][:40]}")
print(f"Index 11070 in patch: {formatted_lines[-1][:40]}")

cn_lines[start:end] = formatted_lines
assert len(cn_lines) == 110622

with open("ALL_TEXT_cn.txt", "w", encoding="utf-8") as f:
    for line in cn_lines:
        f.write(line + "\n")

print("Successfully patched ama_old_010 tail (51 lines)!")
