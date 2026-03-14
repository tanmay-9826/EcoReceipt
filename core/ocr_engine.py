import pytesseract
from PIL import Image

# This line is the magic fix. It tells Python EXACTLY where Tesseract lives on your computer.
# If your Tesseract is installed somewhere else, change this path!
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def ocr_image(file_stream) -> str:
    try:
        img = Image.open(file_stream)
        text = pytesseract.image_to_string(img)
        return text.strip()
    except Exception as e:
        return f"OCR Image Error: {str(e)}"