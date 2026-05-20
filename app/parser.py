import re
from pypdf import PdfReader

SECTION_PATTERNS = {
    "education":      r"\b(education|academic background|qualifications|academic details)\b",
    "experience":     r"\b(experience|work experience|internship|employment|professional experience)\b",
    "projects":       r"\b(projects|personal projects|academic projects|project work|key projects|notable projects)\b",
    "skills":         r"\b(skills|technical skills|core competencies|tools|technologies|tech stack)\b",
    "achievements":   r"\b(achievements|awards|honors|accomplishments|recognitions)\b",
    "certifications": r"\b(certifications|courses|training|licenses)\b",
    "summary":        r"\b(summary|objective|profile|about me|about)\b",
    "publications":   r"\b(publications|research|papers)\b",
    "extracurricular":r"\b(extracurricular|activities|hobbies|interests|volunteering)\b",
}


def extract_text_from_pdf(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    pages = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text.strip())
    return "\n".join(pages)


def split_into_sections(resume_text: str) -> dict[str, str]:
    lines = resume_text.split("\n")
    sections: dict[str, list[str]] = {"header": []}
    current_section = "header"

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        detected = _detect_section_header(stripped)
        if detected:
            current_section = detected
            sections.setdefault(current_section, [])
        else:
            sections.setdefault(current_section, []).append(stripped)

    return {sec: "\n".join(lines) for sec, lines in sections.items()}


def _detect_section_header(line: str) -> str | None:
    if len(line) > 55:
        return None
    line_clean = line.strip().rstrip(":").strip()
    line_lower = line_clean.lower()
    for section_name, pattern in SECTION_PATTERNS.items():
        if re.search(pattern, line_lower):
            return section_name
    if line_clean.isupper() and len(line_clean) > 2:
        for section_name, pattern in SECTION_PATTERNS.items():
            if re.search(pattern, line_lower):
                return section_name
    return None


def extract_cgpa(resume_text: str) -> float | None:
    patterns = [
        r"cgpa[:\s]+([0-9]\.[0-9]{1,2})",
        r"gpa[:\s]+([0-9]\.[0-9]{1,2})",
        r"([0-9]\.[0-9]{1,2})\s*/\s*10",
        r"([0-9]\.[0-9]{1,2})\s*/\s*4\.0",
        r"cpi[:\s]+([0-9]\.[0-9]{1,2})",
        r"sgpa[:\s]+([0-9]\.[0-9]{1,2})",
    ]
    text_lower = resume_text.lower()
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            val = float(match.group(1))
            if val <= 4.0:
                val = val * 2.5
            return round(val, 2)
    return None


def extract_institute(education_text: str) -> str:
    lines = education_text.split("\n")
    for line in lines:
        stripped = line.strip()
        if len(stripped) > 5 and not stripped.isdigit():
            return stripped.lower()
    return ""


def extract_bullet_points(sections: dict[str, str]) -> list[str]:
    bullets = []
    target_sections = ["experience", "projects", "achievements"]
    bullet_pattern = re.compile(r"^[\•\-\*\>\◦\▪\➢\►\→]?\s*(.+)$")
    for sec in target_sections:
        text = sections.get(sec, "")
        for line in text.split("\n"):
            stripped = line.strip()
            if len(stripped) > 20:
                match = bullet_pattern.match(stripped)
                if match:
                    bullets.append(match.group(1).strip())
    return bullets