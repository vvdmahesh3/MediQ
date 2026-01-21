from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
from datetime import datetime, timezone
import uuid
import time

# Internal Imports
from ai_engine import analyze_medical_text
from extractors import extract_text   # ✅ FIXED IMPORT

app = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# ✅ Phase-6: Expanded allowed extensions
ALLOWED_EXTENSIONS = {'.pdf', '.png', '.jpg', '.jpeg', '.csv'}
MAX_FILE_SIZE_MB = 10 * 1024 * 1024  # 10MB

REPORT_HISTORY = []
MAX_HISTORY = 15

SYSTEM_METRICS = {
    "total_files_processed": 0,
    "successful_scans": 0,
    "failed_scans": 0,
    "ocr_extractions": 0
}

# -------------------------------
# HELPERS
# -------------------------------

def validate_file(file):
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Unsupported file type ({ext}). Upload PDF, Image, or CSV."

    file.seek(0, 2)
    size = file.tell()
    file.seek(0)

    if size > MAX_FILE_SIZE_MB:
        return False, "File too large. Max size is 10MB."

    return True, None

def calculate_trend(history):
    if len(history) < 2:
        return "stable"
    return (
        "improving"
        if history[-1]["health_score"] > history[-2]["health_score"]
        else "declining"
    )

# -------------------------------
# ROUTES
# -------------------------------

@app.route("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": "phase-6-multimodal",
        "supported_formats": list(ALLOWED_EXTENSIONS)
    }

@app.route("/upload", methods=["POST"])
def upload_file():
    start_time = time.time()
    session_id = f"SES-{uuid.uuid4().hex[:8].upper()}"

    if "file" not in request.files:
        SYSTEM_METRICS["failed_scans"] += 1
        return jsonify({
            "error": "No file detected in request",
            "session_id": session_id
        }), 400

    file = request.files["file"]

    # 1. Validation
    is_valid, error_msg = validate_file(file)
    if not is_valid:
        SYSTEM_METRICS["failed_scans"] += 1
        return jsonify({
            "error": error_msg,
            "session_id": session_id
        }), 400

    # 2. Save File
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    save_path = UPLOAD_DIR / filename
    file.save(save_path)

    try:
        # 3. Smart Extraction
        extracted_text = extract_text(save_path)

        if not extracted_text or len(extracted_text.strip()) < 10:
            return jsonify({
                "error": "Extraction failed. Document seems empty or unreadable.",
                "session_id": session_id
            }), 422

        # 4. AI Analysis
        ai_result = analyze_medical_text(extracted_text)

        processing_time = round(time.time() - start_time, 2)

        # 5. Telemetry Snapshot
        snapshot = {
            "report_id": f"REP-{uuid.uuid4().hex[:10].upper()}",
            "session_id": session_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "filename": file.filename,
            "file_type": Path(file.filename).suffix[1:].upper(),
            "health_score": ai_result["risk_metrics"]["health_score"],
            "overall_risk": ai_result["risk_metrics"]["overall_risk"],
            "processing_time": processing_time
        }

        REPORT_HISTORY.append(snapshot)
        REPORT_HISTORY[:] = REPORT_HISTORY[-MAX_HISTORY:]

        SYSTEM_METRICS["total_files_processed"] += 1
        SYSTEM_METRICS["successful_scans"] += 1

        ai_result["meta"] = snapshot
        ai_result["history"] = REPORT_HISTORY
        ai_result["trend"] = calculate_trend(REPORT_HISTORY)
        ai_result["system_stats"] = SYSTEM_METRICS

        return jsonify(ai_result)

    except Exception as e:
        SYSTEM_METRICS["failed_scans"] += 1
        print(f"🔥 ERROR: {str(e)}")
        return jsonify({
            "error": "Processing Engine Failure",
            "details": str(e),
            "session_id": session_id
        }), 500

@app.route("/history", methods=["GET"])
def get_history():
    return jsonify({
        "count": len(REPORT_HISTORY),
        "reports": REPORT_HISTORY,
        "metrics": SYSTEM_METRICS
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)