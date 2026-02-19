# src/parser.py

import re


def clean_text(text: str) -> list:
    """
    Convert OCR text into cleaned product list
    """

    lines = text.split("\n")
    cleaned_items = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Remove header/footer words
        if re.search(r"(TOTAL|DATE|TIME|INVOICE|SUPERMARKET|FRESH MART)", line, re.I):
            continue

        # Remove prices and numbers
        line = re.sub(r"\$?\d+(\.\d+)?", "", line)

        # Remove any digits left
        line = re.sub(r"\d+", "", line)

        # Remove common measurement units anywhere in string
        line = re.sub(r"(kg|g|ml|l|okg|ke|lkg|pcs|pc)", "", line, flags=re.I)

        # Remove non-letters
        line = re.sub(r"[^A-Za-z\s]", "", line)

        # Remove extra spaces
        line = re.sub(r"\s+", " ", line)

        line = line.strip()

        if len(line) >= 3:
            cleaned_items.append(line.upper())

    return cleaned_items
