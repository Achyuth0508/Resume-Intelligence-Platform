import { useState } from "react";
import { analyzeResume } from "./api";
import UploadForm from "./components/UploadForm";
import Dashboard  from "./components/Dashboard";

export default function App() {
  const [result,  setResult]  = useState(null);
  const [loading, setLoading] = useState(false);
  const [error,   setError]   = useState(null);

  async function handleAnalyze(file, jd, skipSemantic, skipAI) {
    setError(null);
    setResult(null);
    setLoading(true);
    try {
      const data = await analyzeResume(file, jd, skipSemantic, skipAI);
      setResult(data);
    } catch (err) {
      setError(
        err?.response?.data?.detail ||
        err?.message ||
        "Analysis failed. Is your FastAPI backend running on port 8000?"
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{ minHeight: "100vh" }}>

      <header style={{
        position: "sticky", top: 0, zIndex: 50,
        display: "flex", alignItems: "center", justifyContent: "space-between",
        padding: "14px 32px",
        background: "rgba(10,10,15,0.88)", backdropFilter: "blur(12px)",
        borderBottom: "1px solid var(--border)",
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{
            width: 28, height: 28, borderRadius: 8,
            background: "var(--accent)", display: "flex", alignItems: "center",
            justifyContent: "center", fontSize: 13, fontWeight: 800, color: "#fff",
          }}>R</div>
          <span style={{ fontWeight: 700, fontSize: 14, letterSpacing: "-0.01em" }}>Resume Intelligence</span>
          <span className="mono" style={{
            fontSize: 10, padding: "2px 7px", borderRadius: 5,
            background: "var(--border)", color: "var(--txt-3)", marginLeft: 4,
          }}>v2.0</span>
        </div>
        <span className="mono" style={{ fontSize: 11, color: "var(--txt-3)" }}>
          AI/ML · SDE · ATS · Gemini
        </span>
      </header>

      <main style={{ padding: "48px 24px 80px" }}>

        {loading && (
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", paddingTop: 80, gap: 20 }}>
            <div style={{ position: "relative", width: 52, height: 52 }}>
              <div style={{
                position: "absolute", inset: 0, borderRadius: "50%",
                border: "2.5px solid transparent", borderTopColor: "var(--accent)",
                animation: "spin 0.85s linear infinite",
              }} />
              <div style={{
                position: "absolute", inset: 8, borderRadius: "50%",
                border: "2px solid transparent", borderTopColor: "var(--blue)",
                animation: "spin 1.3s linear infinite reverse",
              }} />
            </div>
            <p className="mono" style={{ fontSize: 13, color: "var(--accent)", animation: "pulse 2s ease infinite" }}>
              Analyzing resume...
            </p>
            <p className="mono" style={{ fontSize: 11, color: "var(--txt-3)" }}>
              May take 30–60 seconds for full AI analysis
            </p>
          </div>
        )}

        {!loading && error && (
          <div style={{ maxWidth: 520, margin: "0 auto" }}>
            <div style={{
              padding: 18, borderRadius: 10, marginBottom: 24,
              background: "var(--red-bg)", border: "1px solid var(--red-bd)",
            }}>
              <p style={{ fontWeight: 700, color: "var(--red)", marginBottom: 6, fontSize: 14 }}>Analysis Failed</p>
              <p style={{ fontSize: 13, color: "var(--txt-2)" }}>{error}</p>
              <p className="mono" style={{ fontSize: 11, color: "var(--txt-3)", marginTop: 10 }}>
                Make sure backend is running: uvicorn app.api:app --reload --port 8000
              </p>
            </div>
            <UploadForm onAnalyze={handleAnalyze} loading={loading} />
          </div>
        )}

        {!loading && !error && !result && (
          <UploadForm onAnalyze={handleAnalyze} loading={loading} />
        )}

        {!loading && !error && result && (
          <Dashboard result={result} onReset={() => setResult(null)} />
        )}

      </main>

      <footer style={{
        textAlign: "center", padding: "20px 0",
        borderTop: "1px solid var(--border)",
        color: "var(--txt-3)", fontSize: 12,
      }}>
        <span className="mono">Resume Intelligence Platform</span>
      </footer>
    </div>
  );
}
