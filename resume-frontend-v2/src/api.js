import axios from "axios";

const BASE = "http://localhost:8000";

export async function analyzeResume(file, jdText, skipSemantic, skipAI) {
  const form = new FormData();
  form.append("file", file);
  if (jdText.trim()) form.append("jd_text", jdText.trim());
  if (skipSemantic)  form.append("skip_semantic", "true");
  if (skipAI)        form.append("skip_ai", "true");

  const { data } = await axios.post(`${BASE}/analyze`, form, {
    headers: { "Content-Type": "multipart/form-data" },
    timeout: 120000,
  });

  return data;
}
