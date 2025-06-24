from fastapi import APIRouter, HTTPException, Depends
from app.services.dataset_service import entrenar_modelo, agregar_datos_excel, eliminar_fila_por_id, actualizar_campo_por_id, obtener_dataset
from fastapi.responses import FileResponse, JSONResponse, Response
from app.services.registry_model import MODEL_REGISTRY
from app.schemas.student_schema import SocialUpdateData, InsertarDatosSocialRequest
from app.common.middleware import verificar_acceso, verificar_admin
import os
import gzip
import json

router = APIRouter(prefix="/dataset")

@router.put("/{modelo_nombre}/actualizar")
def actualizar_modelo_individual(modelo_nombre: str, _: None = Depends(verificar_admin)):
    if modelo_nombre not in MODEL_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Modelo '{modelo_nombre}' no encontrado")

    model_info = MODEL_REGISTRY[modelo_nombre]
    
    try:
        resultado = entrenar_modelo(
            dataset=model_info["dataset"],
            campos_entrada=model_info["input_fields"],
            campo_objetivo=model_info["target_field"],
            tipo_modelo=model_info["model_type"],
            carpeta_modelo=model_info["model_path"]
        )
        return {"mensaje": f"Modelo '{modelo_nombre}' actualizado: {resultado}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/actualizar-todos")
def actualizar_todos_modelos(_: None = Depends(verificar_admin)):
    resultados = []

    for i, (modelo_nombre, modelo_data) in enumerate(MODEL_REGISTRY.items(), start=1):
        model_info = modelo_data
        try:
            resultado = entrenar_modelo(
                dataset=model_info["dataset"],
                campos_entrada=model_info["input_fields"],
                campo_objetivo=model_info["target_field"],
                tipo_modelo=model_info["model_type"],
                carpeta_modelo=model_info["model_path"]
            )
            resultados.append({
                "numero": i,
                "modelo": modelo_nombre,
                "resultado": resultado
            })
        except Exception as e:
            resultados.append({
                "numero": i,
                "modelo": modelo_nombre,
                "error": str(e)
            })

    return JSONResponse(content={"modelos_actualizados": resultados})

@router.get("/student/descargar-datos", response_class=FileResponse)
def descargar_datos(_: None = Depends(verificar_admin)):
    ruta_archivo = f"app/common/data/students_cleaned.xlsx"
    
    if not os.path.exists(ruta_archivo):
        return {"error": "Archivo no encontrado"}

    return FileResponse(
        path=ruta_archivo,
        filename=f"students_cleaned.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

@router.get("/student/dataset-json")
def obtener_dataset_json(_: None = Depends(verificar_acceso)):
    ruta_excel = "app/common/data/students_cleaned.xlsx"

    try:
        df = obtener_dataset(ruta_excel)
        datos_compactos = df.to_dict(orient="split")

        # Serializar a JSON y luego comprimir con gzip
        json_bytes = json.dumps({"dataset": datos_compactos}).encode("utf-8")
        compressed = gzip.compress(json_bytes)

        return Response(
            content=compressed,
            media_type="application/json",
            headers={"Content-Encoding": "gzip"}
        )

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el dataset: {str(e)}")

@router.post("/student/agregar-datos")
def agregar_datos(request: InsertarDatosSocialRequest, _: None = Depends(verificar_acceso)):
    ruta_excel = "app/common/data/students_cleaned.xlsx"
    try:
        mensaje = agregar_datos_excel(
            ruta_excel,
            [d.dict() for d in request.datos],
            nombre_dataset="dataset estudiantes",
            no_repite="Student_ID"
        )
        return {"mensaje": mensaje}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/student/{student_id}")
def actualizar(student_id: int, datos: SocialUpdateData, _: None = Depends(verificar_admin)):
    ruta_excel = "app/common/data/students_cleaned.xlsx"
    try:
        campos_actualizados = datos.dict(exclude_none=True)

        if not campos_actualizados:
            raise HTTPException(status_code=400, detail="No se proporcionó ningún campo para actualizar")

        mensaje = actualizar_campo_por_id(
            ruta_excel,
            id_columna="Student_ID",
            id_valor=student_id,
            nuevos_datos=campos_actualizados
        )
        return {"mensaje": mensaje}

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/student/{student_id}")
def eliminar(student_id: int, _: None = Depends(verificar_admin)):
    ruta_excel = "app/common/data/students_cleaned.xlsx"
    try:
        mensaje = eliminar_fila_por_id(ruta_excel, "Student_ID", student_id)
        return {"mensaje": mensaje}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))