import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

_client = None


def _get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        genai.configure(api_key=api_key)
        _client = genai.GenerativeModel("gemini-2.0-flash")
    return _client


def score_projects_with_ai(projects_text: str, role: str) -> dict:
    if not projects_text.strip():
        return {"ai_project_score": 0, "ai_project_feedback": "No projects section found."}

    prompt = f"""You are a senior technical recruiter evaluating a {role} candidate's projects section.

Analyze the following projects text and return a JSON response only — no explanation, no markdown, just raw JSON.

Projects text:
{projects_text[:2000]}

Evaluate and return exactly this JSON structure:
{{
  "score": <integer 0-100>,
  "tech_stack_quality": <integer 0-100>,
  "complexity_level": "<low|medium|high>",
  "deployment_evidence": <true|false>,
  "ai_usage_detected": <true|false>,
  "scalability_signals": <true|false>,
  "metric_presence": <true|false>,
  "strongest_project": "<one sentence about the best project>",
  "critical_gap": "<one sentence on what is missing>",
  "recommendation": "<one actionable sentence>"
}}

Scoring guide:
- 80-100: Production-grade projects with deployment, metrics, real users, complex architecture
- 60-79: Solid projects with clear tech stack, some deployment or API work
- 40-59: Standard academic/personal projects, basic implementation
- 20-39: Simple projects, no deployment, no clear impact
- 0-19: Very basic or unclear projects"""

    try:
        client = _get_client()
        response = client.generate_content(prompt)
        raw = response.text.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(raw)
        return {
            "ai_project_score": result.get("score", 0),
            "ai_project_feedback": result,
        }
    except Exception as e:
        return {
            "ai_project_score": 0,
            "ai_project_feedback": f"AI scoring failed: {str(e)}",
        }


def generate_ai_resume_feedback(
    role: str,
    section_scores: dict,
    matched_skills: list[str],
    missing_skills: list[str],
    bullet_quality: dict,
    jd_similarity: float | None,
    projects_text: str,
    experience_text: str,
) -> str:
    weak_bullets = bullet_quality.get("weak_bullets", [])
    weak_sample = "\n".join(weak_bullets[:3]) if weak_bullets else "None detected"

    jd_line = f"JD similarity score: {jd_similarity:.1f}%" if jd_similarity else "No JD provided"

    prompt = f"""You are an expert AI/ML career coach helping a student crack top tech company placements.

Role targeting: {role}

Resume analysis data:
- Skills score: {section_scores.get('skills', 0)}%
- Projects score: {section_scores.get('projects', 0)}%
- Experience score: {section_scores.get('experience', 0)}%
- Education score: {section_scores.get('education', 0)}%
- Bullet quality score: {bullet_quality.get('quality_score', 0)}%
- {jd_line}

Matched skills: {', '.join(matched_skills[:10]) if matched_skills else 'None'}
Missing high-value skills: {', '.join(missing_skills[:8]) if missing_skills else 'None'}

Sample weak bullets found:
{weak_sample}

Projects text (first 500 chars):
{projects_text[:500]}

Give exactly 5 specific, prioritized, actionable recommendations numbered 1-5.
Be direct, technical, and specific — no generic advice.
Each recommendation should be 1-2 sentences max.
Focus on what will have the highest impact on getting shortlisted."""

    try:
        client = _get_client()
        response = client.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"AI feedback generation failed: {str(e)}"


def recommend_skills_for_role(role: str, matched_skills: list[str]) -> str:
    prompt = f"""You are a technical recruiter at a top AI/ML product company.

A candidate is targeting {role} roles and already has these skills: {', '.join(matched_skills[:15])}.

List exactly 6 skills they should add to maximize their chances at top companies in 2025.
Format: numbered list, skill name + one sentence on why it matters right now.
Be specific, no generic advice."""

    try:
        client = _get_client()
        response = client.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Skill recommendation failed: {str(e)}"