import re, os
from fpdf import FPDF

PHOTO_PATH = "/home/user/job-search.md/tanya_photo_cv.png"
BULLET = chr(183)

def sanitize(text):
    text = text.replace('–', '-').replace('—', '-')
    text = text.replace(''', chr(39)).replace(''', chr(39))
    text = text.replace('"', chr(34)).replace('"', chr(34))
    text = text.replace('…', '...')
    text = text.replace('é', 'e').replace('è', 'e').replace('ê', 'e')
    text = text.replace('à', 'a').replace('â', 'a')
    return text.encode('latin-1', errors='replace').decode('latin-1')

def thick_line(pdf, L=22):
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.7)
    pdf.line(L, pdf.get_y(), 210 - L, pdf.get_y())
    pdf.set_line_width(0.2)

def thin_line(pdf, L=22):
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.3)
    pdf.line(L, pdf.get_y(), 210 - L, pdf.get_y())
    pdf.set_line_width(0.2)

def generate_pdf(cv_markdown, output_path, photo_path=PHOTO_PATH):
    L = 22
    CW = 210 - 2 * L  # 166mm content width

    class CV(FPDF):
        def header(self): pass
        def footer(self): pass

    pdf = CV(format="A4")
    pdf.set_margins(L, 15, L)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=10)

    if photo_path and os.path.exists(photo_path):
        pdf.image(photo_path, x=210 - L - 30, y=12, w=30, h=30)

    in_header = True
    first_section = True
    prev_was_rule = False  # True after a --- so ## handler skips its own transition

    for line in cv_markdown.strip().split("\n"):
        raw = line.strip()

        # blank line
        if not raw:
            if not in_header:
                pdf.ln(1.5)
            continue

        # # NAME
        if raw.startswith("# "):
            name = sanitize(raw[2:].strip()).upper()
            pdf.set_font("Times", "B", 28)
            pdf.set_char_spacing(3)
            pdf.set_text_color(0, 0, 0)
            pdf.set_xy(L, 15)
            pdf.cell(CW - 32, 12, name, align="C")
            pdf.set_char_spacing(0)
            pdf.ln(12)
            prev_was_rule = False

        # ## SECTION HEADER
        elif raw.startswith("## "):
            in_header = False
            text = sanitize(raw[3:].strip()).upper()

            if text == "CORE COMPETENCIES":
                pdf.ln(3)
                pdf.set_font("Helvetica", "B", 10)
                pdf.set_text_color(0, 0, 0)
                pdf.set_x(L)
                pdf.cell(CW, 5.5, text, ln=True)
                thin_line(pdf, L)
                pdf.ln(2.5)
                prev_was_rule = False
            else:
                # Add transition separator only if --- didn't just fire
                if not first_section and not prev_was_rule:
                    pdf.ln(3)
                    thick_line(pdf, L)
                    pdf.ln(3)
                elif not first_section and prev_was_rule:
                    pdf.ln(1)  # small gap after ---
                else:
                    pdf.ln(3)
                first_section = False

                pdf.set_font("Times", "B", 16)
                pdf.set_text_color(0, 0, 0)
                pdf.set_x(L)
                pdf.cell(CW, 8, text, ln=True)
                thick_line(pdf, L)
                pdf.ln(3)
                prev_was_rule = False

        # ### JOB TITLE
        elif raw.startswith("### "):
            text = sanitize(raw[4:].strip())
            pdf.ln(3)
            pdf.set_font("Helvetica", "B", 13)
            pdf.set_text_color(0, 0, 0)
            pdf.set_x(L)
            pdf.multi_cell(CW, 7, text)
            prev_was_rule = False

        # --- horizontal rule
        elif raw == "---":
            if in_header:
                in_header = False
                first_section = True
                pdf.ln(2)
                thick_line(pdf, L)
                pdf.ln(4)
            else:
                pdf.ln(2)
                thick_line(pdf, L)
                pdf.ln(3)
            prev_was_rule = True

        # - bullet
        elif raw.startswith("- "):
            text = sanitize(re.sub(r'\*{1,2}(.+?)\*{1,2}', r'\1', raw[2:]))
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(0, 0, 0)
            pdf.set_x(L + 4)
            pdf.cell(5, 5.5, BULLET, ln=False)
            pdf.set_x(L + 10)
            pdf.multi_cell(CW - 10, 5.5, text, align="J")
            prev_was_rule = False

        # **bold** subtitle in header
        elif in_header and raw.startswith("**") and raw.endswith("**"):
            text = sanitize(raw.strip("*"))
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(0, 0, 0)
            pdf.set_x(L)
            pdf.cell(CW - 32, 6, text, align="C", ln=True)
            prev_was_rule = False

        # *italic* dates
        elif raw.startswith("*") and raw.endswith("*") and not raw.startswith("**"):
            text = sanitize(raw.strip("*"))
            pdf.set_font("Helvetica", "I", 10)
            pdf.set_text_color(50, 50, 50)
            pdf.set_x(L)
            pdf.multi_cell(CW, 5.5, text)
            prev_was_rule = False

        # **bold** whole line (company lines)
        elif raw.startswith("**") and raw.endswith("**"):
            text = sanitize(raw.strip("*"))
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(0, 0, 0)
            pdf.set_x(L)
            pdf.multi_cell(CW, 5.5, text)
            prev_was_rule = False

        # mixed **bold** inline
        elif "**" in raw:
            parts = re.split(r'(\*\*[^*]+\*\*)', raw)
            pdf.set_x(L)
            for part in parts:
                if part.startswith("**") and part.endswith("**"):
                    pdf.set_font("Helvetica", "B", 10)
                    pdf.set_text_color(0, 0, 0)
                    pdf.write(5.5, sanitize(part.strip("*")))
                else:
                    pdf.set_font("Helvetica", "", 10)
                    pdf.set_text_color(0, 0, 0)
                    pdf.write(5.5, sanitize(part))
            pdf.ln(5.5)
            prev_was_rule = False

        # centered contact lines in header
        elif in_header:
            text = sanitize(re.sub(r'\*{1,2}(.+?)\*{1,2}', r'\1', raw))
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(60, 60, 60)
            pdf.set_x(L)
            pdf.multi_cell(CW - 32, 5, text, align="C")
            prev_was_rule = False

        # body text
        else:
            text = sanitize(re.sub(r'\*{1,2}(.+?)\*{1,2}', r'\1', raw))
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(0, 0, 0)
            pdf.set_x(L)
            pdf.multi_cell(CW, 5.5, text, align="J")
            prev_was_rule = False

    pdf.output(output_path)
    print("Done:", output_path)
