from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


W, H = 1242, 1656
ROOT = Path("/Users/lishihao/Documents/小红书/第十二篇/AI错题库工作流")
OUT = ROOT / "images"
OUT.mkdir(parents=True, exist_ok=True)

FONT_CJK = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_ALT = "/System/Library/Fonts/STHeiti Medium.ttc"

COLORS = {
    "bg": "#F4F0E8",
    "panel": "#FBF9F5",
    "text": "#2F2D29",
    "muted": "#6A655D",
    "sage": "#7D9185",
    "blue": "#8799AA",
    "sand": "#B1967A",
    "line": "#DDD6CD",
    "soft_green": "#E7EFE9",
    "soft_blue": "#EBF0F4",
    "soft_sand": "#F1E8DE",
}


def font(size: int, bold: bool = False):
    path = FONT_ALT if bold else FONT_CJK
    return ImageFont.truetype(path, size=size)


def wrap_text(draw, text, font_obj, max_width):
    lines = []
    for paragraph in text.split("\n"):
        if not paragraph:
            lines.append("")
            continue
        current = ""
        for ch in paragraph:
            test = current + ch
            if draw.textbbox((0, 0), test, font=font_obj)[2] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = ch
        if current:
            lines.append(current)
    return lines


def draw_multiline(draw, xy, text, font_obj, fill, max_width, line_gap=12):
    x, y = xy
    for line in wrap_text(draw, text, font_obj, max_width):
        draw.text((x, y), line, font=font_obj, fill=fill)
        y += font_obj.size + line_gap
    return y


def rounded(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def add_header(draw, page_no, title):
    rounded(draw, (72, 58, 1170, 146), 28, fill="#F8F4EE", outline=COLORS["line"], width=2)
    draw.text((102, 84), title, font=font(40, bold=True), fill=COLORS["text"])
    draw.text((1020, 86), f"{page_no:02d}/07", font=font(28), fill=COLORS["muted"])
    rounded(draw, (72, 168, 330, 216), 20, fill=COLORS["soft_green"])
    draw.text((96, 181), "Rishao的AI教研室", font=font(22), fill=COLORS["sage"])


def add_card(draw, box, title, lines, accent, text_size=29):
    x1, y1, x2, y2 = box
    rounded(draw, box, 34, fill=COLORS["panel"], outline=COLORS["line"], width=2)
    rounded(draw, (x1 + 22, y1 + 20, x1 + 192, y1 + 64), 18, fill=accent)
    draw.text((x1 + 40, y1 + 29), title, font=font(22, bold=True), fill="#FFFFFF")
    y = y1 + 92
    max_width = x2 - x1 - 74
    for line in lines:
        draw.ellipse((x1 + 34, y + 10, x1 + 46, y + 22), fill=accent)
        y = draw_multiline(
            draw,
            (x1 + 62, y),
            line,
            font(text_size),
            COLORS["text"],
            max_width,
            line_gap=10,
        ) + 18


def body_base():
    bg = Image.new("RGB", (W, H), COLORS["bg"])
    draw = ImageDraw.Draw(bg)
    draw.rectangle((0, 0, W, 264), fill="#EFE9E0")
    draw.rectangle((0, H - 110, W, H), fill="#F2ECE4")
    for x, y, r, fill in [
        (1065, 240, 172, COLORS["soft_green"]),
        (174, 1432, 216, "#EEE4D7"),
        (1002, 1220, 138, COLORS["soft_blue"]),
    ]:
        draw.ellipse((x - r, y - r, x + r, y + r), fill=fill)
    rounded(draw, (936, 108, 1152, 230), 30, fill="#F6F2EA", outline=COLORS["line"], width=2)
    draw.rectangle((968, 132, 1120, 144), fill="#D7D0C6")
    draw.rectangle((968, 158, 1120, 170), fill="#D7D0C6")
    draw.rectangle((968, 184, 1080, 196), fill="#D7D0C6")
    return bg


def cover_background():
    img = Image.new("RGB", (W, H), "#F5F1EA")
    draw = ImageDraw.Draw(img)
    for y in range(H):
        tone = int(245 - y * 18 / H)
        draw.line((0, y, W, y), fill=(tone, tone - 2, tone - 6))

    draw.rectangle((0, 1080, W, H), fill="#ECE6DD")
    rounded(draw, (86, 146, 1156, 1520), 54, fill=(249, 246, 240), outline=COLORS["line"], width=2)

    rounded(draw, (124, 1018, 610, 1458), 38, fill="#F6F1EA", outline=COLORS["line"], width=2)
    draw.rectangle((154, 1066, 578, 1090), fill="#D8D0C5")
    draw.rectangle((154, 1120, 546, 1142), fill="#D8D0C5")
    draw.rectangle((154, 1174, 522, 1196), fill="#D8D0C5")
    draw.rectangle((154, 1228, 490, 1250), fill="#D8D0C5")

    rounded(draw, (720, 1040, 1086, 1320), 32, fill="#EDF1F4", outline=COLORS["line"], width=2)
    rounded(draw, (756, 1080, 918, 1124), 18, fill=COLORS["blue"])
    rounded(draw, (756, 1154, 1028, 1198), 18, fill=COLORS["sage"])
    rounded(draw, (756, 1228, 966, 1272), 18, fill=COLORS["sand"])

    draw.ellipse((932, 188, 1108, 364), fill="#E8EFE8", outline=COLORS["line"])
    draw.ellipse((968, 224, 1072, 328), outline="#C9C1B7", width=6)
    draw.line((1072, 324, 1114, 364), fill="#C9C1B7", width=8)

    rounded(draw, (132, 236, 444, 292), 24, fill="#FFFFFF")
    draw.text((160, 248), "Rishao的AI教研室", font=font(26), fill=COLORS["sage"])
    return img


def make_cover():
    img = cover_background()
    draw = ImageDraw.Draw(img)
    rounded(draw, (124, 352, 1118, 944), 48, fill=(255, 255, 255), outline=(227, 219, 209), width=2)
    draw.text((178, 438), "AI帮我整理", font=font(104, bold=True), fill=COLORS["text"])
    draw.text((178, 592), "错题库", font=font(122, bold=True), fill=COLORS["text"])
    draw.text((184, 780), "周测后，先把错题", font=font(42), fill=COLORS["muted"])
    draw.text((184, 842), "变成可复用错因表", font=font(42), fill=COLORS["muted"])

    rounded(draw, (180, 972, 502, 1028), 24, fill=COLORS["soft_green"])
    draw.text((212, 986), "IGCSE理科老师工作流", font=font(27), fill=COLORS["sage"])
    rounded(draw, (528, 972, 754, 1028), 24, fill=COLORS["soft_blue"])
    draw.text((560, 986), "错题归类", font=font(28), fill=COLORS["blue"])
    rounded(draw, (780, 972, 978, 1028), 24, fill=COLORS["soft_sand"])
    draw.text((812, 986), "可复制", font=font(28), fill=COLORS["sand"])
    img.save(OUT / "01_封面.png", quality=95)


def make_problem():
    img = body_base()
    draw = ImageDraw.Draw(img)
    add_header(draw, 2, "最难的不是批改，是整理错题")
    add_card(
        draw,
        (78, 278, 1164, 844),
        "真实痛点",
        [
            "卷子改完了，错法却还是散在每一份答卷里。",
            "下次备课、重教、出变式题，还得重新翻一遍。",
            "真正耗时间的，是把零散错误整理成可复用错因表。",
        ],
        accent=COLORS["sage"],
    )
    add_card(
        draw,
        (78, 894, 1164, 1418),
        "为什么要先留下错因表",
        [
            "如果这一步没留下来，很多判断都会在下次重做。",
            "老师真正缺的不是分数，而是下一步能继续用的整理结构。",
        ],
        accent=COLORS["blue"],
    )
    img.save(OUT / "02_问题页.png", quality=95)


def make_traditional():
    img = body_base()
    draw = ImageDraw.Draw(img)
    add_header(draw, 3, "传统整理方式，为什么总在重复劳动")
    add_card(
        draw,
        (78, 278, 548, 1376),
        "以前做法",
        [
            "一边翻卷子一边记错法。",
            "再自己判断这些算不算同一类。",
            "手动给每一类起名字。",
            "最后再想下一节课怎么补。",
        ],
        accent=COLORS["sage"],
    )
    add_card(
        draw,
        (614, 278, 1164, 1376),
        "容易出现",
        [
            "同类错误没有合并。",
            "分类名字太散，下次看不懂。",
            "很难直接转成补救动作。",
            "每次小测都像重来一遍。",
        ],
        accent=COLORS["sand"],
    )
    img.save(OUT / "03_传统做法页.png", quality=95)


def make_ai_workflow():
    img = body_base()
    draw = ImageDraw.Draw(img)
    add_header(draw, 4, "我现在固定用这 4 步")
    steps = [
        ("01", "先做匿名化", "只保留题号、错法、标准答案和知识点，不上传原卷。"),
        ("02", "让 AI 先做归类", "先把零散错法合并成 3 到 5 类，不替老师下结论。"),
        ("03", "再补补救动作", "区分哪些适合重讲概念，哪些适合一步练习或 exit ticket。"),
        ("04", "老师审核定稿", "重点看分类有没有混、命名是否自然、动作能否直接进下一节课。"),
    ]
    y = 274
    for idx, title, desc in steps:
        rounded(draw, (90, y, 1152, y + 252), 36, fill=COLORS["panel"], outline=COLORS["line"], width=2)
        rounded(draw, (118, y + 34, 238, y + 98), 26, fill=COLORS["sage"])
        draw.text((146, y + 48), idx, font=font(34, bold=True), fill="#FFFFFF")
        draw.text((276, y + 46), title, font=font(40, bold=True), fill=COLORS["text"])
        draw_multiline(draw, (278, y + 114), desc, font(27), COLORS["muted"], 800, line_gap=10)
        y += 280
    rounded(draw, (90, 1424, 1152, 1530), 28, fill=COLORS["soft_green"])
    draw.text((126, 1452), "AI 负责整理结构，老师负责教学判断。", font=font(31), fill=COLORS["sage"])
    img.save(OUT / "04_AI做法页.png", quality=95)


def make_result():
    img = body_base()
    draw = ImageDraw.Draw(img)
    add_header(draw, 5, "一个 IGCSE Physics 案例")
    add_card(
        draw,
        (78, 278, 730, 1406),
        "案例事实",
        [
            "Year 11 IGCSE Physics。",
            "主题：series and parallel circuits。",
            "班里 18 人，抽取 11 条匿名化错法。",
            "最后整理成 4 类共性错因。",
        ],
        accent=COLORS["sage"],
    )
    add_card(
        draw,
        (760, 278, 1164, 1406),
        "结果",
        [
            "35-40 分钟 -> 10 分钟",
            "1 张错因表",
            "1 页重教顺序",
            "3 道变式题",
            "1 道 exit ticket",
        ],
        accent=COLORS["blue"],
        text_size=27,
    )
    img.save(OUT / "05_成果展示页.png", quality=95)


def make_prompt():
    img = body_base()
    draw = ImageDraw.Draw(img)
    add_header(draw, 6, "这段提示词可直接复制")
    rounded(draw, (78, 278, 1164, 1432), 38, fill="#FAF8F3", outline=COLORS["line"], width=2)
    prompt_text = (
        "角色：国际课程理科老师的教研助理\n"
        "输入：匿名化错题记录 + 标准答案 + 教师备注\n"
        "输出：错因分类 + 判断依据 + 补救动作\n"
        "限制：不虚构学生背景，不评价个人\n\n"
        "课程背景：\n"
        "Year 11 IGCSE Physics\n"
        "主题：series and parallel circuits\n\n"
        "匿名化错法：\n"
        "- 串联电流写成会逐段减小\n"
        "- 并联某支路电压写成总电压一半\n"
        "- 并联题套用串联电阻相加\n"
        "- 250 mA 直接当成 250 A\n\n"
        "要求：\n"
        "- 合并成 3-5 类错因\n"
        "- 给每类一个老师能直接看懂的名字\n"
        "- 标注可能原因和复核点\n"
        "- 区分适合重讲/练习/exit ticket"
    )
    draw_multiline(draw, (116, 326), prompt_text, font(27), COLORS["text"], 992, line_gap=11)
    rounded(draw, (108, 1452, 1132, 1530), 24, fill=COLORS["soft_sand"])
    draw.text((138, 1476), "先把输入整理干净，AI 才能把错因归得稳。", font=font(30), fill=COLORS["sand"])
    img.save(OUT / "06_提示词页.png", quality=95)


def make_interaction():
    img = body_base()
    draw = ImageDraw.Draw(img)
    add_header(draw, 7, "这套流程适合哪些场景")
    add_card(
        draw,
        (78, 278, 548, 1308),
        "适合",
        [
            "周测后整理共性错因。",
            "给下一节课准备重教重点。",
            "为变式题和家长反馈留底稿。",
        ],
        accent=COLORS["sage"],
    )
    add_card(
        draw,
        (614, 278, 1164, 1308),
        "不适合",
        [
            "直接上传原卷和学生身份信息。",
            "不审核就照单使用分类结果。",
            "让 AI 替老师判断学生水平。",
        ],
        accent=COLORS["sand"],
    )
    rounded(draw, (78, 1354, 1164, 1514), 34, fill=COLORS["soft_blue"], outline=COLORS["line"], width=2)
    draw.text((116, 1394), "你最卡的是归类、命名还是补救？", font=font(42, bold=True), fill=COLORS["text"])
    draw.text((118, 1454), "评论区告诉我，我继续拆下一步模板。", font=font(28), fill=COLORS["blue"])
    img.save(OUT / "07_互动页.png", quality=95)


def make_contact_sheet():
    files = [
        OUT / "01_封面.png",
        OUT / "02_问题页.png",
        OUT / "03_传统做法页.png",
        OUT / "04_AI做法页.png",
        OUT / "05_成果展示页.png",
        OUT / "06_提示词页.png",
        OUT / "07_互动页.png",
    ]
    thumbs = [Image.open(path).resize((310, 413)) for path in files]
    sheet = Image.new("RGB", (976, 1260), "#F3EEE6")
    for idx, thumb in enumerate(thumbs):
        x = 24 + (idx % 3) * 318
        y = 24 + (idx // 3) * 421
        sheet.paste(thumb, (x, y))
    sheet.save(ROOT / "preview_montage.png", quality=92)


def main():
    make_cover()
    make_problem()
    make_traditional()
    make_ai_workflow()
    make_result()
    make_prompt()
    make_interaction()
    make_contact_sheet()


if __name__ == "__main__":
    main()
