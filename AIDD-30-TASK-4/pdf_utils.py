# pdf_utils.py
from PyPDF2 import PdfReader

def extract_pdf_text(path: str) -> str:
    """
    Extract text from all pages of a PDF and return as a single string.
    """
    reader = PdfReader(path)
    parts = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            parts.append(text)
    return "\n\n".join(parts)
