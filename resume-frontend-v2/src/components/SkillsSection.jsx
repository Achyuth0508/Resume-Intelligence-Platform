function Chip({ label, weight, variant }) {
  const styles = {
    green: { bg: "var(--green-bg)", bd: "var(--green-bd)", col: "var(--green)" },
    red:   { bg: "var(--red-bg)",   bd: "var(--red-bd)",   col: "var(--red)" },
  };
  const s = styles[variant];
  return (
    <div style={{
      display: "inline-flex", alignItems: "center", gap: 6,
      padding: "5px 10px", borderRadius: 7,
      background: s.bg, border: `1px solid ${s.bd}`,
      fontSize: 12, fontWeight: 600, color: s.col,
      fontFamily: "'DM Mono', monospace",
    }}>
      <span style={{ width: 5, height: 5, borderRadius: "50%", background: s.col, flexShrink: 0 }} />
      {label}
      {weight != null && <span style={{ opacity: 0.55 }}>+{weight}</span>}
    </div>
  );
}

function JdScore({ score }) {
  const col = score >= 70 ? "var(--green)" : score >= 50 ? "var(--amber)" : "var(--red)";
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
      <div style={{ flex: 1, height: 5, borderRadius: 9, background: "var(--surface)", overflow: "hidden" }}>
        <div style={{
          height: "100%", width: `${score}%`, borderRadius: 9,
          background: col, transition: "width 0.9s ease",
          boxShadow: `0 0 8px ${col}55`,
        }} />
      </div>
      <span className="mono" style={{ fontSize: 14, fontWeight: 700, color: col, minWidth: 44, textAlign: "right" }}>
        {score}%
      </span>
    </div>
  );
}

export default function SkillsSection({ scores, missingSkills, jdMatch, jdRankedMissing }) {
  const matched  = scores?.matched_skills  ? Object.entries(scores.matched_skills)  : [];
  const missing  = jdRankedMissing?.length
    ? jdRankedMissing.map(([s]) => s)
    : (missingSkills || []);

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>

      {jdMatch && (
        <div className="card fade-in delay-2">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
            <p className="section-label">JD Match Score</p>
            <span className="mono" style={{ fontSize: 11, color: "var(--txt-3)" }}>semantic similarity</span>
          </div>
          <JdScore score={jdMatch.similarity_score} />
          <p style={{ fontSize: 13, color: "var(--txt-2)", marginTop: 10 }}>{jdMatch.interpretation}</p>
        </div>
      )}

      <div className="card fade-in delay-3">
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
          <p className="section-label">Matched Skills</p>
          <span className="tag tag-green">{matched.length} found</span>
        </div>
        {matched.length === 0
          ? <p style={{ fontSize: 13, color: "var(--txt-3)" }}>No keyword matches found in skills section.</p>
          : (
            <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
              {matched.map(([skill, weight]) => (
                <Chip key={skill} label={skill} weight={weight} variant="green" />
              ))}
            </div>
          )}
      </div>

      <div className="card fade-in delay-4">
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 16 }}>
          <p className="section-label">Missing Skills</p>
          <span className="tag tag-red">{missing.length} gaps</span>
        </div>
        {missing.length === 0
          ? <p style={{ fontSize: 13, color: "var(--txt-3)" }}>No critical skill gaps detected.</p>
          : (
            <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
              {missing.map((skill) => (
                <Chip key={skill} label={skill} variant="red" />
              ))}
            </div>
          )}
        {jdRankedMissing?.length > 0 && (
          <p className="mono" style={{ fontSize: 11, color: "var(--txt-3)", marginTop: 12 }}>
            ↑ ranked by relevance to your job description
          </p>
        )}
      </div>
    </div>
  );
}
