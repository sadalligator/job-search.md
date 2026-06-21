"""
Batch CV generator — runs generate_cv_pdf.generate_cv() for all 3 saved jobs.
"""
import sys
sys.path.insert(0, '/home/user/job-search.md')
from generate_cv_pdf import generate_cv

# ─────────────────────────────────────────────────────────────────────────────
# CV 1 — Legal Specialist | GLOBAL TAX ASSISTANT-FZCO
# ATS focus: corporate law, company formation, contracts, MOA, compliance, UAE
# ─────────────────────────────────────────────────────────────────────────────

generate_cv(
    filename="CV_Tanya_Sharma_GlobalTaxAssistant_LegalSpecialist",
    subtitle="Legal Specialist | Corporate Law & Compliance | Contract Drafting",
    summary=(
        "Qualified Legal Professional with 2+ years of post-qualification experience in "
        "corporate legal support, contract drafting, regulatory compliance, and legal "
        "documentation management. Strong foundation in drafting and reviewing commercial "
        "contracts, legal correspondence, and corporate resolutions. Experienced in "
        "coordinating with clients, stakeholders, and regulatory bodies to ensure "
        "compliance with applicable laws. Adept at managing legal documentation in "
        "high-volume environments and eager to apply legal expertise to corporate law and "
        "compliance workflows in Dubai, including corporate tax and VAT support."
    ),
    competencies=(
        "Corporate Law &amp; Company Formation Support • Contract Drafting &amp; Review • "
        "Legal Documentation &amp; Compliance • Regulatory &amp; Tax Compliance Support • "
        "MOA &amp; Corporate Resolutions • Government &amp; Authority Liaison • "
        "Legal Research &amp; Analysis • Client Coordination • Document Management • "
        "Intellectual Property Law • Dispute Resolution"
    ),
    experience_blocks=[
        {
            "title":   "Executive Assistant (Legal &amp; Corporate Support)",
            "company": "Zopreneurs | Zoho Premium Partner | Dubai, United Arab Emirates",
            "dates":   "December 2025 – Present | On-site",
            "bullets": [
                "Draft, review, and organise commercial contracts, corporate agreements, and internal legal documentation to ensure compliance and accuracy in a fast-paced business environment.",
                "Coordinate with government authorities, external partners, and internal teams on documentation, regulatory filings, and compliance-related processes.",
                "Maintain structured corporate filing and document management systems, ensuring data integrity, audit readiness, and efficient document retrieval.",
                "Support senior management with corporate governance documentation, policy compliance, and business correspondence.",
            ],
        },
        {
            "title":   "Independent Attorney",
            "company": "High Court of Delhi | New Delhi, India",
            "dates":   "September 2024 – December 2025 | Full-time, On-site",
            "bullets": [
                "Drafted and reviewed commercial contracts, legal notices, corporate resolutions, and ancillary legal documents across civil, IP, and commercial matters.",
                "Advised clients on corporate law, regulatory compliance, and legal risk; prepared legal opinions and compliance assessments across multiple practice areas.",
                "Conducted in-depth legal research on statutes, corporate regulations, and case law; produced practical compliance advisories for client matters.",
                "Coordinated with courts, government authorities, and external counsel to ensure timely regulatory filings and procedural compliance.",
                "Managed case files end-to-end and maintained structured legal documentation systems supporting audit readiness.",
            ],
        },
        {
            "title":   "Junior Legal Associate — IP Law Litigation Team",
            "company": "S.S. Rana &amp; Co. Advocates | New Delhi, India",
            "dates":   "September 2023 – May 2024",
            "bullets": [
                "Drafted commercial contracts, pleadings, corporate correspondence, and legal notices for trademark, copyright, and patent matters.",
                "Prepared compliance advisories and legal opinions on regulatory requirements for FMCG and pharmaceutical corporate clients.",
                "Coordinated filings with clients, external counsel, and trademark offices; maintained structured corporate documentation for audits.",
                "Conducted legal research on corporate regulations and compliance frameworks to support client advisory work.",
                "Tracked matter timelines and budgets; ensured timely filings in accordance with procedural and regulatory requirements.",
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
        "Managed 50+ legal document reviews including commercial contracts and compliance assessments with zero errors",
        "Prepared corporate compliance advisories for FMCG and pharmaceutical clients on regulatory and IP matters",
        "Coordinated multiple concurrent legal matters and regulatory filings, maintaining strict deadline adherence",
        "Filed cases and legal documents before High Courts and District Courts in New Delhi, India",
        "Streamlined legal case-file and documentation systems, significantly improving audit readiness",
    ],
)


# ─────────────────────────────────────────────────────────────────────────────
# CV 2 — In-House Lawyer / Legal Officer | Living Concept Engineering Consultant LLC
# ATS focus: in-house lawyer, legal officer, construction, court cases, documentation
# ─────────────────────────────────────────────────────────────────────────────

generate_cv(
    filename="CV_Tanya_Sharma_LivingConcept_InHouseLawyer",
    subtitle="In-House Lawyer | Legal Officer | Litigation &amp; Legal Documentation",
    summary=(
        "Qualified Legal Professional with 2+ years of post-qualification experience in "
        "litigation support, legal documentation, contract drafting, and coordination with "
        "courts, clients, and external counsel. Experienced in managing legal matters "
        "end-to-end including pleadings, submissions, legal notices, and case file "
        "management. Skilled at liaising with government authorities, subcontractors, and "
        "consultants to ensure procedural compliance and timely resolution of legal matters. "
        "Brings strong English drafting skills, a meticulous approach to legal documentation, "
        "and a commitment to delivering effective in-house legal support in Dubai."
    ),
    competencies=(
        "Litigation Support &amp; Court Filings • Legal Documentation &amp; Drafting • "
        "Contract Review &amp; Management • In-House Legal Advisory • "
        "Government &amp; Authority Coordination • External Counsel Liaison • "
        "Dispute Resolution • Legal Research &amp; Analysis • "
        "Client &amp; Stakeholder Coordination • Case File Management • "
        "Regulatory Compliance • Intellectual Property Law"
    ),
    experience_blocks=[
        {
            "title":   "Executive Assistant (Legal &amp; Documentation Support)",
            "company": "Zopreneurs | Zoho Premium Partner | Dubai, United Arab Emirates",
            "dates":   "December 2025 – Present | On-site",
            "bullets": [
                "Draft, review, and organise contracts, legal correspondence, and business documentation, applying legal training to ensure compliance in a fast-paced environment.",
                "Liaise with clients, external partners, and internal teams on documentation requirements, contractual obligations, and compliance matters.",
                "Maintain structured document management systems and coordinate legal administrative processes, ensuring audit readiness and data integrity.",
                "Support senior management with policy documentation, corporate correspondence, and governance-related administrative tasks.",
            ],
        },
        {
            "title":   "Independent Attorney",
            "company": "High Court of Delhi | New Delhi, India",
            "dates":   "September 2024 – December 2025 | Full-time, On-site",
            "bullets": [
                "Managed legal matters end-to-end including court appearances, hearings, evidence preparation, and case strategy across civil, commercial, and IP disputes.",
                "Drafted and filed pleadings, motions, written submissions, legal notices, and ancillary legal documents in civil and commercial matters.",
                "Coordinated with clients, external counsel, subcontractors, and government authorities to ensure timely filings and procedural compliance.",
                "Prepared legal opinions and conducted legal research on regulations, statutes, and case law relevant to disputes and compliance requirements.",
                "Managed case files and maintained comprehensive legal documentation systems to support matter management and audit readiness.",
            ],
        },
        {
            "title":   "Junior Legal Associate — IP Law Litigation Team",
            "company": "S.S. Rana &amp; Co. Advocates | New Delhi, India",
            "dates":   "September 2023 – May 2024",
            "bullets": [
                "Drafted pleadings, legal notices, and court submissions for IP infringement matters before Indian courts and tribunals.",
                "Coordinated with clients, external counsel, and government offices on legal filings, documentation, and procedural compliance requirements.",
                "Conducted legal research and prepared legal opinions on statutes and case law to support litigation strategies.",
                "Maintained structured legal documentation and case file systems to support court filings, audits, and matter management.",
                "Tracked litigation timelines and ensured all filings and submissions were completed within procedural deadlines.",
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
        "Managed 50+ legal document reviews and court filings with zero compliance or procedural errors",
        "Coordinated multiple concurrent litigation matters and court filings, maintaining strict deadline adherence",
        "Filed pleadings and legal documents before High Courts and District Courts across New Delhi, India",
        "Streamlined legal case-file management systems, improving document retrieval and audit readiness",
        "Delivered legal research and opinions supporting successful dispute resolution across IP and commercial matters",
    ],
)


# ─────────────────────────────────────────────────────────────────────────────
# CV 3 — Associate Lawyer | Motei & Associates LLC
# ATS focus: corporate & commercial law, dispute resolution, arbitration, English drafting
# ─────────────────────────────────────────────────────────────────────────────

generate_cv(
    filename="CV_Tanya_Sharma_Motei_AssociateLawyer",
    subtitle="Associate Lawyer | Corporate &amp; Commercial | Dispute Resolution",
    summary=(
        "Motivated and commercially minded Legal Professional with 2+ years of "
        "post-qualification experience in corporate and commercial law, dispute resolution, "
        "legal drafting, and client advisory work. Qualified and enrolled as a practising "
        "lawyer in India, with hands-on experience drafting and negotiating commercial "
        "agreements, preparing legal opinions, arbitration submissions, and conducting "
        "litigation support across civil and commercial matters. All legal work conducted "
        "and drafted independently in English. Experienced in advising international and "
        "corporate clients on legal risk, contracts, and dispute resolution strategies. "
        "Eager to contribute to a well-established Dubai law firm advising expatriate and "
        "international clients."
    ),
    competencies=(
        "Commercial &amp; Corporate Law • Dispute Resolution &amp; Arbitration Support • "
        "Legal Drafting &amp; Negotiation • Client Advisory &amp; Representation • "
        "Legal Research &amp; Opinions • Litigation Support • "
        "Contract Review &amp; Management • Legal Memoranda &amp; Submissions • "
        "Intellectual Property Law • Regulatory Compliance • Deadline Management"
    ),
    experience_blocks=[
        {
            "title":   "Executive Assistant (Legal &amp; Business Support)",
            "company": "Zopreneurs | Zoho Premium Partner | Dubai, United Arab Emirates",
            "dates":   "December 2025 – Present | On-site",
            "bullets": [
                "Draft, review, and negotiate commercial contracts and legal documentation in English, applying legal training in a fast-paced client-facing business environment.",
                "Advise senior management on contractual obligations, legal risk, and documentation standards to support sound business decision-making.",
                "Coordinate with clients, external partners, and internal stakeholders on legal and compliance matters, correspondence, and governance documentation.",
                "Maintain structured document management systems supporting audit readiness and efficient retrieval of legal records.",
            ],
        },
        {
            "title":   "Independent Attorney",
            "company": "High Court of Delhi | New Delhi, India",
            "dates":   "September 2024 – December 2025 | Full-time, On-site",
            "bullets": [
                "Advised corporate and individual clients on commercial disputes, IP matters, and regulatory compliance; prepared legal opinions and risk assessments independently in English.",
                "Drafted and negotiated commercial agreements, legal notices, arbitration submissions, written submissions, and client correspondence entirely in English.",
                "Represented clients before courts and tribunals; managed all stages of dispute resolution from initial advisory through hearings, advocacy, and case closure.",
                "Conducted in-depth legal research on statutes, case law, and regulations; prepared detailed legal memoranda and opinions to support client matters.",
                "Managed multiple concurrent client matters, coordinated with external counsel and government authorities, and maintained strict deadline adherence.",
            ],
        },
        {
            "title":   "Junior Legal Associate — IP Law Litigation Team",
            "company": "S.S. Rana &amp; Co. Advocates | New Delhi, India",
            "dates":   "September 2023 – May 2024",
            "bullets": [
                "Drafted and reviewed commercial agreements, pleadings, and legal notices for corporate clients in trademark, copyright, and patent dispute matters.",
                "Prepared legal opinions, compliance advisories, and arbitration-ready documentation for corporate clients in FMCG and pharmaceutical sectors.",
                "Conducted legal research and provided client advisory support on IP regulations, dispute resolution strategies, and compliance requirements.",
                "Coordinated directly with clients, external counsel, and courts on matter management, filings, and dispute resolution proceedings.",
                "Handled multiple client matters simultaneously, managing deadlines and delivering independently drafted legal documents in English.",
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
        "Independently drafted 50+ commercial agreements, legal opinions, and compliance documents in English with zero errors",
        "Prepared arbitration submissions and litigation documents for dispute resolution matters across IP and commercial practice areas",
        "Advised corporate clients in FMCG and pharmaceutical sectors on IP disputes, commercial contracts, and regulatory compliance",
        "Managed multiple concurrent client matters simultaneously, maintaining strict billing deadlines and client communication standards",
        "Filed cases and submissions before High Courts and District Courts across New Delhi; experienced in all stages of dispute resolution",
    ],
)

print("\nAll 3 CVs generated successfully.")
