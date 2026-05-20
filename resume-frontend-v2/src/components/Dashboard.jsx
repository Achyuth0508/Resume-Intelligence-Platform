import ScoreCard          from "./ScoreCard";
import SkillsSection       from "./SkillsSection";
import WeaknessSection     from "./WeaknessSection";
import RecommendationSection from "./RecommendationSection";

export default function Dashboard({ result, onReset }) {
  const { role, scores, missing_skills, jd_match, jd_ranked_missing,
          weaknesses, ai_project_result, ai_feedback,
          ai_skill_recommendations, sections_found } = result;

  return (
    <div style={{ maxWidth: 860, margin: "0 auto" }}>

      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 28, flexWrap: "wrap", gap: 12 }}>
        <div>
          <p className="mono" style={{ fontSize: 11, color: "var(--txt-3)", marginBottom: 4 }}>Analysis complete</p>
          <p style={{ fontSize: 13, color: "var(--txt-2)" }}>
            Sections: <span style={{ color: "var(--txt)" }}>{sections_found?.join(", ")}</span>
          </p>
        </div>
        <button
          onClick={onReset}
          style={{
            padding: "8px 16px", borderRadius: 8, fontSize: 13, fontWeight: 600,
            background: "var(--card)", border: "1px solid var(--border-hi)",
            color: "var(--txt-2)", cursor: "pointer", fontFamily: "'Syne', sans-serif",
          }}
        >
          ← Analyze another
        </button>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16, marginBottom: 16 }}>
        <div style={{ gridColumn: "1 / -1" }}>
          <ScoreCard scores={scores} roleInfo={role} />
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))", gap: 16 }}>
        <SkillsSection
          scores={scores}
          missingSkills={missing_skills}
          jdMatch={jd_match}
          jdRankedMissing={jd_ranked_missing}
        />

        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <WeaknessSection
            weaknesses={weaknesses}
            bulletQuality={scores?.bullet_quality}
          />
          <RecommendationSection
            aiFeedback={ai_feedback}
            aiSkillRecs={ai_skill_recommendations}
            aiProjectResult={ai_project_result}
          />
        </div>
      </div>
    </div>
  );
}
