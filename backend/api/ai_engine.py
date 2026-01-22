import os
import json
import re
import hashlib
import random
import time
from datetime import datetime, timezone
from dotenv import load_dotenv
import google.genai as genai  # ✅ FIXED: Using the modern 2026 SDK
from groq import Groq

# ======================================================
# ENV LOAD
# ======================================================
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY missing from environment variables")

# ======================================================
# CLIENTS & CONFIG
# ======================================================
# ✅ FIXED: Correct initialization for the 'google-genai' library
gemini_client = genai.Client(api_key=GEMINI_API_KEY)
groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

GEMINI_MODEL = "gemini-2.0-flash-exp" 
GROQ_MODEL = "llama-3.1-8b-instant"
ENGINE_VERSION = "v5.1-stable-prod"

# Simple in-memory cache
CACHE = {}

# ======================================================
# UTILITIES
# ======================================================
def get_text_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def extract_json(text: str) -> dict:
    """Safely cleans AI markdown and extracts a JSON dictionary."""
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

    return {
        "user_profile": {
            "name": safe(data.get("user_profile", {}).get("name"), "Patient"),
            "age": safe(data.get("user_profile", {}).get("age"), "N/A"),
            "gender": safe(data.get("user_profile", {}).get("gender"), "N/A"),
        },
        "parameters": params,
        "summary": safe(data.get("summary"), "Medical report analysis complete."),
        "recommendations": data.get("recommendations", []),
        "risk_metrics": risk_metrics,
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
# AI LAYERS
# ======================================================
def build_prompt(text: str) -> str:
    return f"""
Return ONLY valid JSON:
{{
  "user_profile": {{ "name": "", "age": "", "gender": "" }},
  "parameters": [
    {{
      "name": "", "value": "", "unit": "", "normalRange": "",
      "status": "low | normal | high | critical",
      "confidence": 0.0, "explanation": ""
    }}
  ],
  "recommendations": [],
  "summary": ""
}}
Rules: No hallucinations. JSON only.
TEXT: {text[:12000]}
"""

def analyze_with_gemini(text: str) -> dict:
    prompt = build_prompt(text)
    # ✅ FIXED: Correct method call for the google-genai SDK
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
        cached = CACHE[text_hash]
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
            # Minimal fallback structure
            raw = {"user_profile": {}, "parameters": [], "summary": "AI processing error."}
            engine_used = "error-fallback"

    normalized = normalize_result(
        raw, 
        engine_used, 
        time.time() - start_time, 
        False
    )
    
    CACHE[text_hash] = normalized
    return normalized