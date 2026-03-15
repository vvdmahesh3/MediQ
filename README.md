<p align="center">
  <img src="https://img.shields.io/badge/MediQ-AI_Medical_Analyzer-0ea5e9?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCI+PHBhdGggZD0iTTIyIDEyaC00bC0zIDlMOSAzbC0zIDlIMiIvPjwvc3ZnPg==" alt="MediQ Badge"/>
  <br/>
  <img src="https://img.shields.io/badge/version-v6.0--enhanced-22d3ee?style=flat-square" alt="Version"/>
  <img src="https://img.shields.io/badge/python-3.x-3776ab?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/react-18.3.1-61dafb?style=flat-square&logo=react&logoColor=white" alt="React"/>
  <img src="https://img.shields.io/badge/flask-latest-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask"/>
  <img src="https://img.shields.io/badge/gemini-2.0_flash-8E75B2?style=flat-square&logo=google&logoColor=white" alt="Gemini"/>
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License"/>
</p>

<h1 align="center">🏥 MediQ — AI-Powered Medical Report Analyzer</h1>

<p align="center">
  <strong>Transform unstructured medical reports into structured, actionable health insights using dual AI engines.</strong>
  <br/>
  Upload a PDF, image, or CSV → Get a full analysis dashboard with health scores, risk predictions, organ scores, a personalized 10-day health plan, and a doctor's perspective — all in under 30 seconds.
</p>

<p align="center">
  <a href="#-features">Features</a> •
  <a href="#-tech-stack">Tech Stack</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-getting-started">Getting Started</a> •
  <a href="#-api-reference">API Reference</a> •
  <a href="#-screenshots">Screenshots</a> •
  <a href="#-project-structure">Project Structure</a>
</p>

---

## 📌 Overview

**MediQ** is a full-stack, AI-powered medical report analysis platform built as part of the **Infosys Virtual Internship (March 2026)**. It processes medical reports in multiple formats (PDF, scanned images via OCR, CSV) and uses a **dual AI engine** (Google Gemini 2.0 Flash + Groq LLaMA 3.1 fallback) to extract biomarkers, analyze them against clinical reference ranges, and generate comprehensive health insights.

| Problem | How MediQ Solves It |
|---|---|
| Reports come in different formats (PDF, image, CSV) | Smart extraction router handles all formats automatically |
| Biomarkers buried in long documents | AI extracts and structures every value with confidence scores |
| Patients can't understand complex lab language | AI generates plain-language explanations per parameter |
| No quick risk assessment tool | Automated risk scoring with health score out of 100 |
| No tracking over time | Persistent report history with side-by-side comparison |
| No personalized recovery guidance | AI-generated 10-day health plan per report |
| No doctor-like interpretation | AI simulates a doctor's perspective on results |

> **Author:** Mahesh VVD. P &nbsp;|&nbsp; **Internship:** Infosys Virtual Internship &nbsp;|&nbsp; **Date:** March 2026 &nbsp;|&nbsp; **Version:** v6.0-enhanced

---

## ✨ Features

### 🔬 Core Analysis Engine
- **Multi-format ingestion** — PDF (digital + scanned via OCR), JPG, PNG, CSV
- **Dual AI engine** — Gemini 2.0 Flash (primary) with Groq LLaMA 3.1 8B (fallback)
- **Smart extraction pipeline** — PyMuPDF for digital PDFs, Tesseract OCR for scanned documents, Pandas for CSV
- **In-memory caching** — SHA-256 text hashing prevents redundant AI calls
- **Confidence scoring** — Each biomarker gets an AI confidence rating (0.65–0.98)

### 📊 Results Dashboard
- **Health Score** — Overall score out of 100 with color-coded risk level (low / moderate / high)
- **Biomarker Table** — Filterable (All / Critical / Abnormal / Normal), expandable rows with clinical interpretation
- **Visual Range Bars** — Each parameter shows a visual indicator on the low → normal → high → critical range
- **Organ System Scores** — 5-system breakdown: Metabolic, Cardiac, Renal, Hepatic, Hematologic
- **Disease Risk Predictions** — AI-predicted conditions with probability bars
- **Doctor's Perspective** — AI-generated clinical interpretation in physician's voice
- **Infra Telemetry Strip** — Shows analysis ID, engine used, latency, cache status, version
- **PDF Export** — Clean print-optimized layout via `window.print()`

### 🗓️ 10-Day Personalized Health Plan
- Day-by-day actionable guidance: **Diet**, **Exercise**, **Sleep**, **Supplements**, **Precautions**
- Interactive completion tracking with progress bar
- Each day color-coded with unique gradient badge

### 📈 Report Comparison
- Select any 2 historical reports for side-by-side analysis
- Parameter-level diff with trend tracking (improved / declined / stable)
- Health score and organ score delta visualization
- Percentage change calculations for numeric parameters

### 🔐 Authentication System
- JWT-based authentication (HS256, 72-hour expiry)
- Secure password hashing (pbkdf2:sha256 + 16-char salt)
- Auto-logout on token expiry or API 401
- Auth state persisted in `localStorage`

### 🌗 Additional Features
- **Dark / Light mode** — Persisted theme preference
- **Drag-and-drop upload** — With real-time progress simulation and backend health monitoring
- **Animated processing pipeline** — 5-stage visual animation while results load
- **Report history** — View, delete, and compare past reports
- **Glassmorphism UI** — Modern frosted-glass design with micro-animations
- **Responsive layout** — Works across desktop and tablet screens

---

## 🛠️ Tech Stack

### Frontend
| Technology | Version | Purpose |
|---|---|---|
| React | 18.3.1 | UI component framework |
| TypeScript | 5.5.3 | Type-safe JavaScript |
| Vite | 5.4.2 | Build tool & dev server (port 5173) |
| Tailwind CSS | 3.4.1 | Utility-first CSS framework |
| Recharts | 3.7.0 | Charts: RadialBar, PieChart, BarChart |
| lucide-react | 0.344.0 | Icon library (50+ icons) |
| Inter + JetBrains Mono | — | Typography (Google Fonts) |

### Backend
| Technology | Version | Purpose |
|---|---|---|
| Python | 3.x | Runtime |
| Flask | Latest | Web framework & REST API |
| Flask-CORS | Latest | Cross-origin resource sharing |
| PyMuPDF (fitz) | Latest | PDF text extraction |
| pytesseract | Latest | OCR for scanned documents |
| Pillow (PIL) | Latest | Image processing for OCR |
| pandas | Latest | CSV parsing |
| google-genai | Latest | Gemini 2.0 Flash API client |
| groq | Latest | Groq Cloud / LLaMA 3.1 API client |
| PyJWT | Latest | JWT token management |
| werkzeug | Latest | Password hashing (pbkdf2:sha256) |
| SQLite | stdlib | Embedded database |
| python-dotenv | Latest | Environment variable loading |

### External Services
| Service | Purpose |
|---|---|
| Google AI Studio (Gemini 2.0 Flash) | Primary AI analysis engine |
| Groq Cloud (LLaMA 3.1 8B Instant) | Fallback AI engine |
| Tesseract OCR | Optical character recognition for scanned PDFs & images |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  FRONTEND (Browser)                      │
│   React 18 + TypeScript + Tailwind CSS + Vite           │
│                                                         │
│   8 Screens:  Landing → Auth → Upload → Processing     │
│               → Results → History → HealthPlan → Compare│
│                                                         │
│   API Client:  lib/api.ts  (JWT-authenticated fetch)    │
└──────────────────────┬──────────────────────────────────┘
                       │  HTTP REST  (localhost:5001)
                       │  JSON + multipart/form-data
                       │  Authorization: Bearer <JWT>
┌──────────────────────▼──────────────────────────────────┐
│                BACKEND (Flask API)                       │
│   Python 3.x + Flask + Flask-CORS                       │
│                                                         │
│   Routes:  /  /health  /auth/*  /upload                 │
│            /reports  /reports/<uid>  /reports/compare    │
│                                                         │
│   Modules:                                              │
│   ┌──────────┐  ┌───────────┐  ┌──────────┐ ┌───────┐  │
│   │ app.py   │  │extractors │  │ai_engine │ │utils  │  │
│   │ (routes) │  │  .py      │  │  .py     │ │ .py   │  │
│   └──────────┘  └──────┬────┘  └────┬─────┘ └───────┘  │
│                        │            │                    │
│               ┌────────▼──┐  ┌──────▼──────────────┐   │
│               │ PDF/OCR/  │  │ Gemini 2.0 Flash     │   │
│               │ CSV Parse │  │ (Primary AI Engine)  │   │
│               └───────────┘  │ Groq / LLaMA 3.1     │   │
│                              │ (Fallback Engine)    │   │
│                              └──────────────────────┘   │
│                                                         │
│   database.py ──► SQLite (mediq.db)                     │
└─────────────────────────────────────────────────────────┘
```

### Navigation Flow (State Machine)

```
[Landing Page]
  │ "Get Started"
  ├── IF logged in ──► [Upload Interface]
  └── IF not ──► [Auth Screen]
                  │ Login / Signup
                  └──► [Upload Interface]
                        │ File uploaded
                        └──► [Processing Screen] (animated pipeline)
                               │ ~11 seconds
                               └──► [Results Dashboard]
                                      ├── "View History" → [History Dashboard]
                                      │                      ├── View → [Results]
                                      │                      └── Compare 2 → [Compare Reports]
                                      └── "Health Plan" → [Health Plan View]
```

### AI Engine Failsafe Chain

```
analyze_medical_text(text)
  ├── CACHE HIT? → return cached result immediately
  ├── Try: Gemini 2.0 Flash (primary)
  │     ├── SUCCESS → parse JSON → normalize
  │     └── FAIL ↓
  ├── Try: Groq LLaMA 3.1 8B (fallback)
  │     ├── SUCCESS → parse JSON → normalize
  │     └── FAIL ↓
  └── Use error-fallback dict → normalize
  
  → normalize_result() always runs
  → Cache result for future requests
  → Return structured analysis
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+** installed
- **Node.js 18+** and **npm** installed
- **Tesseract OCR** installed ([download](https://github.com/UB-Mannheim/tesseract/wiki))
- **Google AI Studio API Key** ([get one](https://aistudio.google.com/apikey))
- **Groq API Key** ([get one](https://console.groq.com/keys)) — *optional, used as fallback*

### 1. Clone the Repository

```bash
git clone https://github.com/vvdmahesh3/MediQ.git
cd MediQ
```

### 2. Backend Setup

```bash
# Create and activate virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
# source .venv/bin/activate

# Install dependencies
pip install -r backend/api/requirements.txt
```

### 3. Configure Environment Variables

Create `backend/api/.env`:
```env
GEMINI_API_KEY=your_google_ai_studio_key
GROQ_API_KEY=your_groq_api_key
JWT_SECRET=your_random_secret_string_here
```

Create `Frontend/.env`:
```env
VITE_API_URL=http://127.0.0.1:5001
```

### 4. Frontend Setup

```bash
cd Frontend
npm install
```

### 5. Run the Application

**Terminal 1 — Start Backend:**
```bash
cd backend
python app.py
# 🚀 MediQ API v6.0 starting on port 5001...
```

**Terminal 2 — Start Frontend:**
```bash
cd Frontend
npm run dev
# → http://localhost:5173
```

### 6. Open in Browser

Navigate to **http://localhost:5173** — Create an account, upload a medical report, and explore!

---

## 📸 Screenshots

<p align="center">
  <img src="demo/assets/screenshots/UploadInterface.png" alt="Upload Interface" width="700"/>
  <br/><em>Upload Interface — Drag & drop with real-time backend health monitoring</em>
</p>

<p align="center">
  <img src="demo/assets/screenshots/ResultsDashboard.png" alt="Results Dashboard" width="700"/>
  <br/><em>Results Dashboard — Full AI analysis with health scores, biomarkers, charts & more</em>
</p>

<p align="center">
  <img src="demo/assets/screenshots/system-generated-summary.png" alt="AI Summary" width="700"/>
  <br/><em>AI-Generated Summary with Doctor's Perspective</em>
</p>

---

## 📁 Project Structure

```
MediQ/
├── README.md                          # This file
├── MediQ_Complete_Documentation.md    # Detailed 60-page technical documentation
├── .gitignore                         # Git ignore rules
│
├── backend/
│   ├── app.py                         # Launcher (delegates to backend/api/app.py)
│   └── api/
│       ├── app.py                     # Flask server — all routes & business logic
│       ├── ai_engine.py               # Dual AI orchestrator (Gemini → Groq → fallback)
│       ├── extractors.py              # Smart file router: PDF / OCR / CSV text extraction
│       ├── database.py                # SQLite CRUD — users & reports tables
│       ├── utils.py                   # JWT, password hashing, auth decorator, validators
│       ├── run_debug.py               # Debug launcher with stdout/stderr logging
│       ├── requirements.txt           # Python dependencies
│       ├── .env                       # API keys & JWT secret (git-ignored)
│       ├── mediq.db                   # SQLite database file
│       ├── uploads/                   # Temp file storage (auto-cleaned)
│       └── results/                   # Additional results storage
│
├── Frontend/
│   ├── index.html                     # HTML entry point
│   ├── package.json                   # npm dependencies & scripts
│   ├── vite.config.ts                 # Vite configuration
│   ├── tailwind.config.js             # Tailwind CSS configuration
│   ├── tsconfig.json                  # TypeScript configuration
│   ├── .env                           # Frontend env vars (git-ignored)
│   └── src/
│       ├── main.tsx                   # React entry point
│       ├── App.tsx                    # Root component — screen state machine
│       ├── index.css                  # Global styles, animations, glassmorphism
│       ├── lib/
│       │   └── api.ts                 # Centralized API client with JWT handling
│       └── components/
│           ├── LandingPage.tsx         # Hero page with features & CTA
│           ├── AuthScreen.tsx          # Login / Signup with animated background
│           ├── UploadInterface.tsx     # Drag-and-drop upload with health monitoring
│           ├── ProcessingScreen.tsx    # 5-stage animated pipeline
│           ├── ResultsDashboard.tsx    # Full analysis dashboard (largest component)
│           ├── HistoryDashboard.tsx    # Report history with compare/view/delete
│           ├── HealthPlanView.tsx      # 10-day interactive health plan
│           └── CompareReports.tsx      # Side-by-side report comparison
│
└── demo/
    ├── index.html                     # Demo presentation page
    ├── styles.css                     # Demo page styles
    └── assets/
        ├── MediQ_Presentation.pdf     # Presentation slides
        ├── code_mediq.mp4             # Demo video walkthrough
        └── screenshots/              # Application screenshots
```

---

## 🔌 API Reference

All endpoints are served from `http://localhost:5001`.

### Public Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Service info & status |
| `GET` | `/health` | Backend health check |
| `POST` | `/auth/signup` | Create new account |
| `POST` | `/auth/login` | Login & receive JWT |

### Protected Endpoints (requires `Authorization: Bearer <token>`)

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/auth/me` | Get current user info + report count |
| `POST` | `/upload` | Upload file → extract → AI analyze → save |
| `GET` | `/reports` | Get all user's report summaries |
| `GET` | `/reports/<uid>` | Get single full report with analysis data |
| `DELETE` | `/reports/<uid>` | Delete a report |
| `POST` | `/reports/compare` | Compare two reports side-by-side |
| `GET` | `/history` | Legacy endpoint (backward compat) |

### Example: Upload & Analyze

```bash
# Sign up
curl -X POST http://localhost:5001/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "secure123", "full_name": "John Doe"}'

# Upload report (use token from signup response)
curl -X POST http://localhost:5001/upload \
  -H "Authorization: Bearer <your_jwt_token>" \
  -F "file=@blood_report.pdf"
```

### Response Structure (Upload)

```json
{
  "user_profile": { "name": "...", "age": "...", "gender": "..." },
  "parameters": [
    {
      "name": "Hemoglobin",
      "value": "10.2",
      "unit": "g/dL",
      "normalRange": "13.5-17.5",
      "status": "low",
      "confidence": 0.87,
      "explanation": "Below normal range, may indicate anemia...",
      "red_flag": false
    }
  ],
  "summary": "Clinical summary...",
  "recommendations": ["...", "..."],
  "doctor_perspective": "Based on these results, I would recommend...",
  "organ_scores": {
    "metabolic": 72, "cardiac": 80, "renal": 68,
    "hepatic": 75, "hematologic": 79
  },
  "health_plan": [
    { "day": 1, "focus": "...", "diet": "...", "exercise": "...",
      "precautions": "...", "sleep": "...", "supplements": "..." }
  ],
  "disease_risks": [
    { "disease": "Anemia", "risk_level": "high",
      "probability": 75, "explanation": "..." }
  ],
  "risk_metrics": {
    "health_score": 63, "overall_risk": "moderate-risk",
    "critical_count": 0, "abnormal_count": 3, "average_confidence": 0.84
  },
  "audit": {
    "analysis_id": "abc123", "engine": "gemini",
    "processing_time_ms": 4521, "cache_hit": false
  }
}
```

---

## 🗄️ Database Schema

MediQ uses **SQLite** with WAL (Write-Ahead Logging) mode for concurrent access.

```sql
-- Users table
CREATE TABLE users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    email         TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    full_name     TEXT NOT NULL,
    created_at    TEXT NOT NULL DEFAULT (datetime('now')),
    last_login    TEXT
);

-- Reports table
CREATE TABLE reports (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id       INTEGER NOT NULL,
    report_uid    TEXT UNIQUE NOT NULL,    -- e.g. REP-A1B2C3D4E5
    filename      TEXT NOT NULL,
    file_type     TEXT NOT NULL,           -- PDF, PNG, CSV, etc.
    health_score  INTEGER DEFAULT 0,
    overall_risk  TEXT DEFAULT 'unknown',  -- low-risk / moderate-risk / high-risk
    analysis_data TEXT,                    -- Full JSON blob of AI result
    created_at    TEXT NOT NULL DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE INDEX idx_reports_user ON reports(user_id);
CREATE INDEX idx_reports_uid  ON reports(report_uid);
```

### Data Security
- 🔒 **User isolation** — `user_id` is always included in queries; users can only access their own reports
- 🔒 **Password security** — Stored as `pbkdf2:sha256` hashes with 16-character salt, never plain text
- 🔒 **Cascade delete** — Deleting a user automatically removes all their reports
- 🔒 **JWT protected** — All sensitive endpoints require a valid Bearer token

---

## ⚙️ How It Works

### File Processing Pipeline

```
Input File
    │
    ├── .pdf → PyMuPDF (fitz) extracts text
    │            └── If text < 20 chars (scanned PDF):
    │                  convert to images → Tesseract OCR (--psm 6, 2x zoom)
    │
    ├── .jpg/.png → Pillow opens image → Tesseract OCR
    │
    └── .csv → pandas.read_csv() → rows converted to natural language sentences
    
    → extracted_text (string) → AI Analysis
```

### Risk Score Calculation

```
Starting score = 100
For each parameter:
  status == "critical" → score -= 25
  status == "high" or "low" → score -= 12
  status == "normal" → score -= 2

score = clamp(5, 100)

score >= 75 → "low-risk"     (green)
score >= 45 → "moderate-risk" (amber)
score <  45 → "high-risk"     (red)
```

### Error Handling

| Scenario | Backend Response | Frontend Behavior |
|---|---|---|
| No file uploaded | `400 "No file received"` | Error banner |
| Wrong file type | `400 "Unsupported file type"` | Error banner |
| File > 10MB | `400 "File exceeds 10MB"` | Error banner |
| Unreadable document | `500 "Empty or unreadable"` | Error banner |
| Both AI engines fail | `500` + fallback empty params | Processing error |
| Invalid/expired JWT | `401 "Invalid or expired token"` | Auto-logout → Auth |
| 90s upload timeout | `AbortError` thrown | "Analysis timed out" |
| Email already exists | `409 "Account exists"` | Inline form error |

---

## 🧩 Frontend Screens

| # | Screen | Component | Key Features |
|---|---|---|---|
| 1 | **Landing** | `LandingPage.tsx` | Animated hero, feature grid, trust badges, stats |
| 2 | **Auth** | `AuthScreen.tsx` | Login/Signup tabs, DNA helix animation, error handling |
| 3 | **Upload** | `UploadInterface.tsx` | Drag-and-drop, progress bar, health monitor, file preview |
| 4 | **Processing** | `ProcessingScreen.tsx` | 5-stage pipeline animation, log terminal, status chips |
| 5 | **Results** | `ResultsDashboard.tsx` | Full dashboard — 662 lines, most complex component |
| 6 | **History** | `HistoryDashboard.tsx` | Report cards, trend icons, compare selection, delete |
| 7 | **Health Plan** | `HealthPlanView.tsx` | 10-day cards, completion tracking, expandable details |
| 8 | **Compare** | `CompareReports.tsx` | Side-by-side diffs, score deltas, organ comparisons |

> **No routing library** is used — navigation is managed entirely through React state in `App.tsx`.

---

## 🎨 Design System

MediQ features a premium, modern UI with:

- **Glassmorphism** — Frosted glass cards with `backdrop-filter: blur()` and subtle borders
- **Dynamic gradients** — Animated gradient backgrounds with flowing color transitions
- **Micro-animations** — Float, fade-in, shimmer, orbit, helix, bounce effects
- **3D card perspectives** — Interactive hover effects with depth
- **Dark mode first** — Full dark/light theme support persisted to localStorage
- **Custom CSS utilities** — `.glass`, `.glass-dark`, `.glow-blue`, `.glow-emerald`
- **Print styles** — Clean, ink-friendly layout for PDF export

---

## 📝 Documentation

For the complete 60-page technical documentation covering every module, route, component, data flow, and implementation detail, see:

📄 **[MediQ_Complete_Documentation.md](MediQ_Complete_Documentation.md)**

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## ⚠️ Medical Disclaimer

> **⚕️ IMPORTANT:** MediQ is an AI-powered tool designed for **educational and informational purposes only**. It is **NOT** a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional for medical decisions. AI-generated results may contain inaccuracies.

---

## 📜 License

This project was developed as part of the **Infosys Virtual Internship** program. See the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built with ❤️ by <strong>Mahesh VVD. P</strong> • Infosys Virtual Internship • March 2026
  <br/>
  <sub>MediQ v6.0-enhanced | React + TypeScript + Python Flask + Gemini AI + SQLite</sub>
</p>
