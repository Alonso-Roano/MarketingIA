# app/routers/text_extraction_router.py

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.services.extract_service import extract_text_from_pdf
from app.common.middleware import verificar_acceso

router = APIRouter(prefix="/extract", tags=["Extractor Texto PDF"])

@router.post("/pdf")
async def extract_pdf_text(
    file: UploadFile = File(...),
    _: None = Depends(verificar_acceso)
):
    """
    Extrae todo el texto del PDF enviado.
    """
    try:
        content = extract_text_from_pdf(file)
        return {"text": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al extraer texto: {str(e)}")
