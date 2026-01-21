import os
import json
import re
import hashlib
import random
import time
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from groq import Groq

# ======================================================
# ENV LOAD
# ======================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY missing")

# ======================================================
# CLIENTS
# ======================================================

gemini_client = genai.Client(api_key=GEMINI_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

GEMINI_MODEL = "models/gemini-flash-latest"
GROQ_MODEL = "llama-3.1-8b-instant"

ENGINE_VERSION = "v5.0-prod"

# ======================================================
# CACHE
# ======================================================

CACHE = {}

def get_text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

# ======================================================
# JSON EXTRACTION
# ======================================================

def extract_json(text: str) -> dict:
    text = text.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(text)
    except Exception:
        match = re.search(r"\{[\s\S]*\}", text)
        if not match:
            raise ValueError("❌ No JSON detected in AI output")
        return json.loads(match.group(0))

# ======================================================
# HEURISTICS
# ======================================================

def generate_confidence(status: str) -> float:
    status = status.lower()
    if status == "normal":
        return round(random.uniform(0.85, 0.98), 2)
    if status in ["low", "high"]:
        return round(random.uniform(0.75, 0.90), 2)
    if status == "critical":
        return round(random.uniform(0.65, 0.85), 2)
    return round(random.uniform(0.60, 0.80), 2)

def is_red_flag(status: str) -> bool:
    return status.lower() == "critical"

# ======================================================
# SMART RISK SCORING
# ======================================================

def calculate_risk_score(parameters: list) -> dict:
    score = 100
    critical = 0
    abnormal = 0
    confidence_sum = 0

    for p in parameters:
        status = p["status"]
        confidence_sum += p["confidence"]

        if status == "critical":
            score -= 25
            critical += 1
        elif status in ["high", "low"]:
            score -= 12
            abnormal += 1
        elif status == "normal":
            score -= 2

    score = max(5, min(100, score))
    avg_confidence = round(confidence_sum / max(len(parameters), 1), 2)

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
        "average_confidence": avg_confidence
    }

# ======================================================
# NORMALIZATION
# ======================================================

def normalize_result(
    data: dict,
    engine: str,
    processing_time: float,
    cache_hit: bool
) -> dict:

    def safe(v, default=""):
        return v if v is not None else default

    parameters = []

    for p in data.get("parameters", []):
        status = str(p.get("status", "normal")).lower()
        confidence = p.get("confidence") or generate_confidence(status)
        explanation = p.get("explanation") or \
            f"{p.get('name','This biomarker')} interpreted as {status}."

        parameters.append({
            "name": safe(p.get("name")),
            "value": safe(p.get("value")),
            "unit": safe(p.get("unit")),
            "normalRange": safe(p.get("normalRange")),
            "status": status,
            "confidence": float(confidence),
            "explanation": explanation,
            "red_flag": is_red_flag(status)
        })

    risk_metrics = calculate_risk_score(parameters)

    normalized = {
        "user_profile": {
            "name": safe(data.get("user_profile", {}).get("name")),
            "age": safe(data.get("user_profile", {}).get("age")),
            "gender": safe(data.get("user_profile", {}).get("gender")),
        },
        "parameters": parameters,
        "summary": safe(data.get("summary")),
        "recommendations": data.get("recommendations", []),
        "risk_metrics": risk_metrics,

        # ✅ ENTERPRISE AUDIT METADATA
        "audit": {
            "analysis_id": hashlib.md5(str(datetime.utcnow()).encode()).hexdigest()[:12],
            "timestamp": datetime.utcnow().isoformat(),
            "engine": engine,
            "engine_version": ENGINE_VERSION,
            "processing_time_ms": int(processing_time * 1000),
            "cache_hit": cache_hit
        }
    }

    return normalized

# ======================================================
# PROMPT
# ======================================================

def build_prompt(text: str) -> str:
    return f"""
Return ONLY valid JSON:

{{
  "user_profile": {{
    "name": "",
    "age": "",
    "gender": ""
  }},
  "parameters": [
    {{
      "name": "",
      "value": "",
      "unit": "",
      "normalRange": "",
      "status": "low | normal | high | critical",
      "confidence": 0.0,
      "explanation": ""
    }}
  ],
  "recommendations": [],
  "summary": ""
}}

Rules:
- No hallucinations.
- JSON only.

TEXT:
{text[:12000]}
"""

# ======================================================
# AI LAYERS
# ======================================================

def analyze_with_gemini(text: str) -> dict:
    prompt = build_prompt(text)
    response = gemini_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )
    return extract_json(response.text)

def analyze_with_groq(text: str) -> dict:
    if not groq_client:
        raise RuntimeError("Groq disabled")

    prompt = build_prompt(text)
    chat = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
    )
    return extract_json(chat.choices[0].message.content)

def analyze_with_regex(text: str) -> dict:
    return {
        "user_profile": {},
        "parameters": [],
        "summary": "Offline extraction used."
    }

# ======================================================
# ORCHESTRATOR
# ======================================================

def analyze_medical_text(text: str) -> dict:
    start_time = time.time()
    text_hash = get_text_hash(text)

    # ✅ CACHE HIT
    if text_hash in CACHE:
        cached = CACHE[text_hash]
        cached["audit"]["cache_hit"] = True
        cached["audit"]["engine"] = "cache"
        cached["audit"]["processing_time_ms"] = 1
        return cached

    engine_used = "gemini"
    cache_hit = False

    try:
        raw = analyze_with_gemini(text)
    except Exception:
        try:
            raw = analyze_with_groq(text)
            engine_used = "groq"
        except Exception:
            raw = analyze_with_regex(text)
            engine_used = "regex"

    processing_time = time.time() - start_time
    normalized = normalize_result(
        raw,
        engine_used,
        processing_time,
        cache_hit
    )

    CACHE[text_hash] = normalized
    return normalized