# src/ocr_engine.py

import pytesseract
import pdfplumber
from PIL import Image
from pathlib import Path


def ocr_image(image_path: str) -> str:
    """
    Extract text from image using Tesseract
    """
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        return f"OCR Image Error: {str(e)}"


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from PDF using pdfplumber
    """
    try:
        full_text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
        return full_text.strip()
    except Exception as e:
        return f"OCR PDF Error: {str(e)}"
