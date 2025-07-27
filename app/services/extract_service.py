# app/services/extract_service.py

import fitz  # PyMuPDF
from fastapi import UploadFile

def extract_text_from_pdf(file: UploadFile) -> str:
    """
    Extrae todo el texto de un archivo PDF usando PyMuPDF (fitz).
    """
    file_bytes = file.file.read()
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        return "\n".join(page.get_text() for page in doc)
