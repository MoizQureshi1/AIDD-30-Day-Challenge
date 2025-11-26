# pdf_utils.py
from PyPDF2 import PdfReader

def extract_pdf_text(path: str) -> str:
    reader = PdfReader(path)
    text_parts = []
    for p in reader.pages:
        page_text = p.extract_text() or ""
        text_parts.append(page_text)
    return "\n\n".join(text_parts)
