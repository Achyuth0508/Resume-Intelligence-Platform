import re
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"


def split_sentences(text: str) -> list[str]:
    chunks = re.split(r"[.\n•\-]", text)

    cleaned = []

    for chunk in chunks:
        chunk = chunk.strip()

        if len(chunk) > 5:
            cleaned.append(chunk)

    return cleaned


class SemanticMatcher:

    def __init__(self):
        self.model = SentenceTransformer(MODEL_NAME)

    def embed(self, text: str) -> np.ndarray:
        vec = self.model.encode(text, convert_to_numpy=True)
        norm = np.linalg.norm(vec)
        return vec / (norm + 1e-10)

    def embed_batch(self, texts: list[str]) -> list[np.ndarray]:
        vecs = self.model.encode(texts, convert_to_numpy=True)
        return [v / (np.linalg.norm(v) + 1e-10) for v in vecs]

    def cosine_sim(self, a: np.ndarray, b: np.ndarray) -> float:
        return float(np.dot(a, b))

    def resume_jd_score(self, resume_text: str, jd_text: str) -> dict:
        resume_vec = self.embed(resume_text)
        jd_vec = self.embed(jd_text)

        raw = self.cosine_sim(resume_vec, jd_vec)

        score = round(((raw + 1) / 2) * 100, 2)

        return {
            "similarity_score": score,
            "interpretation": _interpret_jd_similarity(score),
        }

    def semantic_skill_match(
        self,
        resume_text: str,
        target_skills: list[str],
        threshold: float = 0.45,
    ) -> dict:

        chunks = split_sentences(resume_text)

        if not chunks:
            return {
                "semantic_score": 0.0,
                "matched": [],
                "missing": [
                    {
                        "skill": skill,
                        "score": 0.0,
                        "evidence": "",
                    }
                    for skill in target_skills
                ],
            }

        chunk_vecs = self.embed_batch(chunks)
        skill_vecs = self.embed_batch(target_skills)

        matched = []
        missing = []

        for skill, skill_vec in zip(target_skills, skill_vecs):

            sims = [
                self.cosine_sim(skill_vec, chunk_vec)
                for chunk_vec in chunk_vecs
            ]

            best_idx = int(np.argmax(sims))
            best_sim = float(sims[best_idx])
            best_chunk = chunks[best_idx]

            result = {
                "skill": skill,
                "score": round(best_sim, 3),
                "evidence": best_chunk,
            }

            if best_sim >= threshold:
                matched.append(result)
            else:
                missing.append(result)

        matched.sort(key=lambda x: x["score"], reverse=True)
        missing.sort(key=lambda x: x["score"], reverse=True)

        all_scores = [x["score"] for x in matched + missing]

        semantic_score = (
            round(float(np.mean(all_scores)) * 100, 2)
            if all_scores else 0.0
        )

        return {
            "semantic_score": semantic_score,
            "matched": matched,
            "missing": missing,
        }

    def score_projects_semantically(
        self,
        projects_text: str,
        role: str,
    ) -> float:

        if not projects_text.strip():
            return 0.0

        if role == "AI/ML":
            reference_descriptions = [
                "RAG system with vector database and LLM",
                "NLP model for text classification deployed with FastAPI",
                "computer vision model trained on custom dataset with evaluation metrics",
                "fine-tuned transformer model for downstream task",
                "end-to-end machine learning pipeline with data preprocessing and model deployment",
                "LangChain chatbot with document retrieval and conversation memory",
            ]
        else:
            reference_descriptions = [
                "scalable REST API with authentication and database integration",
                "microservices architecture with Docker and Kubernetes deployment",
                "full stack web application with React frontend and Node.js backend",
                "distributed system with message queue and caching layer",
                "CI/CD pipeline with automated testing and deployment",
                "real-time WebSocket application with load balancing",
            ]

        project_vec = self.embed(projects_text)
        ref_vecs = self.embed_batch(reference_descriptions)

        similarities = [
            self.cosine_sim(project_vec, ref_vec)
            for ref_vec in ref_vecs
        ]

        avg_sim = float(np.mean(similarities))

        score = round(((avg_sim + 1) / 2) * 100, 2)

        return min(score, 100.0)

    def rank_missing_skills_by_jd(
        self,
        missing_skills: list[str],
        jd_text: str,
    ) -> list[tuple[str, float]]:

        if not missing_skills or not jd_text:
            return [(s, 0.0) for s in missing_skills]

        jd_vec = self.embed(jd_text)
        skill_vecs = self.embed_batch(missing_skills)

        scored = [
            (
                skill,
                round(self.cosine_sim(sv, jd_vec), 3)
            )
            for skill, sv in zip(missing_skills, skill_vecs)
        ]

        return sorted(
            scored,
            key=lambda x: x[1],
            reverse=True
        )


def _interpret_jd_similarity(score: float) -> str:

    if score >= 80:
        return "Excellent match — strong alignment with the job description."

    elif score >= 65:
        return "Good match — resume covers most key requirements."

    elif score >= 50:
        return "Moderate match — some relevant experience but gaps exist."

    elif score >= 35:
        return "Weak match — significant alignment gaps with the JD."

    else:
        return "Poor match — resume does not align well with this role."