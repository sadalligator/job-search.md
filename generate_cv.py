import re, os, tempfile
from fpdf import FPDF

BULLET = chr(183)
PHOTO_PATH = "/home/user/job-search.md/tanya_photo.jpeg"

def sanitize(text):
    text = text.replace('–', '-').replace('—', '-')
    text = text.replace('‘', chr(39)).replace('’', chr(39))
    text = text.replace('“', chr(34)).replace('”', chr(34))
    text = text.replace('…', '...')
    text = text.replace('·', chr(183))
    text = text.replace('\xe9', 'e').replace('\xe8', 'e').replace('\xea', 'e')
    text = text.replace('\xe0', 'a').replace('\xe2', 'a')
    return text.encode('latin-1', errors='replace').decode('latin-1')

def make_circular_photo(photo_path):
    from PIL import Image, ImageDraw
    img = Image.open(photo_path).convert("RGB")
    size = min(img.size)
    img = img.crop(((img.width-size)//2, (img.height-size)//2,
                    (img.width+size)//2, (img.height+size)//2))
    img = img.resize((300, 300), Image.LANCZOS)
    mask = Image.new("L", (300, 300), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, 300, 300), fill=255)
    out = Image.new("RGB", (300, 300), (255, 255, 255))
    out.paste(img, (0, 0), mask)
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    out.save(tmp.name, "PNG")
    return tmp.name

def generate_pdf(cv_markdown, output_path, photo_path=PHOTO_PATH):
    class CV(FPDF):
        def header(self): pass
        def footer(self): pass

    pdf = CV(format="A4")
    pdf.set_margins(20, 15, 20)
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=12)

    if photo_path and os.path.exists(photo_path):
        circ = make_circular_photo(photo_path)
        pdf.image(circ, x=163, y=10, w=28, h=28)
        os.unlink(circ)

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
    print(f"Done: {output_path}")


# ── BASE CV MARKDOWN TEMPLATE ──────────────────────────────────────────────────
BASE_CV = """
# TANYA SHARMA

**Attorney | Legal Assistant | Paralegal**

Dubai, UAE | +971 50 278 1900 | Advocatetanyasharma7@gmail.com
linkedin.com/in/tanya-sharma-attorney/

---

## PROFESSIONAL SUMMARY

Attorney enrolled with the Bar Council of India, with 2+ years of post-enrolment experience in commercial, criminal and I.P litigation, contract drafting, legal research, and regulatory compliance. Experienced in supporting senior counsel, managing case files, and coordinating with clients and external parties across high-volume legal environments. Gained early career experience at one of India's leading litigation firms, developing hands-on expertise in legal drafting, client advisory, and brand protection strategy for FMCG and pharmaceutical clients across commercial and I.P disputes. Aiming to deliver high-quality, business-focused legal support in Dubai.

## CORE COMPETENCIES

Contract Review & Management - Legal Research & Analysis - Document Drafting & Vetting - Litigation Support - Regulatory Compliance - Company Secretarial Support - Court Filings & Submissions - Deadline Management - Legal Database Management - Client Coordination - Intellectual Property Law - Dispute Resolution

## PROFESSIONAL EXPERIENCE

### Executive Assistant
**Zopreneurs - Zoho Premium Partner | Dubai, UAE | Full-time, On-site**
*December 2025 - Present*
- Apply legal training and detail-oriented approach to support senior management with drafting, reviewing, and organizing business documentation, contracts, and internal communications in a fast-paced tech/automation environment.
- Manage executive calendars, meetings, and stakeholder coordination, ensuring efficient communication between clients, internal teams, and external partners.
- Support process, policy, and documentation discipline in line with the company's focus on automation, accuracy, and client-facing excellence.

### Independent Attorney
**High Court of Delhi | New Delhi, India | Full-time, On-site**
*September 2024 - December 2025*
- Completed over two years of post-qualification legal practice through work with multiple attorneys' chambers, with broad exposure to intellectual property, regulatory compliance, commercial and criminal litigation disputes.
- Represented clients before courts and tribunals, assisted in hearings, and supported attorneys with arguments, evidence preparation, and case strategy.
- Drafted and filed pleadings, motions, written submissions, legal notices, and ancillary documents in civil, criminal, and I.P cases.
- Conducted legal research, prepared legal opinions, and analysed statutes, case law, and regulations.
- Managed case files end-to-end, coordinated with clients and external counsel, and ensured timely filings.
- Advised brand owners on protecting reputation against disparaging content and coordinated takedowns across social media, e-commerce, and digital channels.
- Provided legal input on brand positioning, IP clearances, competitor monitoring, and commercial risk.

### Junior Legal Associate, Intellectual Property Law Litigation Team
**S.S. Rana & Co. Advocates | New Delhi, India | Full-time, On-site**
*September 2023 - May 2024*
- Drafted pleadings and notices for trademark, copyright and patent infringement matters.
- Developed and implemented brand protection strategies for FMCG and pharmaceutical clients, including anti-counterfeiting action plans.
- Managed end-to-end DMCA and platform takedown requests for counterfeit listings and fraudulent websites.
- Conducted I.P legal research and prepared compliance advisories for brand protection matters.
- Coordinated filings with clients, counsel, and trademark offices.
- Tracked litigation budgets and monitored case timelines.

## EDUCATION

**Bachelor of Arts and Bachelor of Laws (B.A. LL.B. Hons.)**
Amity University, Noida, Uttar Pradesh, India | 2018-2023 | Specialization: Intellectual Property Law | GPA: 7.2/10

## COURSES

- DL-303 Specialised Course on the Madrid System for the International Registration of Marks
- DL-304 Specialised Course on the Hague System for International Registration of Industrial Designs
- DL-730 Executive Course on Intellectual Property and Exports (Self Study)

## TECHNICAL SKILLS

**Legal Software & Tools:** Microsoft Office Suite (Word, Excel, PowerPoint, Outlook), Contract Management Systems, Legal Research Databases, Document Management Systems, Case Management Software, Zoho and CRM

**Languages:** English (Native), Hindi (Native), Punjabi (Fluent), French (Beginner)

## KEY ACHIEVEMENTS

- Managed 50+ legal document reviews with zero compliance errors.
- Streamlined case file systems, improving audit readiness and document retrieval.
- Coordinated multiple concurrent litigation matters, maintaining strict deadline adherence.
- Filed cases/documents before various forums including High Courts and District Courts in New Delhi, India.

---

*Current UAE visa: Provided by a family-owned company. UAE Driving License: RTA test pending. References available upon request.*
"""

if __name__ == "__main__":
    generate_pdf(BASE_CV, "/home/user/job-search.md/Tanya_Sharma_CV_Base.pdf")
