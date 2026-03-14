
# What MediQ Does
MediQ is a full-stack AI-powered medical report analysis platform that:
  1.  Accepts medical documents in multiple formats (PDF, images, CSV) 
  2.  Extracts text using smart routing — PyMuPDF for digital PDFs, Tesseract OCR for images/scanned PDFs, Pandas for CSVs
  3.  Analyzes the extracted text using Gemini 2.0 Flash (primary) with Groq/LLaMA as a fallback
  4.  Displays results in a beautiful interactive dashboard with biomarker analysis, risk scoring, health scores, trend tracking, and PDF export

# Architecture
-- Layer			Technology	                   Details
-- Frontend			React + TypeScript + Tailwind + Vite	5screens: Landing → Upload → Processing → Results → History
-- Backend			Python + Flask + Flask-CORS	RESTful API with /, /health, /upload, /history endpoints
-- AI Engine			Gemini 2.0 Flash + Groq Fallback	Structured JSON prompt → JSON response → normalization + risk scoring
-- Extraction			PyMuPDF + Tesseract OCR + Pandas	Smart router that auto-detects file type and chooses extractor

# Backend Flow
-- File Upload → Validation → Smart Extractor Router → AI Analysis → 
-- Normalize → Risk Score → Cache → Return JSON with telemetry

# Current Features ✅
1. Multi-format file ingestion (PDF, Image, CSV)
2. OCR fallback for scanned PDFs
3. Dual AI engine with automatic failover
4. In-memory caching (SHA-256 hash)
5. Risk scoring with health score calculation
6. Session-scoped telemetry & history (up to 15 reports)
7. Dark/light theme support
8. Backend health monitoring
9. Processing pipeline animation
10. PDF export via window.print()
11. Drag & drop upload

# 🩺 MediQ — AI-Powered Medical Report Analyzer

MediQ is a full-stack, AI-powered medical report analysis platform that converts unstructured medical documents (PDFs, scanned images, CSVs) into structured, meaningful, and actionable health insights. It addresses a real-world problem in healthcare: **medical reports are often complex, inconsistent, and difficult for patients and even clinicians to quickly interpret.** MediQ bridges this gap by combining intelligent extraction, AI-driven analysis, and a clean user interface to make medical data more accessible and usable.

Built during the **Infosys Virtual Internship**, this project demonstrates end-to-end system design, backend engineering, frontend UX, AI integration, and workflow optimization.


## 🎯 Problem Statement

In real healthcare environments:

- Medical reports come in different formats (PDFs, scanned images, CSV exports).
- Important biomarkers and values are buried in long documents.
- Patients struggle to understand reports.
- Doctors and labs lack simple tools to quickly visualize and summarize data.

**The core problem MediQ solves:**

👉 Making medical reports **machine-readable, human-friendly, and insight-driven**.


## 💡 Motivation & Inspiration

This project was inspired by:
- Observing how difficult it is for non-technical users to understand medical reports.
- The need for digital transformation in healthcare documentation.
- Internship exposure to system design and workflow automation challenges.

I built MediQ to:
- Apply full-stack development skills in a meaningful healthcare use case.
- Explore AI integration in real applications.
- Design a complete, production-style system rather than a toy project.


## 🧑‍💻 My Contributions

I took ownership of the entire system design and implementation, including:

### Backend Engineering
- Designed RESTful APIs using Flask.
- Implemented multi-format file ingestion (PDF, Image, CSV).
- Built a **smart extraction router** that automatically chooses the appropriate extractor:
  - PDF parsing
  - OCR pipeline for scanned images
  - CSV parsing logic
- Integrated an AI analysis engine with fallback logic.
- Implemented risk scoring, abnormality detection, confidence metrics, caching, and telemetry.
- Added structured error handling and validation.

### Frontend Development
- Designed a premium UI using React + TypeScript + Tailwind.
- Built:
  - Drag-and-drop upload interface
  - Real-time backend health monitoring
  - Interactive results dashboard
  - Expandable biomarker explanations
  - Trend visualization & alerts
  - History tracking
  - Dark/light mode support

### Workflow & UX Enhancements
- Optimized backend processing flow.
- Added telemetry and an audit trail for traceability.
- Designed a clean user journey from upload → analysis → results → export.

### PDF Report Generation
- Enabled exportable professional summaries for offline sharing with a structured report layout.


## ✨ Key Features

### 🔧 Backend (Python + Flask)
- Multi-format ingestion (PDF, Image, CSV).
- Smart extraction router (PDF parser, OCR, CSV processor).
- AI-powered medical text analysis with fallback logic.
- Risk scoring, abnormality detection, confidence metrics.
- Workflow optimization, caching, telemetry.
- RESTful APIs with validation & error handling.

### 🎨 Frontend (React + TypeScript)
- Premium UI with Tailwind CSS.
- Drag & drop upload interface.
- Real-time backend health monitoring.
- Interactive results dashboard with biomarker explanations.
- Trend visualization, alerts, history tracking.
- Dark/light theme support.

### 📄 PDF Export
- Generate structured, professional reports for offline sharing.

### ⚙️ Workflow Optimization
- Modular backend architecture.
- Error-resilient pipelines.
- Performance-aware processing.
- Telemetry & audit trail.


## 🧱 High-Level Architecture

```text
Frontend (React + TypeScript)
        |
        v
 REST API (Flask Backend)
        |
        v
 Smart Extraction Router
   ├── PDF Parser
   ├── OCR Engine (Images)
   └── CSV Processor
        |
        v
 AI Analysis Engine
        |
        v
 Normalization + Risk Scoring + Telemetry
        |
        v
 Results Dashboard + PDF Export
```

---

## 🛠 Technologies Used

**Frontend:**
- React
- TypeScript
- Tailwind CSS
- Vite

**Backend:**
- Python
- Flask
- Flask-CORS
- PyMuPDF
- Tesseract OCR
- Pillow

**AI / Processing:**
- AI model integration
- Confidence scoring
- Abnormality detection
- Fallback logic

**Other:**
- Git / GitHub
- Modular service design
- Telemetry & logging


## ⚙️ Installation & Setup

Backend:

```bash
git clone https://github.com/vvdmahesh3/MediQ
cd MediQ/backend/api
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Runs at: `http://127.0.0.1:5000` (local backend API server)

Frontend:

```bash
cd ../frontend
npm install
npm run dev
```

Runs at: `http://localhost:5173` (frontend development server)


## ▶️ Usage Guide

1. Upload a medical report (PDF / Image / CSV).
2. Backend validates and extracts text.
3. AI engine analyzes biomarkers and risk.
4. Dashboard displays parameters, health status, confidence scores, and explanations.
5. Export results as PDF if needed.


## ⚠️ Deployment Note

The backend integrates AI models, OCR engines, and heavy processing libraries, which can require significant compute resources. Free hosting platforms (Render, Railway, etc.) impose strict limits on RAM, CPU, build size, and request timeouts.

➡️ Due to these constraints, the backend is demonstrated locally in this repo, while the frontend can be deployed independently. Production-ready deployment options include dedicated cloud instances, Docker/Kubernetes, or paid cloud services (AWS, Azure, GCP).


## 🔮 Future Roadmap

- User authentication & report history
- Secure cloud storage
- Doctor–patient sharing workflow
- Real-time charts for longitudinal tracking
- HIPAA-compliant security layer
- Mobile app version
- Multi-language OCR support


## 🤝 Contributions & Acknowledgments

Designed and developed by Mahesh during the Infosys Virtual Internship.
Thanks to teammates (e.g., Mohit) and mentor [Saritha](https://github.com/Saritha-batch1) for feedback.
Open-source libraries for PDF, OCR, and UI frameworks made this project possible.


## 📬 Contact

- Mahesh VVD. P
- Portfolio: https://vvdmahesh3.github.io/demo-portfolio/
- LinkedIn: https://www.linkedin.com/in/vvdmahesh362006/
- Email: immahesh300@gmail.com


If you found this project useful, please star the repo, fork it, or share feedback.
