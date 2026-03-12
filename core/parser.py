import re

def clean_items(text: str) -> list:
    lines = text.split("\n")
    cleaned_items = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if re.search(r"(TOTAL|DATE|TIME|INVOICE|SUPERMARKET|FRESH MART)", line, re.I):
            continue
            
        line = re.sub(r"\$?\d+(\.\d+)?", "", line)
        line = re.sub(r"\d+", "", line)
        line = re.sub(r"\b(kg|g|ml|l|okg|ke|lkg|pcs|pc)\b", "", line, flags=re.I)
        line = re.sub(r"[^A-Za-z\s]", "", line)
        line = re.sub(r"\s+", " ", line).strip()
        
        if len(line) >= 3:
            cleaned_items.append(line.upper())
            
    return cleaned_items