WEAKNESS_THRESHOLD = 50.0


def detect_missing_skills(
    matched_skills: dict[str, int],
    full_skills_dict: dict[str, int],
    top_n: int = 8,
) -> list[str]:
    missing = {
        skill: weight
        for skill, weight in full_skills_dict.items()
        if skill not in matched_skills
    }
    sorted_missing = sorted(missing.items(), key=lambda x: x[1], reverse=True)
    return [skill for skill, _ in sorted_missing[:top_n]]


def analyze_weaknesses(section_scores: dict[str, float], bullet_quality: dict) -> list[str]:
    weaknesses = []
    messages = {
        "skills": "Skills section is below threshold — add more relevant tools and technologies explicitly.",
        "projects": "Projects score is low — add projects with clear tech stack, deployment evidence, and measurable outcomes.",
        "experience": "Experience section is weak — add internships, research roles, or open source contributions.",
        "education": "Education score is lower than expected — ensure CGPA and institute name are clearly visible.",
    }
    for section, score in section_scores.items():
        if score < WEAKNESS_THRESHOLD:
            weaknesses.append(messages.get(section, f"{section} needs improvement."))

    quality_score = bullet_quality.get("quality_score", 100)
    weak_count = bullet_quality.get("weak_count", 0)
    if quality_score < 60 and weak_count > 0:
        weaknesses.append(
            f"{weak_count} weak bullet points detected using passive language like "
            "'worked on', 'responsible for', 'helped with'. Replace with action verbs and metrics."
        )

    return weaknesses


def build_full_report(
    role_info: dict,
    score_info: dict,
    missing_skills: list[str],
    jd_result: dict | None,
    semantic_skill_result: dict | None,
    sections: dict[str, str],
    ai_project_result: dict | None,
    ai_feedback: str | None,
    ai_skill_recommendations: str | None,
    jd_ranked_missing: list[tuple[str, float]] | None,
) -> dict:
    section_scores = score_info["section_scores"]
    bullet_quality = score_info.get("bullet_quality", {})
    weaknesses = analyze_weaknesses(section_scores, bullet_quality)

    return {
        "role": role_info,
        "scores": score_info,
        "missing_skills": missing_skills,
        "jd_ranked_missing": jd_ranked_missing or [],
        "weaknesses": weaknesses,
        "jd_match": jd_result,
        "semantic_skill_match": semantic_skill_result,
        "ai_project_result": ai_project_result,
        "ai_feedback": ai_feedback,
        "ai_skill_recommendations": ai_skill_recommendations,
        "sections_found": list(sections.keys()),
    }