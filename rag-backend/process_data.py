import re
import fitz
from typing import List

# Extract text from a PDF file
def extract_text_pymupdf(pdf_path:str)->str:
    doc = fitz.open(pdf_path)
    text = ""
    for page_num, page in enumerate(doc, start=1):
        text += f"Page {page_num}:\n"
        text += page.get_text() + "\n"
    return text

def clean_text(text:str)->str:
    # Remove special characters
    text = re.sub(r"[^a-zA-Z0-9\s.,!?-]", "", text)
    # Replace multiple spaces with a single space
    text = re.sub(r"\s+", " ", text)
    # Strip leading/trailing whitespace
    text = text.strip()
    return text

def split_into_chunks(text: str, chunk_size: int = 100, overlap: int = 20) -> List[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i : i + chunk_size])
        chunks.append(chunk)
    return chunks

