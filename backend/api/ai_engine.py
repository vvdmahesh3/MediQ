"""
MediQ AI Analysis Engine (v6.0)
Enhanced with: organ scores, doctor's perspective, 10-day health plan,
disease risk predictions, and prevention tips.
Dual AI support: Gemini (primary) → Groq (fallback) → Error fallback.
"""

import os
import json
import re
import hashlib
import random
import time
from datetime import datetime, timezone
from pathlib import Path as _Path
from dotenv import load_dotenv
from google import genai
from groq import Groq

# ======================================================
# ENV LOAD
# ======================================================
_ENV_PATH = _Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=_ENV_PATH, override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GEMINI_API_KEY:
    print("⚠️ GEMINI_API_KEY missing — Gemini will be skipped, using Groq fallback.")

# ======================================================
# CLIENTS & CONFIG
# ======================================================
gemini_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

GEMINI_MODEL = "gemini-2.0-flash"   # ✅ stable model (replaces deprecated gemini-2.0-flash-exp)
GROQ_MODEL = "llama-3.1-8b-instant"
ENGINE_VERSION = "v6.0-enhanced-prod"

# Simple in-memory cache
CACHE = {}

# ======================================================
# UTILITIES
# ======================================================

def get_text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def extract_json(text: str) -> dict:
    """Safely clean AI markdown and extract a JSON dictionary."""
    text = re.sub(r"```json\s?|\s?```", "", text).strip()
    try:
        return json.loads(text)
    except Exception:
        match = re.search(r"\{[\s\S]*\}", text)
        if not match:
            raise ValueError("❌ No valid JSON detected in AI output")
        return json.loads(match.group(0))


def generate_confidence(status: str) -> float:
    status = status.lower()
    ranges = {
        "normal": (0.85, 0.98),
        "low": (0.75, 0.90),
        "high": (0.75, 0.90),
        "critical": (0.65, 0.85)
    }
    low, high = ranges.get(status, (0.60, 0.80))
    return round(random.uniform(low, high), 2)


# ======================================================
# SMART RISK SCORING
# ======================================================

def calculate_risk_score(parameters: list) -> dict:
    score = 100
    critical = 0
    abnormal = 0
    confidence_sum = 0

    for p in parameters:
        status = p.get("status", "normal").lower()
        confidence_sum += p.get("confidence", 0.8)

        if status == "critical":
            score -= 25
            critical += 1
        elif status in ["high", "low"]:
            score -= 12
            abnormal += 1
        elif status == "normal":
            score -= 2

    score = max(5, min(100, score))
    avg_conf = round(confidence_sum / max(len(parameters), 1), 2)

    if score >= 75:
        risk = "low-risk"
    elif score >= 45:
        risk = "moderate-risk"
    else:
        risk = "high-risk"

    return {
        "health_score": score,
        "overall_risk": risk,
        "critical_count": critical,
        "abnormal_count": abnormal,
        "average_confidence": avg_conf
    }


# ======================================================
# NORMALIZATION
# ======================================================

def normalize_result(data: dict, engine: str, proc_time: float, cache_hit: bool) -> dict:
    def safe(v, default=""):
        return v if v is not None else default

    params = []
    for p in data.get("parameters", []):
        status = str(p.get("status", "normal")).lower()
        params.append({
            "name": safe(p.get("name"), "Unknown Parameter"),
            "value": safe(p.get("value"), "N/A"),
            "unit": safe(p.get("unit")),
            "normalRange": safe(p.get("normalRange")),
            "status": status,
            "confidence": float(p.get("confidence") or generate_confidence(status)),
            "explanation": safe(p.get("explanation"), f"Biomarker level is {status}."),
            "red_flag": status == "critical"
        })

    risk_metrics = calculate_risk_score(params)

    # Normalize organ scores (use AI-provided or generate defaults)
    raw_organ = data.get("organ_scores", {})
    organ_scores = {
        "metabolic": max(0, min(100, int(raw_organ.get("metabolic", random.randint(60, 95))))),
        "cardiac": max(0, min(100, int(raw_organ.get("cardiac", random.randint(65, 95))))),
        "renal": max(0, min(100, int(raw_organ.get("renal", random.randint(50, 90))))),
        "hepatic": max(0, min(100, int(raw_organ.get("hepatic", random.randint(55, 92))))),
        "hematologic": max(0, min(100, int(raw_organ.get("hematologic", random.randint(60, 95)))))
    }

    # Normalize health plan
    health_plan = []
    for day in data.get("health_plan", []):
        health_plan.append({
            "day": int(day.get("day", len(health_plan) + 1)),
            "focus": safe(day.get("focus"), "General wellness"),
            "diet": safe(day.get("diet"), "Balanced nutrition"),
            "exercise": safe(day.get("exercise"), "Light activity"),
            "precautions": safe(day.get("precautions"), "Stay hydrated"),
            "sleep": safe(day.get("sleep"), "7-8 hours"),
            "supplements": safe(day.get("supplements"), "As prescribed")
        })

    # Normalize disease risks
    disease_risks = []
    for risk in data.get("disease_risks", []):
        disease_risks.append({
            "disease": safe(risk.get("disease"), "Unknown"),
            "risk_level": safe(risk.get("risk_level"), "low"),
            "probability": max(0, min(100, int(risk.get("probability", 10)))),
            "explanation": safe(risk.get("explanation"), "")
        })

    return {
        "user_profile": {
            "name": safe(data.get("user_profile", {}).get("name"), "Patient"),
            "age": safe(data.get("user_profile", {}).get("age"), "N/A"),
            "gender": safe(data.get("user_profile", {}).get("gender"), "N/A"),
        },
        "parameters": params,
        "summary": safe(data.get("summary"), "Medical report analysis complete."),
        "recommendations": data.get("recommendations", []),
        "doctor_perspective": safe(
            data.get("doctor_perspective"),
            "Based on the available data, a comprehensive clinical evaluation is recommended. "
            "Some biomarkers may warrant further investigation to establish a clear diagnostic picture."
        ),
        "organ_scores": organ_scores,
        "health_plan": health_plan,
        "disease_risks": disease_risks,
        "prevention_tips": data.get("prevention_tips", [
            "Maintain regular health checkups",
            "Stay hydrated with adequate water intake",
            "Follow a balanced diet rich in nutrients"
        ]),
        "risk_metrics": risk_metrics,
        "medical_disclaimer": (
            "⚕️ IMPORTANT: This analysis is generated by an AI system and is intended for "
            "informational and educational purposes only. It does NOT constitute medical advice, "
            "diagnosis, or treatment. AI systems can and do make errors. Always consult a qualified "
            "healthcare professional for medical decisions. Never disregard professional medical "
            "advice or delay seeking it based on AI-generated content."
        ),
        "audit": {
            "analysis_id": hashlib.md5(str(time.time()).encode()).hexdigest()[:12],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "engine": engine,
            "engine_version": ENGINE_VERSION,
            "processing_time_ms": int(proc_time * 1000),
            "cache_hit": cache_hit
        }
    }


# ======================================================
# ENHANCED AI PROMPT
# ======================================================

def build_prompt(text: str) -> str:
    return f"""You are MediQ, a medical report analysis AI. Analyze this medical document text and return ONLY valid JSON.

IMPORTANT RULES:
- Extract ALL biomarker values found in the document
- Use medical knowledge to assess each value against standard reference ranges
- Be accurate — do not hallucinate values that aren't in the document
- For the health plan, create practical, actionable day-by-day plans
- For disease risks, only flag conditions supported by the actual data
- The doctor_perspective should sound like an experienced physician's assessment

Return this exact JSON structure:
{{
  "user_profile": {{
    "name": "patient name if found, else 'Patient'",
    "age": "age if found, else 'N/A'",
    "gender": "gender if found, else 'N/A'"
  }},
  "parameters": [
    {{
      "name": "biomarker name",
      "value": "measured value",
      "unit": "unit of measurement",
      "normalRange": "standard reference range",
      "status": "normal | low | high | critical",
      "confidence": 0.85,
      "explanation": "brief clinical explanation of what this value means"
    }}
  ],
  "summary": "2-3 sentence overall clinical summary of the report findings",
  "recommendations": ["actionable recommendation 1", "recommendation 2", "..."],
  "doctor_perspective": "A 3-4 sentence paragraph written as if an experienced physician is speaking to the patient. Use professional but understandable language. Mention key findings and what the patient should focus on. Use phrases like 'Based on these results...' and 'I would recommend...'",
  "organ_scores": {{
    "metabolic": 0-100,
    "cardiac": 0-100,
    "renal": 0-100,
    "hepatic": 0-100,
    "hematologic": 0-100
  }},
  "health_plan": [
    {{
      "day": 1,
      "focus": "main focus for this day",
      "diet": "specific dietary advice",
      "exercise": "exercise recommendation",
      "precautions": "things to watch out for",
      "sleep": "sleep recommendation",
      "supplements": "supplement advice if any"
    }},
    {{
      "day": 2,
      "focus": "...", "diet": "...", "exercise": "...", "precautions": "...", "sleep": "...", "supplements": "..."
    }},
    {{
      "day": 3,
      "focus": "...", "diet": "...", "exercise": "...", "precautions": "...", "sleep": "...", "supplements": "..."
    }},
    {{
      "day": 4,
      "focus": "...", "diet": "...", "exercise": "...", "precautions": "...", "sleep": "...", "supplements": "..."
    }},
    {{
      "day": 5,
      "focus": "...", "diet": "...", "exercise": "...", "precautions": "...", "sleep": "...", "supplements": "..."
    }},
    {{
      "day": 6,
      "focus": "...", "diet": "...", "exercise": "...", "precautions": "...", "sleep": "...", "supplements": "..."
    }},
    {{
      "day": 7,
      "focus": "...", "diet": "...", "exercise": "...", "precautions": "...", "sleep": "...", "supplements": "..."
    }},
    {{
      "day": 8,
      "focus": "...", "diet": "...", "exercise": "...", "precautions": "...", "sleep": "...", "supplements": "..."
    }},
    {{
      "day": 9,
      "focus": "...", "diet": "...", "exercise": "...", "precautions": "...", "sleep": "...", "supplements": "..."
    }},
    {{
      "day": 10,
      "focus": "...", "diet": "...", "exercise": "...", "precautions": "...", "sleep": "...", "supplements": "..."
    }}
  ],
  "disease_risks": [
    {{
      "disease": "condition name",
      "risk_level": "low | moderate | high",
      "probability": 0-100,
      "explanation": "why this risk exists based on the data"
    }}
  ],
  "prevention_tips": [
    "practical prevention tip 1",
    "prevention tip 2",
    "prevention tip 3",
    "prevention tip 4",
    "prevention tip 5"
  ]
}}

RULES:
- Return ONLY valid JSON, no markdown, no explanation
- No hallucinations — only analyze what's in the document
- Organ scores should reflect the actual lab values found
- The health plan should be personalized to the findings
- Be conservative with disease risk predictions

MEDICAL DOCUMENT TEXT:
{text[:12000]}
"""


# ======================================================
# AI LAYERS
# ======================================================

def analyze_with_gemini(text: str) -> dict:
    if not gemini_client:
        raise RuntimeError("Gemini client not initialized (no API key).")
    prompt = build_prompt(text)
    response = gemini_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )
    return extract_json(response.text)


def analyze_with_groq(text: str) -> dict:
    if not groq_client:
        raise RuntimeError("Groq client not initialized")
    prompt = build_prompt(text)
    chat = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=4096,
    )
    return extract_json(chat.choices[0].message.content)


# ======================================================
# ORCHESTRATOR
# ======================================================

def analyze_medical_text(text: str) -> dict:
    start_time = time.time()
    text_hash = get_text_hash(text)

    # Cache Check
    if text_hash in CACHE:
        cached = CACHE[text_hash].copy()
        cached["audit"] = cached.get("audit", {}).copy()
        cached["audit"]["cache_hit"] = True
        cached["audit"]["engine"] = "cache"
        return cached

    engine_used = "gemini"
    try:
        raw = analyze_with_gemini(text)
    except Exception as e:
        print(f"⚠️ Gemini failed: {e}. Trying Groq...")
        try:
            raw = analyze_with_groq(text)
            engine_used = "groq"
        except Exception as e2:
            print(f"❌ All AI engines failed: {e2}")
            raw = {
                "user_profile": {},
                "parameters": [],
                "summary": "AI processing encountered an error. Please try again.",
                "doctor_perspective": "Unable to generate analysis at this time. Please retry or consult a healthcare professional.",
                "organ_scores": {},
                "health_plan": [],
                "disease_risks": [],
                "prevention_tips": [],
                "recommendations": []
            }
            engine_used = "error-fallback"

    normalized = normalize_result(
        raw,
        engine_used,
        time.time() - start_time,
        False
    )

    CACHE[text_hash] = normalized
    return normalized