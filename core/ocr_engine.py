import pytesseract
from PIL import Image
import sys

# Smart path check: Only use the C:\ drive if running on a Windows machine
if sys.platform == "win32":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ocr_image(file_stream) -> str:
    try:
        img = Image.open(file_stream)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        return f"OCR Image Error: {str(e)}"