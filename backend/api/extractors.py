# Only if Tesseract is NOT in your Windows PATH
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

import fitz  # PyMuPDF
import pytesseract
import pandas as pd
from pathlib import Path
from PIL import Image
import mimetypes


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
        print("❌ PDF Extraction Error:", e)

    return text.strip()


# ======================================================
# IMAGE OCR EXTRACTION
# ======================================================

def extract_image_text(file_path: Path) -> str:
    """
    OCR extraction from image files using Tesseract.
    Supports JPG / PNG / JPEG.
    """
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        print("❌ Image OCR Error:", e)
        return ""


# ======================================================
# CSV EXTRACTION
# ======================================================

def extract_csv_text(file_path: Path) -> str:
    """
    Convert CSV rows into readable medical sentences.
    """
    try:
        df = pd.read_csv(file_path)

        if df.empty:
            return ""

        lines = []

        for _, row in df.iterrows():
            sentence_parts = []

            for col, val in row.items():
                sentence_parts.append(f"{col} is {val}")

            sentence = ", ".join(sentence_parts)
            lines.append(sentence)

        return "\n".join(lines)

    except Exception as e:
        print("❌ CSV Extraction Error:", e)
        return ""


# ======================================================
# UNIFIED EXTRACTION ROUTER
# ======================================================

def extract_text(file_path: Path) -> str:
    """
    Auto-detect file type and extract text accordingly.
    """
    file_type = detect_file_type(file_path)

    print(f"📄 Detected file type: {file_type}")

    if file_type == "pdf":
        text = extract_pdf_text(file_path)

        # If scanned PDF has no text → try OCR fallback
        if not text:
            print("⚠️ PDF has no text. Trying OCR fallback...")
            try:
                images = convert_pdf_to_images(file_path)
                ocr_text = []
                for img in images:
                    ocr_text.append(pytesseract.image_to_string(img))
                return "\n".join(ocr_text).strip()
            except Exception as e:
                print("❌ PDF OCR fallback failed:", e)
                return ""

        return text

    if file_type == "image":
        return extract_image_text(file_path)

    if file_type == "csv":
        return extract_csv_text(file_path)

    raise ValueError("Unsupported file type")


# ======================================================
# PDF → IMAGE CONVERSION FOR OCR FALLBACK
# ======================================================

def convert_pdf_to_images(file_path: Path):
    """
    Convert PDF pages into images for OCR.
    """
    images = []
    try:
        doc = fitz.open(file_path)
        for page in doc:
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            images.append(img)
        doc.close()
    except Exception as e:
        print("❌ PDF Image Conversion Error:", e)

    return images