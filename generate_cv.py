import re, os
from fpdf import FPDF

BULLET = chr(183)
PHOTO_PATH = "/home/user/job-search.md/tanya_photo_cv.png"

def sanitize(text):
    text = text.replace('–', '-').replace('—', '-')
    text = text.replace('‘', chr(39)).replace('’', chr(39))
    text = text.replace('“', chr(34)).replace('”', chr(34))
    text = text.replace('…', '...')
    text = text.replace('·', chr(183))
    text = text.replace('\xe9', 'e').replace('\xe8', 'e').replace('\xea', 'e')
    text = text.replace('\xe0', 'a').replace('\xe2', 'a')
    return text.encode('latin-1', errors='replace').decode('latin-1')

def generate_pdf(cv_markdown, output_path, photo_path=PHOTO_PATH):
    class CV(FPDF):
        def header(self): pass
        def footer(self): pass

    pdf = CV(format="A4")
    pdf.set_margins(20, 15, 20)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=12)

    if photo_path and os.path.exists(photo_path):
        pdf.image(photo_path, x=163, y=10, w=28, h=28)

    in_header = True
    for line in cv_markdown.split("\n"):
        raw = line.strip()
        if not raw:
            if not in_header:
                pdf.ln(1.5)
            continue

        if raw.startswith("# "):
            name_parts = sanitize(raw[2:].strip()).upper().split()
            name_spaced = "   ".join(name_parts)
            pdf.set_font("Helvetica", "B", 22)
            pdf.set_text_color(0, 0, 0)
            pdf.set_y(12)
            pdf.set_x(20)
            pdf.cell(140, 10, name_spaced, ln=True, align="C")

        elif raw.startswith("## "):
            in_header = False
            text = sanitize(raw[3:].strip()).upper()
            if "EXPERIENCE" in text:
                pdf.ln(2)
                pdf.set_draw_color(0, 0, 0)
                pdf.line(20, pdf.get_y(), 190, pdf.get_y())
                pdf.ln(1.5)
                pdf.line(20, pdf.get_y(), 190, pdf.get_y())
                pdf.ln(3)
            else:
                pdf.ln(3)
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(0, 0, 0)
            pdf.set_x(20)
            pdf.cell(170, 6, text, ln=True)
            pdf.line(20, pdf.get_y(), 190, pdf.get_y())
            pdf.ln(2.5)

        elif raw.startswith("### "):
            text = sanitize(raw[4:].strip())
            pdf.ln(2)
            pdf.set_font("Helvetica", "B", 9.5)
            pdf.set_text_color(0, 0, 0)
            pdf.set_x(20)
            pdf.multi_cell(170, 5.5, text)

        elif raw == "---":
            if in_header:
                in_header = False
                pdf.line(20, pdf.get_y(), 190, pdf.get_y())
                pdf.ln(3)
            else:
                pdf.ln(1)
                pdf.line(20, pdf.get_y(), 190, pdf.get_y())
                pdf.ln(2)

        elif raw.startswith("- "):
            text = sanitize(re.sub(r'\*{1,2}(.+?)\*{1,2}', r'\1', raw[2:]))
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(30, 30, 30)
            pdf.set_x(20)
            pdf.cell(6, 5, BULLET, ln=False)
            pdf.set_x(26)
            pdf.multi_cell(164, 5, text, align="J")

        elif in_header and raw.startswith("**") and raw.endswith("**"):
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(0, 0, 0)
            pdf.set_x(20)
            pdf.cell(140, 5.5, sanitize(raw.strip("*")), ln=True, align="C")

        elif in_header:
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(50, 50, 50)
            pdf.set_x(20)
            pdf.multi_cell(140, 5, sanitize(re.sub(r'\*{1,2}(.+?)\*{1,2}', r'\1', raw)), align="C")

        elif raw.startswith("**") and raw.endswith("**"):
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(0, 0, 0)
            pdf.set_x(20)
            pdf.multi_cell(170, 5, sanitize(raw.strip("*")))

        elif "**" in raw:
            parts = re.split(r'(\*\*[^*]+\*\*)', raw)
            pdf.set_x(20)
            for part in parts:
                if part.startswith("**") and part.endswith("**"):
                    pdf.set_font("Helvetica", "B", 9)
                    pdf.set_text_color(0, 0, 0)
                    pdf.write(5, sanitize(part.strip("*")))
                else:
                    pdf.set_font("Helvetica", "", 9)
                    pdf.set_text_color(30, 30, 30)
                    pdf.write(5, sanitize(part))
            pdf.ln(5)

        elif raw.startswith("*") and raw.endswith("*") and not raw.startswith("**"):
            pdf.set_font("Helvetica", "I", 9)
            pdf.set_text_color(50, 50, 50)
            pdf.set_x(20)
            pdf.multi_cell(170, 5, sanitize(raw.strip("*")))

        else:
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(30, 30, 30)
            pdf.set_x(20)
            pdf.multi_cell(170, 5, sanitize(re.sub(r'\*{1,2}(.+?)\*{1,2}', r'\1', raw)), align="J")

    pdf.output(output_path)
    print("Done:", output_path)
