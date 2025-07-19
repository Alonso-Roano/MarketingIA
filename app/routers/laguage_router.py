from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.common.middleware import verificar_acceso
from app.services.language_service import obtener_conceptos_desde_texto, predecir_keywords, predecir_categoria

router = APIRouter(prefix="/language")

class TextoEntrada(BaseModel):
    descripcion: str

@router.post("/predecir/rubro")
def predecir_categoria_api(entrada: TextoEntrada, _: None = Depends(verificar_acceso)):
    conceptos = obtener_conceptos_desde_texto(entrada.descripcion, usar_lemma=False)
    return predecir_categoria(conceptos)


@router.post("/predecir/keywords")
def predecir_keywords_api(entrada: TextoEntrada, _: None = Depends(verificar_acceso)):
    conceptos = obtener_conceptos_desde_texto(entrada.descripcion, usar_lemma=True)
    return predecir_keywords(conceptos)

