from fastapi import APIRouter, HTTPException, Body, Depends
from app.services.registry_model import MODEL_REGISTRY, estan_modelos_listos, progreso_carga_modelos
from app.common.middleware import verificar_acceso

router = APIRouter(prefix="/modelo")

def check_modelos_listos():
    if not estan_modelos_listos():
        raise HTTPException(503, detail="Modelos aún cargando, intenta más tarde.")

@router.get("/{modelo}/info")
def modelo_info(modelo: str, _: None = Depends(verificar_acceso)):
    check_modelos_listos()
    entry = MODEL_REGISTRY.get(modelo)
    if not entry:
        raise HTTPException(404, detail="Modelo no encontrado")
    return entry["service"].obtener_info()

@router.get("/{modelo}/metricas")
def modelo_metricas(modelo: str, _: None = Depends(verificar_acceso)):
    check_modelos_listos()
    entry = MODEL_REGISTRY.get(modelo)
    if not entry:
        raise HTTPException(404, detail="Modelo no encontrado")
    return entry["service"].obtener_metricas()

@router.post("/{modelo}/predict")
def modelo_predict(modelo: str, payload: dict = Body(...), _: None = Depends(verificar_acceso)):
    check_modelos_listos()
    entry = MODEL_REGISTRY.get(modelo)
    if not entry:
        raise HTTPException(404, detail="Modelo no encontrado")
    schema = entry["schema"]
    try:
        data = schema(**payload)
    except Exception as e:
        raise HTTPException(400, detail=f"Error de validación: {e}")
    return entry["service"].predecir(data.dict())
