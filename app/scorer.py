import re
from app.config import (
    SECTION_WEIGHTS, CGPA_SCORE_MAP, TIER1_INSTITUTES,
    PROJECT_COMPLEXITY_SIGNALS, WEAK_BULLET_PATTERNS, STRONG_BULLET_PATTERNS
)


def extract_unique_keyword_matches(text: str, keyword_dict: dict) -> dict[str, int]:
    text_lower = text.lower()
    matched = {}
    for kw, weight in keyword_dict.items():
        kw_lower = kw.lower()
        occurrences = len(re.findall(re.escape(kw_lower), text_lower))
        if occurrences > 0:
            matched[kw] = weight
    return matched


def score_section(matched: dict[str, int], full_dict: dict[str, int]) -> float:
    total_possible = sum(full_dict.values())
    if total_possible == 0:
        return 0.0
    matched_weight = sum(matched.values())
    return round(min((matched_weight / total_possible) * 100, 100), 2)


def score_project_complexity(projects_text: str) -> float:
    if not projects_text.strip():
        return 0.0
    text_lower = projects_text.lower()
    total_possible = sum(PROJECT_COMPLEXITY_SIGNALS.values())
    matched_weight = sum(
        weight for signal, weight in PROJECT_COMPLEXITY_SIGNALS.items()
        if signal.lower() in text_lower
    )
    complexity_score = min((matched_weight / total_possible) * 100, 100)
    return round(complexity_score, 2)


def score_projects_combined(
    projects_text: str,
    project_keywords: dict,
    semantic_project_score: float | None = None,
) -> tuple[float, dict]:
    keyword_matched = extract_unique_keyword_matches(projects_text, project_keywords)
    keyword_score = score_section(keyword_matched, project_keywords)
    complexity_score = score_project_complexity(projects_text)

    if semantic_project_score is not None:
        final = (keyword_score * 0.35) + (complexity_score * 0.25) + (semantic_project_score * 0.40)
    else:
        final = (keyword_score * 0.50) + (complexity_score * 0.50)

    breakdown = {
        "keyword_score": keyword_score,
        "complexity_score": complexity_score,
        "semantic_score": semantic_project_score,
        "combined": round(final, 2),
    }
    return round(final, 2), breakdown


def analyze_bullet_quality(bullet_points: list[str]) -> dict:
    if not bullet_points:
        return {"weak_count": 0, "strong_count": 0, "quality_score": 50.0, "weak_bullets": []}

    weak_bullets = []
    strong_count = 0

    for bullet in bullet_points:
        bullet_lower = bullet.lower()
        is_weak = any(re.search(p, bullet_lower) for p in WEAK_BULLET_PATTERNS)
        is_strong = any(re.search(p, bullet_lower) for p in STRONG_BULLET_PATTERNS)
        if is_weak and not is_strong:
            weak_bullets.append(bullet[:100])
        if is_strong:
            strong_count += 1

    total = len(bullet_points)
    weak_count = len(weak_bullets)
    quality_score = round(((total - weak_count) / total) * 100, 2) if total > 0 else 50.0

    return {
        "weak_count": weak_count,
        "strong_count": strong_count,
        "total_bullets": total,
        "quality_score": quality_score,
        "weak_bullets": weak_bullets[:5],
    }


def score_education(cgpa: float | None, institute_text: str) -> float:
    cgpa_score = _cgpa_to_score(cgpa)
    institute_score = _institute_to_score(institute_text)
    return round((cgpa_score * 0.70) + (institute_score * 0.30), 2)


def calculate_final_score(section_scores: dict[str, float]) -> float:
    final = sum(
        section_scores.get(section, 0) * weight
        for section, weight in SECTION_WEIGHTS.items()
    )
    return round(final, 2)


def build_score_breakdown(section_scores: dict[str, float]) -> dict:
    breakdown = {}
    for section, weight in SECTION_WEIGHTS.items():
        raw = section_scores.get(section, 0)
        contribution = round(raw * weight, 2)
        breakdown[section] = {
            "raw_score": raw,
            "weight": weight,
            "contribution": contribution,
        }
    return breakdown


def score_all_sections(
    sections: dict[str, str],
    skills_dict: dict,
    project_keywords: dict,
    experience_keywords: dict,
    cgpa: float | None,
    institute_text: str,
    bullet_points: list[str],
    semantic_project_score: float | None = None,
) -> dict:
    full_text = " ".join(sections.values())
    skills_text = sections.get("skills", full_text)
    projects_text = sections.get("projects", "")
    experience_text = sections.get("experience", "")

    matched_skills = extract_unique_keyword_matches(skills_text, skills_dict)
    matched_experience = extract_unique_keyword_matches(experience_text, experience_keywords)

    skills_score = score_section(matched_skills, skills_dict)
    projects_score, project_breakdown = score_projects_combined(
        projects_text, project_keywords, semantic_project_score
    )
    experience_score = score_section(matched_experience, experience_keywords)
    education_score = score_education(cgpa, institute_text)
    bullet_quality = analyze_bullet_quality(bullet_points)

    section_scores = {
        "skills":     skills_score,
        "projects":   projects_score,
        "experience": experience_score,
        "education":  education_score,
    }

    final_score = calculate_final_score(section_scores)
    score_breakdown = build_score_breakdown(section_scores)

    return {
        "section_scores": section_scores,
        "final_score": final_score,
        "score_breakdown": score_breakdown,
        "project_breakdown": project_breakdown,
        "bullet_quality": bullet_quality,
        "matched_skills": matched_skills,
        "matched_experience": matched_experience,
    }


def _cgpa_to_score(cgpa: float | None) -> float:
    if cgpa is None:
        return 60.0
    for (low, high), score in CGPA_SCORE_MAP.items():
        if low <= cgpa < high:
            return float(score)
    return 40.0


def _institute_to_score(institute_text: str) -> float:
    lower = institute_text.lower()
    for tier1 in TIER1_INSTITUTES:
        if tier1 in lower:
            return 100.0
    return 60.0