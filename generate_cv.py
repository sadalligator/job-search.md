"""
CV Generator for Tanya Sharma
Produces PDFs matching the exact format of the original CV.
Usage: python3 generate_cv.py <variant_name> <content_module>
"""

import os
import sys
from docx import Document
from docx.shared import Pt, Inches, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import subprocess
from PIL import Image, ImageDraw
import copy


OUTPUT_DIR = "/home/user/job-search.md/generated series"
PHOTO_PATH = os.path.join(OUTPUT_DIR, "tanya_photo.jpeg")
CIRCULAR_PHOTO_PATH = os.path.join(OUTPUT_DIR, "tanya_photo_circle.png")


def make_circular_photo(src, dst, size=200):
    img = Image.open(src).convert("RGBA")
    # Crop to square from center
    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side)).resize((size, size), Image.LANCZOS)
    # Create circular mask
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    result = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    result.paste(img, mask=mask)
    # White background
    bg = Image.new("RGBA", (size, size), (255, 255, 255, 255))
    bg.paste(result, mask=result.split()[3])
    bg.convert("RGB").save(dst)


def set_cell_border(cell, **kwargs):
    """Set cell borders."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge in ('start', 'top', 'end', 'bottom', 'insideH', 'insideV'):
        tag = f'w:{edge}'
        element = OxmlElement(tag)
        element.set(qn('w:val'), 'nil')
        tcBorders.append(element)
    tcPr.append(tcBorders)


def remove_table_borders(table):
    tbl = table._tbl
    tblPr = tbl.tblPr
    if tblPr is None:
        tblPr = OxmlElement('w:tblPr')
        tbl.insert(0, tblPr)
    tblBorders = OxmlElement('w:tblBorders')
    for edge in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        el = OxmlElement(f'w:{edge}')
        el.set(qn('w:val'), 'nil')
        tblBorders.append(el)
    tblPr.append(tblBorders)
    for row in table.rows:
        for cell in row.cells:
            set_cell_border(cell)


def add_horizontal_rule(doc, thickness_pt=1.5):
    """Add a thick horizontal rule paragraph."""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), str(int(thickness_pt * 8)))  # sz in 1/8 pt
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '000000')
    pBdr.append(bottom)
    pPr.append(pBdr)
    pf = p.paragraph_format
    pf.space_before = Pt(4)
    pf.space_after = Pt(4)
    return p


def set_para_spacing(para, before=0, after=0, line=None):
    pf = para.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    if line:
        pf.line_spacing = Pt(line)
        pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY


def add_run_font(run, name="Times New Roman", size=11, bold=False, italic=False, color=None, spacing=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)
    if spacing is not None:
        rPr = run._r.get_or_add_rPr()
        spacing_el = OxmlElement('w:spacing')
        spacing_el.set(qn('w:val'), str(spacing))
        rPr.append(spacing_el)


def add_section_heading(doc, text, size=18, space_before=8, space_after=2):
    p = doc.add_paragraph()
    run = p.add_run(text)
    add_run_font(run, size=size, bold=True)
    set_para_spacing(p, before=space_before, after=space_after)
    return p


def add_subsection_heading(doc, text, size=13, space_before=6, space_after=2):
    p = doc.add_paragraph()
    run = p.add_run(text)
    add_run_font(run, size=size, bold=True)
    set_para_spacing(p, before=space_before, after=1)
    return p


def add_body_para(doc, text, size=10.5, space_before=1, space_after=2, italic=False, bold=False, justified=True):
    p = doc.add_paragraph()
    if justified:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = p.add_run(text)
    add_run_font(run, size=size, bold=bold, italic=italic)
    set_para_spacing(p, before=space_before, after=space_after)
    return p


def add_bullet(doc, text, size=10.5):
    p = doc.add_paragraph(style='List Bullet')
    run = p.add_run(text)
    add_run_font(run, size=size)
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    set_para_spacing(p, before=1, after=1)
    return p


def set_document_margins(doc, top=1.8, bottom=1.8, left=2.5, right=2.5):
    section = doc.sections[0]
    section.top_margin = Cm(top)
    section.bottom_margin = Cm(bottom)
    section.left_margin = Cm(left)
    section.right_margin = Cm(right)
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)


def build_header(doc, subtitle):
    """Build the two-column header: name+contact left, circular photo right."""
    make_circular_photo(PHOTO_PATH, CIRCULAR_PHOTO_PATH, size=220)

    table = doc.add_table(rows=1, cols=2)
    remove_table_borders(table)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Column widths: wide left, narrow right
    table.columns[0].width = Inches(5.0)
    table.columns[1].width = Inches(1.5)

    left_cell = table.cell(0, 0)
    right_cell = table.cell(0, 1)
    left_cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    right_cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

    # Name
    name_p = left_cell.paragraphs[0]
    name_run = name_p.add_run("TANYA SHARMA")
    name_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    name_run.font.name = "Times New Roman"
    name_run.font.size = Pt(30)
    name_run.font.bold = True
    # Wide letter spacing
    rPr = name_run._r.get_or_add_rPr()
    sp = OxmlElement('w:spacing')
    sp.set(qn('w:val'), '120')
    rPr.append(sp)
    set_para_spacing(name_p, before=0, after=2)

    # Subtitle
    sub_p = left_cell.add_paragraph()
    sub_run = sub_p.add_run(subtitle)
    sub_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    add_run_font(sub_run, size=11, bold=True)
    set_para_spacing(sub_p, before=0, after=3)

    # Contact line 1
    c1_p = left_cell.add_paragraph()
    c1_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r1 = c1_p.add_run("Dubai, UAE | +971 50 278 1900 | ")
    add_run_font(r1, size=10)
    r2 = c1_p.add_run("Advocatetanyasharma7@gmail.com")
    add_run_font(r2, size=10, color=(17, 85, 204))
    set_para_spacing(c1_p, before=0, after=1)

    # Contact line 2 (LinkedIn)
    c2_p = left_cell.add_paragraph()
    c2_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r3 = c2_p.add_run("LinkedIn: https://www.linkedin.com/in/tanyasharma1699/")
    add_run_font(r3, size=10)
    set_para_spacing(c2_p, before=0, after=0)

    # Photo (right cell)
    photo_p = right_cell.paragraphs[0]
    photo_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run_photo = photo_p.add_run()
    run_photo.add_picture(CIRCULAR_PHOTO_PATH, width=Inches(1.25))
    set_para_spacing(photo_p, before=0, after=0)


def generate_cv(filename, subtitle, summary, competencies, experience_blocks, education_block,
                courses, skills_line, achievements):
    """
    Generate a CV PDF.

    experience_blocks: list of dicts:
      { 'title': str, 'company': str, 'dates': str, 'bullets': [str] }

    education_block: dict:
      { 'degree': str, 'university': str, 'dates': str, 'notes': [str] }
    """
    doc = Document()
    set_document_margins(doc)

    # Remove default styles spacing
    doc.styles['Normal'].font.name = 'Times New Roman'
    doc.styles['Normal'].font.size = Pt(10.5)

    # Header
    build_header(doc, subtitle)

    # Rule
    add_horizontal_rule(doc, thickness_pt=2)

    # PROFESSIONAL SUMMARY
    add_section_heading(doc, "PROFESSIONAL SUMMARY", size=17, space_before=4, space_after=2)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = p.add_run(summary)
    add_run_font(run, size=10.5)
    set_para_spacing(p, before=2, after=4)

    # Rule
    add_horizontal_rule(doc, thickness_pt=1.5)

    # CORE COMPETENCIES (smaller, bold caps, no rule above)
    p_cc_label = doc.add_paragraph()
    r_cc = p_cc_label.add_run("CORE COMPETENCIES")
    add_run_font(r_cc, size=10.5, bold=True)
    set_para_spacing(p_cc_label, before=4, after=1)

    p_cc = doc.add_paragraph()
    p_cc.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run_cc = p_cc.add_run(competencies)
    add_run_font(run_cc, size=10.5)
    set_para_spacing(p_cc, before=0, after=4)

    # Rule
    add_horizontal_rule(doc, thickness_pt=2)

    # PROFESSIONAL EXPERIENCE
    add_section_heading(doc, "PROFESSIONAL EXPERIENCE", size=17, space_before=4, space_after=2)

    for exp in experience_blocks:
        # Job title
        add_subsection_heading(doc, exp['title'], size=13, space_before=4, space_after=1)

        # Company | Location
        p_co = doc.add_paragraph()
        run_co = p_co.add_run(exp['company'])
        add_run_font(run_co, size=10.5, bold=True)
        set_para_spacing(p_co, before=0, after=1)

        # Dates
        p_dt = doc.add_paragraph()
        run_dt = p_dt.add_run(exp['dates'])
        add_run_font(run_dt, size=10.5, italic=True)
        set_para_spacing(p_dt, before=0, after=2)

        # Bullets
        for b in exp['bullets']:
            add_bullet(doc, b, size=10.5)

    # EDUCATION
    add_horizontal_rule(doc, thickness_pt=2)
    add_section_heading(doc, "EDUCATION", size=17, space_before=4, space_after=2)

    p_deg = doc.add_paragraph()
    run_deg = p_deg.add_run(education_block['degree'])
    add_run_font(run_deg, size=10.5, bold=True)
    set_para_spacing(p_deg, before=2, after=0)

    p_uni = doc.add_paragraph()
    run_uni = p_uni.add_run(education_block['university'])
    add_run_font(run_uni, size=10.5)
    set_para_spacing(p_uni, before=0, after=0)

    p_dates_ed = doc.add_paragraph()
    run_dates_ed = p_dates_ed.add_run(education_block['dates'])
    add_run_font(run_dates_ed, size=10.5, italic=True)
    set_para_spacing(p_dates_ed, before=0, after=0)

    for note in education_block.get('notes', []):
        p_note = doc.add_paragraph()
        run_note = p_note.add_run(note)
        add_run_font(run_note, size=10.5)
        set_para_spacing(p_note, before=0, after=0)

    # COURSES
    add_horizontal_rule(doc, thickness_pt=1.5)
    add_section_heading(doc, "COURSES", size=17, space_before=4, space_after=2)
    for c in courses:
        add_bullet(doc, c, size=10.5)

    # TECHNICAL SKILLS
    add_horizontal_rule(doc, thickness_pt=1.5)
    add_section_heading(doc, "TECHNICAL SKILLS", size=17, space_before=4, space_after=2)
    p_sk = doc.add_paragraph()
    p_sk.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_sk_label = p_sk.add_run("Legal Software & Tools: ")
    add_run_font(r_sk_label, size=10.5, bold=True)
    r_sk_val = p_sk.add_run(skills_line)
    add_run_font(r_sk_val, size=10.5)
    set_para_spacing(p_sk, before=2, after=2)

    p_lang = doc.add_paragraph()
    r_lang_label = p_lang.add_run("Languages: ")
    add_run_font(r_lang_label, size=10.5, bold=True)
    r_lang_val = p_lang.add_run("English (Native), Hindi (Native), Punjabi (Fluent), French (Beginner)")
    add_run_font(r_lang_val, size=10.5)
    set_para_spacing(p_lang, before=0, after=4)

    # KEY ACHIEVEMENTS
    add_horizontal_rule(doc, thickness_pt=2)
    add_section_heading(doc, "KEY ACHIEVEMENTS", size=17, space_before=4, space_after=2)
    for a in achievements:
        add_bullet(doc, a, size=10.5)

    # Footer note
    add_horizontal_rule(doc, thickness_pt=1)
    p_ref = doc.add_paragraph()
    run_ref = p_ref.add_run(
        "References available upon request\n"
        "Current visa is sponsored by a family-owned company.\n"
        "UAE driving License: RTA test pending."
    )
    add_run_font(run_ref, size=9.5)
    set_para_spacing(p_ref, before=2, after=0)

    # Save DOCX
    docx_path = os.path.join(OUTPUT_DIR, filename + ".docx")
    doc.save(docx_path)
    print(f"Saved DOCX: {docx_path}")

    # Convert to PDF via LibreOffice
    result = subprocess.run(
        ["libreoffice", "--headless", "--convert-to", "pdf",
         "--outdir", OUTPUT_DIR, docx_path],
        capture_output=True, text=True, timeout=60
    )
    pdf_path = os.path.join(OUTPUT_DIR, filename + ".pdf")
    if os.path.exists(pdf_path):
        print(f"Saved PDF:  {pdf_path}")
    else:
        print(f"PDF conversion output: {result.stdout} {result.stderr}")

    return pdf_path


# ─────────────────────────────────────────────────────────────────────────────
# CV VARIANT: Enrologies Global Consultancy — Legal Advisor
# ─────────────────────────────────────────────────────────────────────────────

enrologies_cv = dict(
    filename="CV_Tanya_Sharma_Enrologies_Legal_Advisor",
    subtitle="Legal Advisor | Contract Specialist | Regulatory Compliance",
    summary=(
        "Results-driven Legal Professional with 2+ years of post-qualification experience in "
        "contract drafting and negotiation, regulatory compliance, dispute resolution, and "
        "corporate legal advisory. Qualified and enrolled as a practising lawyer in India, with "
        "a strong foundation in commercial law, litigation, and intellectual property. Adept at "
        "reviewing and managing legal documentation, advising stakeholders on legal risk, "
        "monitoring regulatory developments, and ensuring organisational compliance in "
        "high-volume, deadline-driven environments. Committed to delivering practical, "
        "business-focused legal support in Dubai."
    ),
    competencies=(
        "Contract Drafting & Negotiation • Regulatory Compliance • "
        "Legal Research & Analysis • Corporate Governance Support • "
        "Risk Assessment & Management • Dispute Resolution • "
        "Legal Advisory • Policy Development • Document Management • "
        "Stakeholder Coordination • Intellectual Property Law • "
        "Government & Regulatory Liaison"
    ),
    experience_blocks=[
        {
            "title": "Executive Assistant (Legal & Business Support)",
            "company": "Zopreneurs | Zoho Premium Partner | Dubai, United Arab Emirates",
            "dates": "December 2025 – Present | On-site",
            "bullets": [
                "Draft, review, and organise business contracts, agreements, and internal legal documentation, applying legal training to ensure compliance and accuracy in a fast-paced tech environment.",
                "Advise senior management on documentation standards and contractual obligations, supporting risk-aware decision-making across business operations.",
                "Develop and maintain structured digital filing and document management systems, ensuring audit readiness and data integrity in line with regulatory requirements.",
                "Coordinate compliance-related processes, policy documentation, and cross-functional workflows aligned with organisational governance standards.",
            ],
        },
        {
            "title": "Independent Attorney",
            "company": "High Court of Delhi | New Delhi, India",
            "dates": "September 2024 – December 2025 | Full-time, On-site",
            "bullets": [
                "Provided legal advisory services across IP, regulatory compliance, commercial, and criminal matters; analysed legal risk and advised clients on appropriate courses of action.",
                "Drafted and reviewed contracts, pleadings, legal notices, and written submissions; ensured all documents met procedural and regulatory compliance standards.",
                "Conducted in-depth legal research on statutes, case law, and regulations relevant to compliance and contractual obligations; prepared legal opinions and risk analyses.",
                "Represented clients before courts and tribunals, managing all stages of dispute resolution from initial advisory through to hearing, advocacy, and case closure.",
                "Managed case files end-to-end, coordinating with clients, external counsel, and government authorities to ensure timely and compliant submission of all documentation.",
            ],
        },
        {
            "title": "Junior Legal Associate — Intellectual Property Law Litigation Team",
            "company": "S.S. Rana & Co. Advocates | New Delhi, India",
            "dates": "September 2023 – May 2024",
            "bullets": [
                "Drafted and reviewed pleadings, legal notices, and correspondence for trademark, copyright, and patent infringement matters in a high-volume law firm.",
                "Prepared compliance advisories and legal opinions on brand protection and regulatory requirements for corporate clients in FMCG and pharmaceutical sectors.",
                "Conducted legal research on statutes and case law to support dispute resolution strategies, contract positions, and compliance assessments.",
                "Coordinated all document management and filings with clients, external counsel, and trademark offices; maintained structured records to support audits.",
                "Tracked litigation timelines and budgets; ensured timely filings in accordance with applicable procedural requirements.",
            ],
        },
    ],
    education_block={
        "degree": "Bachelor of Arts and Bachelor of Laws (B.A. LL.B. Hons.)",
        "university": "Amity University, Noida, Uttar Pradesh, India",
        "dates": "2018 – 2023",
        "notes": ["Specialisation: Intellectual Property Law", "GPA: 7.2/10"],
    },
    courses=[
        "DL-730 Executive Course on Intellectual Property and Exports (Self Study) – Ongoing",
        "DL-303 Specialised Course on the Madrid System for International Registration of Marks",
        "DL-304 Specialised Course on the Hague System for International Registration of Industrial Designs – Ongoing",
    ],
    skills_line=(
        "Microsoft Office Suite (Word, Excel, PowerPoint, Outlook), Contract Management Systems, "
        "Legal Research Databases, Document Management Systems, Case Management Software"
    ),
    achievements=[
        "Managed 50+ legal document reviews across IP, commercial, and compliance matters with zero compliance errors",
        "Delivered regulatory compliance advisories for brand protection to corporate clients in FMCG and pharmaceutical sectors",
        "Coordinated multiple concurrent litigation and compliance matters simultaneously, maintaining strict deadline adherence",
        "Filed cases and legal documents before High Courts and District Courts across New Delhi, India",
        "Streamlined legal case-file management systems, improving document retrieval and audit readiness",
    ],
)


if __name__ == "__main__":
    pdf = generate_cv(**enrologies_cv)
    print(f"\nDone. PDF saved at:\n{pdf}")
