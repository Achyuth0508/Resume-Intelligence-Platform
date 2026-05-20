import argparse
from app.parser import extract_text_from_pdf, split_into_sections, extract_cgpa, extract_institute, extract_bullet_points
from app.detector import detect_role, get_role_config
from app.scorer import score_all_sections
from app.semantic import SemanticMatcher
from app.analyzer import detect_missing_skills, build_full_report
from app.gemini import score_projects_with_ai, generate_ai_resume_feedback, recommend_skills_for_role


def run_analysis(pdf_path: str, jd_text: str | None = None, skip_semantic: bool = False, skip_ai: bool = False):
    print("\n" + "═" * 65)
    print("   RESUME INTELLIGENCE PLATFORM  v2.0")
    print("═" * 65)

    print("\n[1/6] Parsing resume...")
    raw_text = extract_text_from_pdf(pdf_path)
    sections = split_into_sections(raw_text)
    cgpa = extract_cgpa(raw_text)
    institute = extract_institute(sections.get("education", raw_text[:500]))
    bullet_points = extract_bullet_points(sections)

    print(f"  Sections found : {', '.join(sections.keys())}")
    print(f"  CGPA extracted : {cgpa if cgpa else 'Not found'}")
    print(f"  Bullets found  : {len(bullet_points)}")

    print("\n[2/6] Detecting role...")
    role_info = detect_role(sections)
    role = role_info["role"]
    print(f"  Role     : {role}")
    print(f"  Confidence : {role_info['confidence'] * 100:.0f}%")
    print(f"  AI/ML raw score : {role_info['aiml_score']}  |  SDE raw score : {role_info['sde_score']}")

    skills_dict, project_keywords, experience_keywords = get_role_config(role)

    semantic_project_score = None
    jd_result = None
    semantic_skill_result = None
    matcher = None

    if not skip_semantic:
        print("\n[3/6] Running semantic analysis (loading model)...")
        matcher = SemanticMatcher()
        semantic_project_score = matcher.score_projects_semantically(
            sections.get("projects", ""), role
        )
        print(f"  Semantic project score : {semantic_project_score}%")

        if jd_text:
            jd_result = matcher.resume_jd_score(raw_text, jd_text)
            print(f"  JD similarity score    : {jd_result['similarity_score']}%")
            print(f"  Interpretation         : {jd_result['interpretation']}")

        target_skills = list(skills_dict.keys())
        semantic_skill_result = matcher.semantic_skill_match(raw_text, target_skills)
        print(f"  Semantic skill match   : {semantic_skill_result['semantic_score']}%")
    else:
        print("\n[3/6] Semantic analysis skipped.")

    print("\n[4/6] Scoring sections...")
    score_info = score_all_sections(
        sections, skills_dict, project_keywords, experience_keywords,
        cgpa, institute, bullet_points, semantic_project_score
    )

    sec = score_info["section_scores"]
    bd = score_info["score_breakdown"]
    print(f"\n  {'Section':<12} {'Raw Score':>10}  {'Weight':>8}  {'Contribution':>14}")
    print(f"  {'─'*12} {'─'*10}  {'─'*8}  {'─'*14}")
    for section in ["skills", "projects", "experience", "education"]:
        raw = bd[section]["raw_score"]
        weight = bd[section]["weight"]
        contrib = bd[section]["contribution"]
        print(f"  {section.capitalize():<12} {raw:>9.1f}%  {weight:>7.0%}  {contrib:>13.2f}")
    print(f"  {'─'*49}")
    print(f"  {'FINAL SCORE':<12} {'':>10}  {'':>8}  {score_info['final_score']:>13.2f}%")

    proj_bd = score_info.get("project_breakdown", {})
    if proj_bd:
        print(f"\n  Project score breakdown:")
        print(f"    Keyword match    : {proj_bd.get('keyword_score', 0):.1f}%")
        print(f"    Complexity score : {proj_bd.get('complexity_score', 0):.1f}%")
        if proj_bd.get("semantic_score") is not None:
            print(f"    Semantic score   : {proj_bd.get('semantic_score', 0):.1f}%")
        print(f"    Combined         : {proj_bd.get('combined', 0):.1f}%")

    bq = score_info.get("bullet_quality", {})
    if bq:
        print(f"\n  Bullet quality: {bq.get('quality_score', 0):.1f}%  "
              f"({bq.get('strong_count', 0)} strong / {bq.get('weak_count', 0)} weak out of {bq.get('total_bullets', 0)})")

    ai_project_result = None
    ai_feedback = None
    ai_skill_recommendations = None

    if not skip_ai:
        print("\n[5/6] Running Gemini AI analysis...")
        ai_project_result = score_projects_with_ai(sections.get("projects", ""), role)
        print(f"  AI project score : {ai_project_result.get('ai_project_score', 'N/A')}/100")
        ai_feedback_text = generate_ai_resume_feedback(
            role=role,
            section_scores=sec,
            matched_skills=list(score_info["matched_skills"].keys()),
            missing_skills=detect_missing_skills(score_info["matched_skills"], skills_dict),
            bullet_quality=bq,
            jd_similarity=jd_result["similarity_score"] if jd_result else None,
            projects_text=sections.get("projects", ""),
            experience_text=sections.get("experience", ""),
        )
        ai_feedback = ai_feedback_text
        ai_skill_recommendations = recommend_skills_for_role(
            role, list(score_info["matched_skills"].keys())
        )
    else:
        print("\n[5/6] AI analysis skipped (--skip-ai flag).")

    print("\n[6/6] Building final report...")
    missing_skills = detect_missing_skills(score_info["matched_skills"], skills_dict)

    jd_ranked_missing = None
    if matcher and jd_text and missing_skills:
        jd_ranked_missing = matcher.rank_missing_skills_by_jd(missing_skills, jd_text)

    report = build_full_report(
        role_info, score_info, missing_skills, jd_result,
        semantic_skill_result, sections, ai_project_result,
        ai_feedback, ai_skill_recommendations, jd_ranked_missing
    )

    _print_report(report)
    return report


def _print_report(report: dict):
    print("\n" + "═" * 65)
    print("   FULL ANALYSIS REPORT")
    print("═" * 65)

    print("\n── Matched Skills (keyword) ────────────────────────────────────")
    matched = report["scores"].get("matched_skills", {})
    if matched:
        for skill, weight in matched.items():
            print(f"  ✓  {skill:<28} weight: {weight}")
    else:
        print("  No skills matched via keyword search.")

    sem = report.get("semantic_skill_match")
    if sem:
        print(f"\n── Semantic Skill Match ─── Score: {sem['semantic_score']}% ──────────────")
        print("  Semantically matched:")
        for skill, sim in sem["matched"][:6]:
            print(f"    ≈  {skill:<28} similarity: {sim}")
        if sem["missing"]:
            print("  Semantically missing:")
            for skill, sim in sem["missing"][:6]:
                print(f"    ✗  {skill:<28} similarity: {sim}")

    print("\n── Missing High-Value Skills ───────────────────────────────────")
    jd_ranked = report.get("jd_ranked_missing")
    if jd_ranked:
        print("  (ranked by JD relevance)")
        for skill, score in jd_ranked[:8]:
            print(f"  ✗  {skill:<28} JD relevance: {score}")
    else:
        for skill in report["missing_skills"]:
            print(f"  ✗  {skill}")

    ai_proj = report.get("ai_project_result")
    if ai_proj and isinstance(ai_proj.get("ai_project_feedback"), dict):
        fb = ai_proj["ai_project_feedback"]
        print(f"\n── AI Project Analysis ─── Score: {ai_proj.get('ai_project_score')}/100 ────")
        print(f"  Complexity     : {fb.get('complexity_level', 'N/A')}")
        print(f"  Deployment     : {'Yes' if fb.get('deployment_evidence') else 'No'}")
        print(f"  AI usage       : {'Yes' if fb.get('ai_usage_detected') else 'No'}")
        print(f"  Has metrics    : {'Yes' if fb.get('metric_presence') else 'No'}")
        print(f"  Scalability    : {'Yes' if fb.get('scalability_signals') else 'No'}")
        if fb.get("strongest_project"):
            print(f"  Best project   : {fb['strongest_project']}")
        if fb.get("critical_gap"):
            print(f"  Critical gap   : {fb['critical_gap']}")
        if fb.get("recommendation"):
            print(f"  Recommendation : {fb['recommendation']}")

    bq = report["scores"].get("bullet_quality", {})
    if bq and bq.get("weak_bullets"):
        print(f"\n── Weak Bullet Points Detected ─────────────────────────────────")
        for b in bq["weak_bullets"]:
            print(f"  ✗  {b[:90]}")

    if report.get("weaknesses"):
        print(f"\n── Weaknesses ──────────────────────────────────────────────────")
        for i, w in enumerate(report["weaknesses"], 1):
            print(f"  {i}. {w}")

    if report.get("ai_feedback"):
        print(f"\n── AI Feedback (Gemini) ────────────────────────────────────────")
        print(report["ai_feedback"])

    if report.get("ai_skill_recommendations"):
        print(f"\n── Skill Recommendations (Gemini) ──────────────────────────────")
        print(report["ai_skill_recommendations"])

    if report.get("jd_match"):
        jd = report["jd_match"]
        print(f"\n── JD Match ────────────────────────────────────────────────────")
        print(f"  Score          : {jd['similarity_score']}%")
        print(f"  Interpretation : {jd['interpretation']}")

    print("\n" + "═" * 65 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resume Intelligence Platform v2")
    parser.add_argument("--resume", required=True, help="Path to resume PDF")
    parser.add_argument("--jd", default=None, help="Job description text")
    parser.add_argument("--skip-semantic", action="store_true", help="Skip sentence-transformer model")
    parser.add_argument("--skip-ai", action="store_true", help="Skip Gemini AI calls")
    args = parser.parse_args()

    run_analysis(
        pdf_path=args.resume,
        jd_text=args.jd,
        skip_semantic=args.skip_semantic,
        skip_ai=args.skip_ai,
    )