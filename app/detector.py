from app.config import (
    AIML_SKILLS, SDE_SKILLS,
    AIML_PROJECT_KEYWORDS, SDE_PROJECT_KEYWORDS,
    AIML_EXPERIENCE_KEYWORDS, SDE_EXPERIENCE_KEYWORDS,
)


def detect_role(sections: dict[str, str]) -> dict:
    skills_text = sections.get("skills", "") * 2
    projects_text = sections.get("projects", "")
    experience_text = sections.get("experience", "")

    aiml_total = 0.0
    sde_total = 0.0

    aiml_total += _score_text(skills_text, AIML_SKILLS) * 2.0
    sde_total  += _score_text(skills_text, SDE_SKILLS) * 2.0

    aiml_total += _score_text(projects_text, AIML_PROJECT_KEYWORDS) * 1.0
    sde_total  += _score_text(projects_text, SDE_PROJECT_KEYWORDS) * 1.0

    aiml_total += _score_text(experience_text, AIML_EXPERIENCE_KEYWORDS) * 0.8
    sde_total  += _score_text(experience_text, SDE_EXPERIENCE_KEYWORDS) * 0.8

    total = aiml_total + sde_total
    if total == 0:
        return {"role": "SDE", "confidence": 0.5, "aiml_score": 0, "sde_score": 0}

    aiml_confidence = aiml_total / total
    role = "AI/ML" if aiml_confidence >= 0.5 else "SDE"
    confidence = aiml_confidence if role == "AI/ML" else (1 - aiml_confidence)

    return {
        "role": role,
        "confidence": round(confidence, 2),
        "aiml_score": round(aiml_total, 1),
        "sde_score": round(sde_total, 1),
    }


def get_role_config(role: str) -> tuple[dict, dict, dict]:
    if role == "AI/ML":
        return AIML_SKILLS, AIML_PROJECT_KEYWORDS, AIML_EXPERIENCE_KEYWORDS
    return SDE_SKILLS, SDE_PROJECT_KEYWORDS, SDE_EXPERIENCE_KEYWORDS


def _score_text(text: str, keyword_dict: dict) -> float:
    text_lower = text.lower()
    return sum(
        weight for keyword, weight in keyword_dict.items()
        if keyword.lower() in text_lower
    )