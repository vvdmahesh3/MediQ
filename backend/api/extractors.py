import fitz  # PyMuPDF
import pytesseract
import pandas as pd
import mimetypes
import os
from pathlib import Path
from PIL import Image

# ======================================================
# CONFIGURATION
# ======================================================

# On Railway/Linux, 'tesseract' is usually in the PATH automatically.
# This line is only needed for local Windows development:
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# ======================================================
# FILE TYPE DETECTION
# ======================================================

def detect_file_type(file_path: Path) -> str:
    """
    Detect file type using extension + mimetype fallback.
    Returns: pdf | image | csv | unknown
    """
    ext = file_path.suffix.lower()

    if ext == ".pdf":
        return "pdf"

    if ext in [".png", ".jpg", ".jpeg"]:
        return "image"

    if ext == ".csv":
        return "csv"

    # Fallback using mimetype
    mime, _ = mimetypes.guess_type(str(file_path))
    if mime:
        if "pdf" in mime:
            return "pdf"
        if "image" in mime:
            return "image"
        if "csv" in mime:
            return "csv"

    return "unknown"


# ======================================================
# PDF EXTRACTION
# ======================================================

def extract_pdf_text(file_path: Path) -> str:
    """
    Extract text from digital PDFs using PyMuPDF.
    """
    text = ""
    try:
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        print(f"❌ PDF Extraction Error: {e}")

    return text.strip()


# ======================================================
# IMAGE OCR EXTRACTION
# ======================================================

def extract_image_text(file_path: Path) -> str:
    """
    OCR extraction from image files using Tesseract.
    """
    try:
        image = Image.open(file_path)
        # We use lang='eng' for medical reports; add others if needed
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        print(f"❌ Image OCR Error: {e}")
        return ""


# ======================================================
# CSV EXTRACTION
# ======================================================

def extract_csv_text(file_path: Path) -> str:
    """
    Convert CSV rows into readable medical sentences for the AI.
    """
    try:
        df = pd.read_csv(file_path)

        if df.empty:
            return ""

        lines = []
        for _, row in df.iterrows():
            sentence_parts = [f"{col} is {val}" for col, val in row.items() if pd.notna(val)]
            if sentence_parts:
                lines.append(", ".join(sentence_parts))

        return "\n".join(lines)

    except Exception as e:
        print(f"❌ CSV Extraction Error: {e}")
        return ""


# ======================================================
# PDF → IMAGE CONVERSION FOR OCR FALLBACK
# ======================================================

def convert_pdf_to_images(file_path: Path):
    """
    Convert PDF pages into high-resolution images for OCR fallback.
    Used when a PDF is a 'scanned' image rather than digital text.
    """
    images = []
    try:
        doc = fitz.open(file_path)
        for page in doc:
            # Increase resolution (zoom) for better OCR accuracy
            zoom = 2  
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(img)
        doc.close()
    except Exception as e:
        print(f"❌ PDF Image Conversion Error: {e}")

    return images


# ======================================================
# UNIFIED EXTRACTION ROUTER (The Main Function)
# ======================================================

def extract_text(file_path: Path) -> str:
    """
    Auto-detect file type and extract text accordingly.
    Includes OCR fallback for scanned PDFs.
    """
    if not file_path.exists():
        return ""

    file_type = detect_file_type(file_path)
    print(f"🔍 Extraction Engine: Processing {file_type} file...")

    if file_type == "pdf":
        text = extract_pdf_text(file_path)

        # If the text is empty, the PDF is likely a scanned image.
        if not text or len(text.strip()) < 20:
            print("⚠️ Digital text not found. Starting OCR Fallback...")
            try:
                images = convert_pdf_to_images(file_path)
                ocr_results = []
                for img in images:
                    ocr_results.append(pytesseract.image_to_string(img))
                return "\n".join(ocr_results).strip()
            except Exception as e:
                print(f"❌ OCR Fallback failed: {e}")
                return ""
        return text

    if file_type == "image":
        return extract_image_text(file_path)

    if file_type == "csv":
        return extract_csv_text(file_path)

    print(f"❌ Unsupported file type detected: {file_type}")
    return ""