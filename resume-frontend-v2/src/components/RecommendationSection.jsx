function Block({ title, content, accentColor, tagLabel }) {
  if (!content) return null;
  const lines = content.split("\n").filter(Boolean);

  return (
    <div style={{
      padding: 18, borderRadius: 10,
      background: "var(--surface)", border: "1px solid var(--border)",
    }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 14 }}>
        <p style={{ fontSize: 13, fontWeight: 700, color: accentColor }}>{title}</p>
        <span className="mono" style={{
          fontSize: 10, padding: "3px 8px", borderRadius: 5,
          background: `${accentColor}15`, color: accentColor,
          border: `1px solid ${accentColor}30`,
        }}>
          {tagLabel}
        </span>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
        {lines.map((line, i) => (
          <p key={i} style={{ fontSize: 13, color: "var(--txt)", lineHeight: 1.65 }}>{line}</p>
        ))}
      </div>
    </div>
  );
}

export default function RecommendationSection({ aiFeedback, aiSkillRecs, aiProjectResult }) {
  const projectFeedback = aiProjectResult?.ai_project_feedback;
  const aiScore         = aiProjectResult?.ai_project_score;

  const hasContent = aiFeedback || aiSkillRecs || (typeof projectFeedback === "object" && projectFeedback);
  if (!hasContent) return null;

  return (
    <div className="card fade-in delay-5">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20 }}>
        <p className="section-label">AI Recommendations</p>
        {aiScore != null && (
          <span className="tag tag-blue">Gemini project score: {aiScore}/100</span>
        )}
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
        {aiFeedback && (
          <Block
            title="Prioritized Improvements"
            content={aiFeedback}
            accentColor="var(--blue)"
            tagLabel="Gemini AI"
          />
        )}
        {aiSkillRecs && (
          <Block
            title="Skills to Add in 2025"
            content={aiSkillRecs}
            accentColor="var(--accent)"
            tagLabel="Gemini AI"
          />
        )}
        {typeof projectFeedback === "object" && projectFeedback?.recommendation && (
          <Block
            title="Project Recommendation"
            content={projectFeedback.recommendation}
            accentColor="var(--amber)"
            tagLabel="Project AI"
          />
        )}
      </div>
    </div>
  );
}
