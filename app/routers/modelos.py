from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.services.registry_models import MODEL_REGISTRY
from fastapi.responses import FileResponse
import os
import pandas as pd
import os
import traceback

router = APIRouter()

class ModeloUpdateRequest(BaseModel):
    modelos: List[int]

@router.post("/pokemon/actualizar")
def actualizar_modelos(request: ModeloUpdateRequest):
    resultados = []

    for modelo_id in request.modelos:
        func = MODEL_REGISTRY.get(modelo_id)
        if not func:
            resultados.append(f"Modelo {modelo_id} no implementado")
            continue
        try:
            resultado = func()
            resultados.append(f"Modelo {modelo_id}: {resultado}")
        except Exception as e:
            resultados.append(f"Error en modelo {modelo_id}: {str(e)}")

    return {"resultados": resultados}

class PokemonData(BaseModel):
    id: int
    identifier: str
    species_id: int
    height: int
    weight: int
    base_experience: int
    order: int
    is_default: bool

class InsertarDatosRequest(BaseModel):
    datos: List[PokemonData]

@router.post("/pokemon/agregar-datos")
def agregar_datos(request: InsertarDatosRequest):
    excel_path = f"app/common/data/pokemons.xlsx"

    if not os.path.exists(excel_path):
        raise HTTPException(status_code=404, detail="Archivo de datos no encontrado")

    try:
        # Cargar Excel existente
        df_existente = pd.read_excel(excel_path)

        # Convertir datos nuevos a DataFrame
        nuevos_datos = pd.DataFrame([d.dict() for d in request.datos])

        # Concatenar y guardar
        df_actualizado = pd.concat([df_existente, nuevos_datos], ignore_index=True)
        df_actualizado.to_excel(excel_path, index=False)

        return {"mensaje": f"{len(nuevos_datos)} registros agregados al dataset pokemons"}

    except Exception as e:
        print("ERROR INTERNO:", traceback.format_exc())  # 👈 Esto lo imprime completo en consola
        raise HTTPException(status_code=500, detail=f"Error al agregar datos: {str(e)}")
    
@router.get("/pokemon/descargar-datos", response_class=FileResponse)
def descargar_datos():
    ruta_archivo = f"app/common/data/pokemons.xlsx"
    
    if not os.path.exists(ruta_archivo):
        return {"error": "Archivo no encontrado"}

    return FileResponse(
        path=ruta_archivo,
        filename=f"modelo_pokemon.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
