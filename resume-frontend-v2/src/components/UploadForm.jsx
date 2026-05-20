import { useState, useRef } from "react";

export default function UploadForm({ onAnalyze, loading }) {
  const [file, setFile]               = useState(null);
  const [jd, setJd]                   = useState("");
  const [skipSemantic, setSkipSem]    = useState(false);
  const [skipAI, setSkipAI]           = useState(false);
  const [drag, setDrag]               = useState(false);
  const inputRef                      = useRef();

  function onDrop(e) {
    e.preventDefault();
    setDrag(false);
    const f = e.dataTransfer.files[0];
    if (f?.type === "application/pdf") setFile(f);
  }

  return (
    <div style={{ maxWidth: 560, margin: "0 auto" }}>

      <div style={{ textAlign: "center", marginBottom: 48 }}>
        <div style={{
          display: "inline-flex", alignItems: "center", gap: 10,
          background: "var(--accent-bg)", border: "1px solid var(--accent-bd)",
          borderRadius: 8, padding: "6px 14px", marginBottom: 24,
        }}>
          <span style={{ width: 6, height: 6, borderRadius: "50%", background: "var(--accent)", display: "inline-block" }} />
          <span className="mono" style={{ fontSize: 12, color: "var(--accent)" }}>AI-Powered · ATS Scoring · Gemini Feedback</span>
        </div>
        <h1 style={{ fontSize: 42, fontWeight: 800, lineHeight: 1.15, letterSpacing: "-0.02em", marginBottom: 12 }}>
          Resume Intelligence<br />
          <span style={{ color: "var(--accent)" }}>Platform</span>
        </h1>
        <p style={{ color: "var(--txt-2)", fontSize: 15 }}>
          Upload your resume. Get ATS score, semantic analysis, and AI feedback.
        </p>
      </div>

      <div className="card" style={{ display: "flex", flexDirection: "column", gap: 22 }}>

        <div>
          <p className="section-label" style={{ marginBottom: 10 }}>Resume PDF</p>
          <div
            onClick={() => inputRef.current.click()}
            onDrop={onDrop}
            onDragOver={(e) => { e.preventDefault(); setDrag(true); }}
            onDragLeave={() => setDrag(false)}
            style={{
              border: `1.5px dashed ${drag || file ? "var(--accent)" : "var(--border-hi)"}`,
              borderRadius: 10,
              background: drag ? "var(--accent-bg)" : "var(--surface)",
              padding: "28px 20px",
              textAlign: "center",
              cursor: "pointer",
              transition: "all 0.2s ease",
            }}
          >
            <div style={{
              width: 40, height: 40, borderRadius: 10, background: "var(--border)",
              display: "flex", alignItems: "center", justifyContent: "center",
              margin: "0 auto 12px",
            }}>
              <svg width="18" height="18" fill="none" stroke={file ? "var(--accent)" : "var(--txt-2)"} strokeWidth="1.8" viewBox="0 0 24 24">
                <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M17 8l-5-5-5 5M12 3v12" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </div>
            {file ? (
              <>
                <p style={{ fontWeight: 600, color: "var(--accent)", fontSize: 14 }}>{file.name}</p>
                <p className="mono" style={{ fontSize: 11, color: "var(--txt-3)", marginTop: 4 }}>
                  {(file.size / 1024).toFixed(1)} KB · click to replace
                </p>
              </>
            ) : (
              <>
                <p style={{ fontWeight: 600, fontSize: 14 }}>Drop your PDF here or click to browse</p>
                <p className="mono" style={{ fontSize: 11, color: "var(--txt-3)", marginTop: 4 }}>PDF only · max 10 MB</p>
              </>
            )}
            <input ref={inputRef} type="file" accept=".pdf" style={{ display: "none" }}
              onChange={(e) => e.target.files[0] && setFile(e.target.files[0])} />
          </div>
        </div>

        <div>
          <p className="section-label" style={{ marginBottom: 10 }}>
            Job Description &nbsp;
            <span style={{ color: "var(--txt-3)", textTransform: "none", letterSpacing: 0, fontSize: 11 }}>(optional — enables JD match scoring)</span>
          </p>
          <textarea
            value={jd}
            onChange={(e) => setJd(e.target.value)}
            placeholder="Paste the job description here..."
            rows={4}
            style={{
              width: "100%", background: "var(--surface)",
              border: `1px solid ${jd ? "var(--accent-bd)" : "var(--border)"}`,
              borderRadius: 10, padding: "12px 14px",
              color: "var(--txt)", fontSize: 14, resize: "vertical",
              fontFamily: "'Syne', sans-serif", outline: "none",
              transition: "border 0.2s",
            }}
          />
        </div>

        <div style={{ display: "flex", gap: 20, flexWrap: "wrap" }}>
          {[
            { label: "Skip Semantic Model", sublabel: "faster", val: skipSemantic, set: setSkipSem },
            { label: "Skip Gemini AI",      sublabel: "no API calls", val: skipAI, set: setSkipAI },
          ].map(({ label, sublabel, val, set }) => (
            <label key={label} style={{ display: "flex", alignItems: "center", gap: 10, cursor: "pointer", userSelect: "none" }}>
              <div
                onClick={() => set(!val)}
                style={{
                  width: 36, height: 20, borderRadius: 10, position: "relative",
                  background: val ? "var(--accent)" : "var(--border-hi)",
                  transition: "background 0.2s",
                }}
              >
                <div style={{
                  position: "absolute", top: 3, width: 14, height: 14, borderRadius: "50%",
                  background: val ? "#fff" : "var(--txt-3)",
                  left: val ? 19 : 3, transition: "left 0.2s, background 0.2s",
                }} />
              </div>
              <span style={{ fontSize: 13, color: "var(--txt-2)" }}>
                {label} <span style={{ color: "var(--txt-3)" }}>· {sublabel}</span>
              </span>
            </label>
          ))}
        </div>

        <button
          onClick={() => file && !loading && onAnalyze(file, jd, skipSemantic, skipAI)}
          disabled={!file || loading}
          style={{
            width: "100%", padding: "13px",
            background: !file || loading ? "var(--border)" : "var(--accent)",
            color: !file || loading ? "var(--txt-3)" : "#fff",
            border: "none", borderRadius: 10,
            fontSize: 14, fontWeight: 700, cursor: !file || loading ? "not-allowed" : "pointer",
            fontFamily: "'Syne', sans-serif", letterSpacing: "0.02em",
            transition: "background 0.2s",
          }}
        >
          {loading ? "Analyzing..." : "Analyze Resume →"}
        </button>
      </div>
    </div>
  );
}
