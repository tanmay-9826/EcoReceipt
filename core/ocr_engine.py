import pytesseract
from PIL import Image

def ocr_image(file_stream) -> str:
    try:
        img = Image.open(file_stream)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        return f"OCR Image Error: {str(e)}"