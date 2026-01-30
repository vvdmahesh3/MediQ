import os
import uuid
import time
from pathlib import Path
from datetime import datetime, timezone

from flask import Flask, request, jsonify
from flask_cors import CORS

# Internal Modules
from ai_engine import analyze_medical_text
from extractors import extract_text


# -----------------------------------
# APP INITIALIZATION
# -----------------------------------

app = Flask(__name__)
CORS(app)

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

# -----------------------------------
# CONFIGURATION
# -----------------------------------

ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg", ".csv"}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

MAX_HISTORY = 15

# Session-scoped telemetry (resets on restart — acceptable for demo)
REPORT_HISTORY = []
SYSTEM_METRICS = {
    "total_files_processed": 0,
    "successful_scans": 0,
    "failed_scans": 0,
    "ocr_extractions": 0
}


# -----------------------------------
# HELPERS
# -----------------------------------

def validate_file(file):
    if not file or not file.filename:
        return False, "No file provided."

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Unsupported file type: {ext}"

    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)

    if size > MAX_FILE_SIZE_BYTES:
        return False, "File size exceeds 10MB limit."

    return True, None


def calculate_trend(history):
    if len(history) < 2:
        return "stable"

    try:
        current = history[-1]["health_score"]
        previous = history[-2]["health_score"]
        if current > previous:
            return "improving"
        if current < previous:
            return "declining"
    except Exception:
        pass

    return "stable"


def safe_delete(path: Path):
    try:
        if path.exists():
            path.unlink()
    except Exception:
        pass


# -----------------------------------
# ROUTES
# -----------------------------------

@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "service": "MediQ AI Analysis API",
        "status": "online",
        "version": "v5.1-stable"
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "supported_formats": list(ALLOWED_EXTENSIONS),
        "uptime": "active"
    })


@app.route("/upload", methods=["POST"])
def upload():
    start_time = time.time()
    session_id = f"SES-{uuid.uuid4().hex[:8].upper()}"

    if "file" not in request.files:
        SYSTEM_METRICS["failed_scans"] += 1
        return jsonify({"error": "No file received", "session_id": session_id}), 400

    file = request.files["file"]

    is_valid, error = validate_file(file)
    if not is_valid:
        SYSTEM_METRICS["failed_scans"] += 1
        return jsonify({"error": error, "session_id": session_id}), 400

    filename = f"{uuid.uuid4().hex}_{file.filename}"
    filepath = UPLOAD_DIR / filename
    file.save(filepath)

    try:
        extracted_text = extract_text(filepath)

        if not extracted_text or len(extracted_text.strip()) < 10:
            raise ValueError("Empty or unreadable document")

        ai_result = analyze_medical_text(extracted_text)

        processing_time = round(time.time() - start_time, 2)

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
        if len(REPORT_HISTORY) > MAX_HISTORY:
            REPORT_HISTORY.pop(0)

        SYSTEM_METRICS["total_files_processed"] += 1
        SYSTEM_METRICS["successful_scans"] += 1

        ai_result.update({
            "meta": snapshot,
            "history": REPORT_HISTORY,
            "trend": calculate_trend(REPORT_HISTORY),
            "system_stats": SYSTEM_METRICS
        })

        return jsonify(ai_result)

    except Exception as e:
        SYSTEM_METRICS["failed_scans"] += 1
        print(f"[ERROR] {str(e)}")

        return jsonify({
            "error": "Internal processing failure",
            "session_id": session_id
        }), 500

    finally:
        safe_delete(filepath)


@app.route("/history", methods=["GET"])
def history():
    return jsonify({
        "count": len(REPORT_HISTORY),
        "reports": REPORT_HISTORY,
        "metrics": SYSTEM_METRICS
    })


# -----------------------------------
# ENTRY POINT (Local only)
# -----------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
