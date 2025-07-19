from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.common.middleware import verificar_acceso
from typing import List, Optional
from app.services.ai21_service import MisionVisionResponse, generar_mision_vision_desde_ai21

router = APIRouter(prefix="/ai21")

class EmpresaRequest(BaseModel):
    descripcion: str
    rubro: Optional[str] = ""
    tamano: str
    alcance: str
    palabras_clave: Optional[List[str]] = []

@router.post("/generar-mision-vision", response_model=MisionVisionResponse)
def generar_mision_vision(request: EmpresaRequest, _: None = Depends(verificar_acceso)):
    return generar_mision_vision_desde_ai21(
        descripcion=request.descripcion,
        rubro=request.rubro,
        tamano=request.tamano,
        alcance=request.alcance,
        palabras_clave=request.palabras_clave
    )