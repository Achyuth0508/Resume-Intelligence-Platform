function scoreColor(s) {
  if (s >= 70) return "var(--green)";
  if (s >= 45) return "var(--amber)";
  return "var(--red)";
}

function scoreLabel(s) {
  if (s >= 70) return "Strong — likely to pass ATS filters";
  if (s >= 45) return "Moderate — needs some improvement";
  return "Below threshold — significant gaps";
}

function Ring({ score }) {
  const r   = 48;
  const c   = 2 * Math.PI * r;
  const arc = c * 0.75;
  const col = scoreColor(score);

  return (
    <div style={{ position: "relative", width: 128, height: 128, flexShrink: 0 }}>
      <svg width="128" height="128" viewBox="0 0 128 128">
        <circle cx="64" cy="64" r={r} fill="none" stroke="var(--surface)" strokeWidth="9"
          strokeDasharray={`${arc} ${c - arc}`} strokeDashoffset={c * 0.125}
          strokeLinecap="round" transform="rotate(135 64 64)" />
        <circle cx="64" cy="64" r={r} fill="none" stroke={col} strokeWidth="9"
          strokeDasharray={`${(score / 100) * arc} ${c - (score / 100) * arc}`}
          strokeDashoffset={c * 0.125} strokeLinecap="round" transform="rotate(135 64 64)"
          style={{ transition: "stroke-dasharray 1s ease", filter: `drop-shadow(0 0 6px ${col}66)` }} />
      </svg>
      <div style={{ position: "absolute", inset: 0, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
        <span className="mono" style={{ fontSize: 26, fontWeight: 700, color: col, lineHeight: 1 }}>{score}</span>
        <span className="mono" style={{ fontSize: 11, color: "var(--txt-3)" }}>/100</span>
      </div>
    </div>
  );
}

function Bar({ label, score, weight, contribution }) {
  const col = scoreColor(score);
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <span style={{ fontSize: 13, fontWeight: 600, textTransform: "capitalize" }}>{label}</span>
        <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
          <span className="mono" style={{ fontSize: 11, color: "var(--txt-3)" }}>{Math.round(weight * 100)}% weight</span>
          <span className="mono" style={{ fontSize: 13, fontWeight: 600, color: col }}>{score?.toFixed(1)}%</span>
        </div>
      </div>
      <div style={{ height: 5, borderRadius: 9, background: "var(--surface)", overflow: "hidden" }}>
        <div style={{
          height: "100%", borderRadius: 9, width: `${score}%`,
          background: col, transition: "width 0.9s ease",
          boxShadow: `0 0 8px ${col}55`,
        }} />
      </div>
      <span className="mono" style={{ fontSize: 11, color: "var(--txt-3)", textAlign: "right" }}>
        +{contribution?.toFixed(2)} pts
      </span>
    </div>
  );
}

export default function ScoreCard({ scores, roleInfo }) {
  if (!scores) return null;
  const { final_score, score_breakdown } = scores;
  const col = scoreColor(final_score);

  return (
    <div className="card fade-in delay-1">
      <p className="section-label" style={{ marginBottom: 20 }}>ATS Score</p>

      <div style={{ display: "flex", gap: 24, alignItems: "center", flexWrap: "wrap", marginBottom: 28 }}>
        <Ring score={final_score} />
        <div style={{ flex: 1, minWidth: 0 }}>
          {roleInfo && (
            <div style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 10, flexWrap: "wrap" }}>
              <span className={`tag tag-blue`}>{roleInfo.role}</span>
              <span className="mono" style={{ fontSize: 12, color: "var(--txt-2)" }}>
                {Math.round(roleInfo.confidence * 100)}% confidence
              </span>
            </div>
          )}
          <p style={{ fontWeight: 700, fontSize: 15, color: col }}>{scoreLabel(final_score)}</p>
          <p className="mono" style={{ fontSize: 12, color: "var(--txt-3)", marginTop: 4 }}>
            Weighted: skills 35% · projects 35% · experience 20% · education 10%
          </p>
        </div>
      </div>

      {score_breakdown && (
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          {Object.entries(score_breakdown).map(([sec, d]) => (
            <Bar key={sec} label={sec} score={d.raw_score} weight={d.weight} contribution={d.contribution} />
          ))}
        </div>
      )}
    </div>
  );
}
