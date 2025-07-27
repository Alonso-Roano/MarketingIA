from fastapi import HTTPException, APIRouter, Depends,  UploadFile, File
from pydantic import BaseModel
from app.common.middleware import verificar_acceso
from typing import Optional
from app.common.utils import enviar_mensaje_a_gemini, get_gemini_client
import shutil
import os
from app.services.gemini_service import generate_campaign_from_pdf
router = APIRouter(prefix="/gemini")

class ChatRequest(BaseModel):
    message: str
    system_message: Optional[str] = "You are a helpful assistant"

class ChatResponse(BaseModel):
    response: str


@router.post("/chat", response_model=ChatResponse)
def chat_with_gemini(request: ChatRequest, _: None = Depends(verificar_acceso)):
    """
    Endpoint para chatear con Gemini
    """
    try:
        respuesta = enviar_mensaje_a_gemini(
            system_message=request.system_message,
            user_message=request.message
        )
        return ChatResponse(response=respuesta)

    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
def health_check(_: None = Depends(verificar_acceso)):
    """
    Endpoint para verificar el estado de la conexión con Gemini
    """
    try:
        client = get_gemini_client()
        
        test_response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": "Hello"},
            ],
            stream=False,
            max_tokens=10
        )
        
        return {
            "status": "healthy",
            "message": "Conexión con Gemini API exitosa",
            "test_response": test_response.choices[0].message.content
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error de conexión con Gemini: {str(e)}"
        ) 
    
@router.post("/extract-from-pdf")
async def extract_form_fields_from_pdf(
    file: UploadFile = File(...),
    _: None = Depends(verificar_acceso)
):
    """
    Extrae texto del PDF y genera sugerencias de formulario con Gemini.
    """
    try:
        json_sugerido = generate_campaign_from_pdf(file)
        return {"form_fields": json_sugerido}
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

