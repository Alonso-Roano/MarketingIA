from fastapi import HTTPException, APIRouter, Depends
from pydantic import BaseModel
from app.common.middleware import verificar_acceso
from app.common.settings import GEMINI_API_KEY, GEMINI_BASE_URL
from openai import OpenAI
from typing import Optional

router = APIRouter(prefix="/gemini")

class ChatRequest(BaseModel):
    message: str
    system_message: Optional[str] = "You are a helpful assistant"

class ChatResponse(BaseModel):
    response: str

def get_gemini_client():
    """Crea y configura el cliente OpenAI para usar Gemini API"""
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="Gemini API key no configurada"
        )
    
    return OpenAI(
        api_key=GEMINI_API_KEY,
        base_url=GEMINI_BASE_URL
    )

@router.post("/chat", response_model=ChatResponse)
def chat_with_gemini(request: ChatRequest, _: None = Depends(verificar_acceso)):
    """
    Endpoint para chatear con Gemini
    """
    try:
        client = get_gemini_client()
        
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": request.system_message},
                {"role": "user", "content": request.message},
            ],
            stream=False
        )
        
        return ChatResponse(response=response.choices[0].message.content)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al comunicarse con Gemini: {str(e)}"
        )

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