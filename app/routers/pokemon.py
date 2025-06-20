from pydantic import BaseModel
from typing import Dict
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.schemas.pokemon_schema import PokemonData
import os
from app.services.pokemon_service import predecir_pokemon, get_model_info, get_model_metrics, explicar_prediccion

router = APIRouter()

@router.post("/predict")
def predict(data: PokemonData):
    return predecir_pokemon(data)

@router.get("/info")
def modelo_info():
    try:
        info = get_model_info()
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metricas")
def modelo_metricas():
    try:
        return get_model_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
class DatosEntrada(BaseModel):
    datos: Dict[str, float]

@router.post("/explicar")
def explicar(entrada: DatosEntrada):
    try:
        explicacion = explicar_prediccion(entrada.datos)
        return explicacion
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
