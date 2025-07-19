from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from app.common.middleware import verificar_acceso
import os

router = APIRouter(prefix="/dataset")

@router.get("/marketing/descargar-datos", response_class=FileResponse)
def descargar_datos(_: None = Depends(verificar_acceso)):
    ruta_archivo = f"app/common/data/marketing_data.xlsx"
    
    if not os.path.exists(ruta_archivo):
        return {"error": "Archivo no encontrado"}

    return FileResponse(
        path=ruta_archivo,
        filename=f"marketing.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@router.get("/descipciones/descargar-datos", response_class=FileResponse)
def descargar_datos(_: None = Depends(verificar_acceso)):
    ruta_archivo = f"app/common/data/dataset_con_embeds.xlsx"
    
    if not os.path.exists(ruta_archivo):
        return {"error": "Archivo no encontrado"}

    return FileResponse(
        path=ruta_archivo,
        filename=f"descripciones.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )