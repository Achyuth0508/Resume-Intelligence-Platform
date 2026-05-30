
# Resume Intelligence Platform

AI-powered resume analysis platform that evaluates resumes using semantic matching, weighted scoring, and AI-assisted feedback.

## Features

* Role detection (AI/ML vs SDE)
* ATS-style resume scoring
* Semantic similarity analysis
* Skill matching and ranking
* Project evaluation
* Resume vs Job Description matching
* Missing skill detection
* Weakness analysis
* AI-generated recommendations
* Interactive dashboard

---

# Tech Stack

## Backend

* FastAPI
* Sentence Transformers
* NumPy
* PyPDF
* Google Generative AI

## Frontend

* React
* Vite
* Tailwind CSS
* Axios

---

# Project Structure

```text id="bjlwmx"
Resume_analyser/
│
├── app/
│   ├── api.py
│   ├── main.py
│   ├── parser.py
│   ├── detector.py
│   ├── scorer.py
│   ├── semantic.py
│   ├── analyzer.py
│   ├── gemini.py
│   └── config.py
│
├── resume-frontend-v2/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── resumes/
├── requirements.txt
├── run_backend.bat
├── run_backend.sh
└── README.md
```

---

# How It Works

```text id="o3gwbx"
Resume PDF
    ↓
FastAPI Backend
    ├── PDF Parsing
    ├── Role Detection
    ├── ATS Scoring
    ├── Semantic Analysis
    ├── AI Feedback
    └── Report Generation
    ↓
React Frontend Dashboard
```

---

# Backend Setup

Install dependencies:

```bash id="08n8zq"
pip install -r requirements.txt
```

Create `.env` file:

```env id="jjlwm8"
GEMINI_API_KEY=your_api_key
```

Run backend:

```bash id="ywq5bm"
uvicorn app.api:app --reload --port 8000
```

Backend runs at:

```text id="oxs8l7"
http://127.0.0.1:8000
```

---

# Frontend Setup

```bash id="8c1h7m"
cd resume-frontend-v2
npm install
npm run dev
```

Frontend runs at:

```text id="xv9rj7"
http://localhost:3000
```

---

# API Endpoint

## Analyze Resume

```http id="n9sl4n"
POST /analyze
```

### Form Data

| Parameter     | Required |
| ------------- | -------- |
| file          | Yes      |
| jd_text       | No       |
| skip_semantic | No       |
| skip_ai       | No       |

---

# Core Concepts Used

* Semantic Search
* Embedding Models
* Cosine Similarity
* Ranking Systems
* ATS Scoring
* FastAPI Backend Engineering
* Frontend/Backend Integration
* AI-assisted Analysis
=======
# Resume-Intelligence-Platform
AI-powered resume analysis platform using semantic matching, ATS-style scoring, and AI-assisted feedback.

