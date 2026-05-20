export default function WeaknessSection({ weaknesses, bulletQuality }) {
  const hasWeaknesses = weaknesses?.length > 0;
  const weakBullets   = bulletQuality?.weak_bullets || [];
  const qualScore     = bulletQuality?.quality_score;

  if (!hasWeaknesses && weakBullets.length === 0) return null;

  return (
    <div className="card fade-in delay-4">
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20 }}>
        <p className="section-label">Weaknesses</p>
        {qualScore != null && (
          <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
            <span className="mono" style={{ fontSize: 11, color: "var(--txt-3)" }}>bullet quality</span>
            <span className="mono" style={{
              fontSize: 12, fontWeight: 700,
              color: qualScore >= 70 ? "var(--green)" : qualScore >= 45 ? "var(--amber)" : "var(--red)",
            }}>
              {qualScore?.toFixed(0)}%
            </span>
          </div>
        )}
      </div>

      {hasWeaknesses && (
        <div style={{ display: "flex", flexDirection: "column", gap: 8, marginBottom: weakBullets.length ? 20 : 0 }}>
          {weaknesses.map((w, i) => (
            <div key={i} style={{
              display: "flex", gap: 12, padding: "11px 14px", borderRadius: 9,
              background: "var(--red-bg)", border: "1px solid var(--red-bd)",
            }}>
              <span style={{ color: "var(--red)", flexShrink: 0, fontWeight: 700 }}>!</span>
              <p style={{ fontSize: 13, color: "var(--txt)", lineHeight: 1.55 }}>{w}</p>
            </div>
          ))}
        </div>
      )}

      {weakBullets.length > 0 && (
        <>
          <p style={{ fontSize: 12, fontWeight: 600, color: "var(--red)", marginBottom: 10 }}>
            Weak bullet points — replace with action verbs + metrics
          </p>
          <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
            {weakBullets.map((b, i) => (
              <div key={i} className="mono" style={{
                fontSize: 12, padding: "8px 12px", borderRadius: 7,
                background: "var(--surface)", border: "1px solid var(--border)",
                color: "var(--txt-2)",
              }}>
                ✗ &nbsp;{b}
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
