import os
import sys
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()

def wrap_text(draw, text, font, max_width):
    lines = []
    paragraphs = text.split('\n')
    for p in paragraphs:
        if not p.strip():
            lines.append('')
            continue
        words = p.split(' ')
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            bbox = font.getbbox(test_line)
            w = bbox[2] - bbox[0]
            if w <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    lines.append(word)
        if current_line:
            lines.append(' '.join(current_line))
    return lines

def draw_news_image(output_path):
    width, height = 1024, 1024
    img = Image.new("RGB", (width, height), color="#0E131F")
    draw = ImageDraw.Draw(img)

    # Fonts
    font_masthead = get_font(38, bold=True)
    font_subdate = get_font(13, bold=True)
    font_sec_header = get_font(11, bold=True)
    font_lead_title = get_font(24, bold=True)
    font_lead_body = get_font(14, bold=False)
    font_card_title = get_font(16, bold=True)
    font_card_body = get_font(12, bold=False)

    # Colors
    bg_card = "#161D2D"
    border_color = "#2A3650"
    accent_nvidia = "#00E676"
    accent_hormuz = "#FF9100"
    accent_russia = "#29B6F6"
    accent_icj = "#AB47BC"
    accent_grok = "#EF5350"
    text_white = "#FFFFFF"
    text_gray = "#A0ABBE"

    # --- TOP MASTHEAD ---
    draw.rectangle([0, 0, width, 115], fill="#090D16")
    draw.line([0, 115, width, 115], fill="#1E293B", width=3)

    title_text = "THE GLOBAL CHRONICLE"
    tb = font_masthead.getbbox(title_text)
    tw = tb[2] - tb[0]
    draw.text(((width - tw) // 2, 18), title_text, font=font_masthead, fill=text_white)

    subdate_text = "TUESDAY, 24 NOVEMBER 2026  |  WORLD NEWS SPECIAL EDITION  |  VERIFIED GLOBAL REPORTING"
    sb = font_subdate.getbbox(subdate_text)
    sw = sb[2] - sb[0]
    draw.text(((width - sw) // 2, 72), subdate_text, font=font_subdate, fill=accent_nvidia)

    # --- LAYOUT GRID ---
    margin = 16
    top_y = 132
    avail_w = width - (margin * 2)
    avail_h = height - top_y - margin

    left_w = 560
    right_w = avail_w - left_w - 16
    col2_x = margin + left_w + 16

    # --- LEFT COLUMN: LEAD STORY (Nvidia) ---
    lead_x = margin
    lead_y = top_y
    lead_h = avail_h
    
    draw.rectangle([lead_x, lead_y, lead_x + left_w, lead_y + lead_h], fill=bg_card, outline=border_color, width=2)
    draw.rectangle([lead_x, lead_y, lead_x + left_w, lead_y + 6], fill=accent_nvidia)

    pad = 22
    cur_y = lead_y + pad

    draw.text((lead_x + pad, cur_y), "TOP STORY • MARKETS & LEADERSHIP", font=font_sec_header, fill=accent_nvidia)
    cur_y += 24

    headline_lead = "NVIDIA BRINGS BACK JENSEN HUANG; STOCKS SURGE 31%"
    for line in wrap_text(draw, headline_lead, font_lead_title, left_w - (pad * 2)):
        draw.text((lead_x + pad, cur_y), line, font=font_lead_title, fill=text_white)
        cur_y += 32
    
    cur_y += 8

    chart_box = [lead_x + pad, cur_y, lead_x + left_w - pad, cur_y + 155]
    draw.rectangle(chart_box, fill="#0A0E17", outline=border_color, width=1)
    
    points = [
        (chart_box[0] + 20, chart_box[3] - 25),
        (chart_box[0] + 90, chart_box[3] - 40),
        (chart_box[0] + 160, chart_box[3] - 55),
        (chart_box[0] + 230, chart_box[3] - 45),
        (chart_box[0] + 300, chart_box[3] - 105),
        (chart_box[0] + 380, chart_box[3] - 125),
        (chart_box[0] + 470, chart_box[3] - 135),
    ]
    for i in range(len(points)-1):
        draw.line([points[i], points[i+1]], fill=accent_nvidia, width=4)
    
    draw.text((chart_box[0] + 15, chart_box[1] + 12), "NVIDIA SHARES +31%  |  NASDAQ +6.5%  |  +$900B VALUE", font=font_sec_header, fill=accent_nvidia)
    draw.text((chart_box[0] + 15, chart_box[1] + 32), "SEC Investigating Accounting Irregularities", font=font_sec_header, fill=text_gray)
    
    cur_y += 175

    body_lead = (
        "Nvidia's board unanimously reinstated founder Jensen Huang as CEO on Monday, "
        "23 November, following personal persuasion by Donald Trump. Nvidia shares surged "
        "31% in a historic single-day move, adding over $900 billion in market value, while "
        "the Nasdaq jumped 6.5% for its best session in over a year.\n\n"
        "Simultaneously, Reuters confirmed that SEC enforcement staff are investigating "
        "potential accounting irregularities at Nvidia, casting a complex regulatory shadow "
        "over the record-breaking market rally."
    )
    for line in wrap_text(draw, body_lead, font_lead_body, left_w - (pad * 2)):
        if line == "":
            cur_y += 10
            continue
        draw.text((lead_x + pad, cur_y), line, font=font_lead_body, fill=text_gray)
        cur_y += 20


    # --- RIGHT COLUMN: 4 SMALLER STORIES ---
    stories = [
        {
            "cat": "MIDDLE EAST • GEOPOLITICS",
            "title": "MINES IN THE STRAIT: IRAN-US STANDOFF",
            "body": "Three oil tankers hit naval mines in the Strait of Hormuz; Iran refuses talks until 7 conditions are met. US Treasury sanctions 25+ Rahbar shadow entities; Vance & Rubio meet Qatar PM.",
            "accent": accent_hormuz
        },
        {
            "cat": "SPACE DEFENSE • RUSSIA & NATO",
            "title": "A BOMB IN ORBIT? RUSSIA NUCLEAR ALARM",
            "body": "Western intelligence warns Russia plans a nuclear satellite launch. NATO chief Mark Rutte vows defense; Medvedev warns of 'preventive nuclear attack' amid 25 airspace violations.",
            "accent": accent_russia
        },
        {
            "cat": "INTERNATIONAL LAW • REFUGEES",
            "title": "NATIONS BACK ICJ RULING ON MYANMAR",
            "body": "Nations back the ICJ ruling that Myanmar committed genocide against the Rohingya. Malaysia to return 6,800+ Myanmar nationals in December by ship and plane.",
            "accent": accent_icj
        },
        {
            "cat": "AI REGULATION • LEGAL ACTION",
            "title": "STATES SUE SPACEX OVER GROK IMAGES",
            "body": "Oregon and Virginia sue SpaceX and Elon Musk over AI-generated CSAM produced by the Grok chatbot in the first major state legal action against chatbot-generated imagery.",
            "accent": accent_grok
        }
    ]

    card_h = (avail_h - (12 * 3)) // 4
    cur_card_y = top_y

    for s in stories:
        draw.rectangle([col2_x, cur_card_y, col2_x + right_w, cur_card_y + card_h], fill=bg_card, outline=border_color, width=2)
        draw.rectangle([col2_x, cur_card_y, col2_x + 5, cur_card_y + card_h], fill=s["accent"])

        cpad_x = 18
        cpad_y = 12
        cx = col2_x + cpad_x
        cy = cur_card_y + cpad_y

        draw.text((cx, cy), s["cat"], font=font_sec_header, fill=s["accent"])
        cy += 16

        for line in wrap_text(draw, s["title"], font=font_card_title, max_width=right_w - cpad_x - 12):
            draw.text((cx, cy), line, font=font_card_title, fill=text_white)
            cy += 20

        cy += 2

        for line in wrap_text(draw, s["body"], font=font_card_body, max_width=right_w - cpad_x - 12):
            draw.text((cx, cy), line, font=font_card_body, fill=text_gray)
            cy += 16

        cur_card_y += card_h + 12

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    img.save(output_path, "PNG", optimize=True)
    print(f"Successfully generated news image at {output_path}")

if __name__ == "__main__":
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    out_path = os.path.join(out_dir, "entry.png")
    draw_news_image(out_path)
