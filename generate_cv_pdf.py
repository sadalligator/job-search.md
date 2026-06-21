"""
CV PDF Generator — Tanya Sharma
Produces PDFs matching the exact format of the original CV using ReportLab.
Photo: circular crop, top-right of header.
Font: Times New Roman (or serif fallback).
Layout: 2 pages max, A4.
"""

import os
from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer,
    Table, TableStyle, HRFlowable, Image as RLImage, KeepTogether
)
from reportlab.platypus.flowables import Flowable
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io

OUTPUT_DIR = "/home/user/job-search.md/generated-cvs"
PHOTO_SRC  = os.path.join(OUTPUT_DIR, "tanya_photo.jpeg")
PHOTO_CIRC = os.path.join(OUTPUT_DIR, "tanya_photo_circle.png")

PAGE_W, PAGE_H = A4          # 595.27 x 841.89 pt
MARGIN_L = 2.2 * cm
MARGIN_R = 2.0 * cm
MARGIN_T = 1.8 * cm
MARGIN_B = 1.8 * cm
BODY_W   = PAGE_W - MARGIN_L - MARGIN_R


# ── Fonts ────────────────────────────────────────────────────────────────────

def register_fonts():
    """Register serif fonts, falling back to built-in Times."""
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics

    sets = [
        # (regular, bold, italic, bolditalic)
        (
            "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf",
            "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman_Bold.ttf",
            "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman_Italic.ttf",
            "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman_Bold_Italic.ttf",
        ),
        (
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf",
        ),
    ]
    for reg, bold, ita, bita in sets:
        if all(os.path.exists(p) for p in (reg, bold, ita, bita)):
            try:
                pdfmetrics.registerFont(TTFont("TNR",       reg))
                pdfmetrics.registerFont(TTFont("TNR-Bold",  bold))
                pdfmetrics.registerFont(TTFont("TNR-Italic",ita))
                pdfmetrics.registerFont(TTFont("TNR-BoldItalic", bita))
                from reportlab.pdfbase.ttfonts import TTFontFace
                pdfmetrics.registerFontFamily(
                    "TNR",
                    normal="TNR", bold="TNR-Bold",
                    italic="TNR-Italic", boldItalic="TNR-BoldItalic"
                )
                return {"TNR": "TNR", "TNR-Bold": "TNR-Bold",
                        "TNR-Italic": "TNR-Italic", "TNR-BoldItalic": "TNR-BoldItalic"}
            except Exception:
                pass
    # Built-in Times fallback
    return {
        "TNR":           "Times-Roman",
        "TNR-Bold":      "Times-Bold",
        "TNR-Italic":    "Times-Italic",
        "TNR-BoldItalic":"Times-BoldItalic",
    }


FONTS = register_fonts()
F_REG  = FONTS["TNR"]
F_BOLD = FONTS["TNR-Bold"]
F_ITA  = FONTS["TNR-Italic"]
F_BITA = FONTS["TNR-BoldItalic"]


# ── Photo helper ─────────────────────────────────────────────────────────────

def make_circular_photo(src, dst, size=260):
    img = Image.open(src).convert("RGBA")
    w, h = img.size
    side = min(w, h)
    # Crop from top to capture face (not center which cuts off the face in portrait photos)
    img = img.crop((0, 0, side, side))
    img = img.resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
    result = Image.new("RGBA", (size, size), (255,255,255,0))
    result.paste(img, mask=mask)
    bg = Image.new("RGBA", (size, size), (255,255,255,255))
    bg.paste(result, mask=result.split()[3])
    bg.convert("RGB").save(dst, "PNG")


# ── Style helpers ─────────────────────────────────────────────────────────────

def S(name, parent=None, **kw):
    return ParagraphStyle(name, parent=parent, **kw)


def make_styles():
    base = ParagraphStyle("base", fontName=F_REG, fontSize=10.5,
                          leading=14, textColor=colors.black)
    return {
        "base":      base,
        "name":      S("name",      fontName=F_BOLD, fontSize=29,
                        leading=33, textColor=colors.black, letterSpacing=3),
        "subtitle":  S("subtitle",  fontName=F_BOLD, fontSize=11,
                        leading=14, textColor=colors.black),
        "contact":   S("contact",   fontName=F_REG,  fontSize=10,
                        leading=13, textColor=colors.black),
        "sec_head":  S("sec_head",  fontName=F_BOLD, fontSize=17,
                        leading=20, spaceAfter=2, spaceBefore=6),
        "sub_head":  S("sub_head",  fontName=F_BOLD, fontSize=12.5,
                        leading=15, spaceBefore=5, spaceAfter=1),
        "company":   S("company",   fontName=F_BOLD, fontSize=10.5,
                        leading=13, spaceBefore=0, spaceAfter=1),
        "dates":     S("dates",     fontName=F_ITA,  fontSize=10.5,
                        leading=13, spaceBefore=0, spaceAfter=2),
        "body":      S("body",      fontName=F_REG,  fontSize=10.5,
                        leading=14, alignment=TA_JUSTIFY,
                        spaceBefore=1, spaceAfter=2),
        "bullet":    S("bullet",    fontName=F_REG,  fontSize=10.5,
                        leading=14, leftIndent=14, firstLineIndent=-10,
                        alignment=TA_JUSTIFY, spaceBefore=1, spaceAfter=1),
        "comp_label":S("comp_label",fontName=F_BOLD, fontSize=10.5,
                        leading=13, spaceBefore=4, spaceAfter=1),
        "comp_body": S("comp_body", fontName=F_REG,  fontSize=10.5,
                        leading=14, spaceBefore=0, spaceAfter=4),
        "footer":    S("footer",    fontName=F_REG,  fontSize=9.5,
                        leading=13, spaceBefore=4),
    }


def HR(thickness=1.5):
    return HRFlowable(width="100%", thickness=thickness, color=colors.black,
                      spaceAfter=4, spaceBefore=4)


def bullet_para(text, styles):
    return Paragraph(f"• &nbsp; {text}", styles["bullet"])


# ── Header (name + contact left, photo right) ────────────────────────────────

def build_header(styles):
    make_circular_photo(PHOTO_SRC, PHOTO_CIRC, size=260)

    photo = RLImage(PHOTO_CIRC, width=3.3*cm, height=3.3*cm)

    name_para    = Paragraph("TANYA SHARMA", styles["name"])
    sub_para     = Paragraph(SUBTITLE, styles["subtitle"])
    contact_line = (
        f'Dubai, UAE &nbsp;|&nbsp; +971 50 278 1900 &nbsp;|&nbsp; '
        f'<font color="#1155CC">Advocatetanyasharma7@gmail.com</font>'
    )
    c1_para = Paragraph(contact_line, styles["contact"])
    c2_para = Paragraph("LinkedIn: https://www.linkedin.com/in/tanyasharma1699/",
                        styles["contact"])

    left_content = [name_para,
                    Spacer(1, 2),
                    sub_para,
                    Spacer(1, 3),
                    c1_para,
                    Spacer(1, 1),
                    c2_para]

    # Build as table: [left stack | photo]
    left_col_w  = BODY_W - 3.6*cm
    right_col_w = 3.6*cm

    data = [[left_content, photo]]
    t = Table(data, colWidths=[left_col_w, right_col_w])
    t.setStyle(TableStyle([
        ('VALIGN',    (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN',     (1,0), (1,0),   'RIGHT'),
        ('TOPPADDING',(0,0), (-1,-1), 0),
        ('BOTTOMPADDING',(0,0),(-1,-1),0),
        ('LEFTPADDING', (0,0),(-1,-1),0),
        ('RIGHTPADDING',(0,0),(-1,-1),0),
    ]))
    return t


# ── CV content data ──────────────────────────────────────────────────────────

SUBTITLE    = ""          # set per variant
SUMMARY     = ""
COMPETENCIES= ""
EXPERIENCE  = []
EDUCATION   = {}
COURSES     = []
SKILLS_LINE = ""
ACHIEVEMENTS= []


# ── Main builder ─────────────────────────────────────────────────────────────

def generate_cv(filename, subtitle, summary, competencies,
                experience_blocks, education_block,
                courses, skills_line, achievements):
    global SUBTITLE
    SUBTITLE = subtitle

    styles  = make_styles()
    story   = []

    # Header
    story.append(build_header(styles))
    story.append(Spacer(1, 3))
    story.append(HR(2))

    # Professional Summary
    story.append(Paragraph("PROFESSIONAL SUMMARY", styles["sec_head"]))
    story.append(Paragraph(summary, styles["body"]))
    story.append(Spacer(1, 2))
    story.append(HR(1.5))

    # Core Competencies
    story.append(Paragraph("CORE COMPETENCIES", styles["comp_label"]))
    story.append(Paragraph(competencies, styles["comp_body"]))
    story.append(HR(2))

    # Professional Experience
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", styles["sec_head"]))

    for exp in experience_blocks:
        block = [
            Paragraph(exp["title"],   styles["sub_head"]),
            Paragraph(exp["company"], styles["company"]),
            Paragraph(exp["dates"],   styles["dates"]),
        ]
        for b in exp["bullets"]:
            block.append(bullet_para(b, styles))
        block.append(Spacer(1, 3))
        story.append(KeepTogether(block))

    # Education
    story.append(HR(2))
    story.append(Paragraph("EDUCATION", styles["sec_head"]))
    ed = education_block
    story.append(Paragraph(ed["degree"],     styles["company"]))
    story.append(Paragraph(ed["university"], styles["body"]))
    p_dates = Paragraph(ed["dates"], styles["dates"])
    story.append(p_dates)
    for note in ed.get("notes", []):
        story.append(Paragraph(note, styles["body"]))
    story.append(Spacer(1, 2))

    # Courses
    story.append(HR(1.5))
    story.append(Paragraph("COURSES", styles["sec_head"]))
    for c in courses:
        story.append(bullet_para(c, styles))
    story.append(Spacer(1, 2))

    # Technical Skills
    story.append(HR(1.5))
    story.append(Paragraph("TECHNICAL SKILLS", styles["sec_head"]))
    skills_para = Paragraph(
        f'<b>Legal Software &amp; Tools:</b> {skills_line}', styles["body"]
    )
    story.append(skills_para)
    lang_para = Paragraph(
        '<b>Languages:</b> English (Native), Hindi (Native), Punjabi (Fluent), French (Beginner)',
        styles["body"]
    )
    story.append(lang_para)
    story.append(Spacer(1, 2))

    # Key Achievements
    story.append(HR(2))
    story.append(Paragraph("KEY ACHIEVEMENTS", styles["sec_head"]))
    for a in achievements:
        story.append(bullet_para(a, styles))
    story.append(Spacer(1, 3))

    # Footer
    story.append(HR(1))
    footer_text = (
        "References available upon request<br/>"
        "Current visa is sponsored by a family-owned company.<br/>"
        "UAE driving License: RTA test pending."
    )
    story.append(Paragraph(footer_text, styles["footer"]))

    # Build PDF
    out_path = os.path.join(OUTPUT_DIR, filename + ".pdf")
    doc = BaseDocTemplate(
        out_path,
        pagesize=A4,
        leftMargin=MARGIN_L,
        rightMargin=MARGIN_R,
        topMargin=MARGIN_T,
        bottomMargin=MARGIN_B,
    )
    frame = Frame(MARGIN_L, MARGIN_B, BODY_W, PAGE_H - MARGIN_T - MARGIN_B,
                  id="main", showBoundary=0)
    doc.addPageTemplates([PageTemplate(id="Page", frames=[frame])])
    doc.build(story)
    print(f"PDF saved: {out_path}")
    return out_path


# ─────────────────────────────────────────────────────────────────────────────
# VARIANT 1: Enrologies Global Consultancy — Legal Advisor
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    generate_cv(
        filename="CV_Tanya_Sharma_Enrologies_Legal_Advisor",
        subtitle="Legal Advisor | Contract Specialist | Regulatory Compliance",
        summary=(
            "Results-driven Legal Professional with 2+ years of post-qualification experience in "
            "contract drafting and negotiation, regulatory compliance, dispute resolution, and "
            "corporate legal advisory. Qualified and enrolled as a practising lawyer in India, "
            "with a strong foundation in commercial law, litigation, and intellectual property. "
            "Adept at reviewing and managing legal documentation, advising stakeholders on legal "
            "risk, monitoring regulatory developments, and ensuring organisational compliance in "
            "high-volume, deadline-driven environments. Committed to delivering practical, "
            "business-focused legal support in Dubai."
        ),
        competencies=(
            "Contract Drafting &amp; Negotiation • Regulatory Compliance • "
            "Legal Research &amp; Analysis • Corporate Governance Support • "
            "Risk Assessment &amp; Management • Dispute Resolution • "
            "Legal Advisory • Policy Development • Document Management • "
            "Stakeholder Coordination • Intellectual Property Law • "
            "Government &amp; Regulatory Liaison"
        ),
        experience_blocks=[
            {
                "title":   "Executive Assistant (Legal &amp; Business Support)",
                "company": "Zopreneurs | Zoho Premium Partner | Dubai, United Arab Emirates",
                "dates":   "December 2025 – Present | On-site",
                "bullets": [
                    "Draft, review, and organise business contracts, agreements, and internal legal documentation, applying legal training to ensure compliance and accuracy in a fast-paced tech environment.",
                    "Advise senior management on documentation standards and contractual obligations, supporting risk-aware decision-making across business operations.",
                    "Develop and maintain structured digital filing and document management systems, ensuring audit readiness and data integrity in line with regulatory requirements.",
                    "Coordinate compliance-related processes, policy documentation, and cross-functional workflows aligned with organisational governance standards.",
                ],
            },
            {
                "title":   "Independent Attorney",
                "company": "High Court of Delhi | New Delhi, India",
                "dates":   "September 2024 – December 2025 | Full-time, On-site",
                "bullets": [
                    "Provided legal advisory services across IP, regulatory compliance, commercial, and criminal matters; analysed legal risk and advised clients on appropriate courses of action.",
                    "Drafted and reviewed contracts, pleadings, legal notices, and written submissions; ensured all documents met procedural and regulatory compliance standards.",
                    "Conducted in-depth legal research on statutes, case law, and regulations relevant to compliance and contractual obligations; prepared legal opinions and risk analyses.",
                    "Represented clients before courts and tribunals, managing all stages of dispute resolution from initial advisory through to hearing and case closure.",
                    "Managed case files end-to-end, coordinating with clients, external counsel, and government authorities to ensure timely and compliant documentation.",
                ],
            },
            {
                "title":   "Junior Legal Associate — IP Law Litigation Team",
                "company": "S.S. Rana &amp; Co. Advocates | New Delhi, India",
                "dates":   "September 2023 – May 2024",
                "bullets": [
                    "Drafted and reviewed pleadings, legal notices, and correspondence for trademark, copyright, and patent infringement matters in a high-volume law firm.",
                    "Prepared compliance advisories and legal opinions on brand protection and regulatory requirements for FMCG and pharmaceutical sector clients.",
                    "Conducted legal research on statutes and case law to support dispute resolution strategies, contract positions, and compliance assessments.",
                    "Coordinated document management and filings with clients, external counsel, and trademark offices; maintained structured records for audits.",
                    "Tracked litigation timelines and budgets; ensured timely filings in accordance with all procedural requirements.",
                ],
            },
        ],
        education_block={
            "degree":     "Bachelor of Arts and Bachelor of Laws (B.A. LL.B. Hons.)",
            "university": "Amity University, Noida, Uttar Pradesh, India",
            "dates":      "2018 – 2023",
            "notes":      ["Specialisation: Intellectual Property Law", "GPA: 7.2/10"],
        },
        courses=[
            "DL-730 Executive Course on Intellectual Property and Exports (Self Study) – Ongoing",
            "DL-303 Specialised Course on the Madrid System for International Registration of Marks",
            "DL-304 Specialised Course on the Hague System for Registration of Industrial Designs – Ongoing",
        ],
        skills_line=(
            "Microsoft Office Suite (Word, Excel, PowerPoint, Outlook), Contract Management Systems, "
            "Legal Research Databases, Document Management Systems, Case Management Software"
        ),
        achievements=[
            "Managed 50+ legal document reviews across IP, commercial, and compliance matters with zero compliance errors",
            "Delivered regulatory compliance advisories for brand protection to FMCG and pharmaceutical sector clients",
            "Coordinated multiple concurrent litigation and compliance matters simultaneously, maintaining strict deadline adherence",
            "Filed cases and legal documents before High Courts and District Courts across New Delhi, India",
            "Streamlined legal case-file management systems, improving document retrieval and audit readiness",
        ],
    )
