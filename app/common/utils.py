import pandas as pd
import joblib
import io
import os
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score, classification_report,
    mean_squared_error, r2_score
)
from sklearn.base import RegressorMixin
import numpy as np
from statistics import mode
import numpy as np
from app.common.settings import GEMINI_API_KEY, GEMINI_BASE_URL
from openai import OpenAI
from fastapi import HTTPException

def cargar_modelo(ruta: str):
    return joblib.load(ruta, mmap_mode='r')

def predecir_instancia(modelo, datos_input: dict, ruta_dataset: str, campos: list[str]) -> dict:
    df = pd.read_excel(ruta_dataset)
    datos_completos = {}

    for campo in campos:
        valor = datos_input.get(campo)

        if valor is not None:
            datos_completos[campo] = valor
        else:
            columna = df[campo].dropna()

            if columna.empty:
                datos_completos[campo] = None
            elif pd.api.types.is_numeric_dtype(columna):
                datos_completos[campo] = columna.mean()
            else:
                try:
                    datos_completos[campo] = mode(columna)
                except:
                    datos_completos[campo] = columna.mode().iloc[0]

    entrada = [[datos_completos[c] for c in campos]]
    pred = modelo.predict(entrada)

    resultado = pred.tolist() if isinstance(pred, np.ndarray) else pred

    return {
        "prediccion": resultado[0]
    }


def obtener_info_dataset(ruta_excel: str, metadata: dict):
    if not os.path.exists(ruta_excel):
        raise FileNotFoundError("Dataset no encontrado")

    df = pd.read_excel(ruta_excel)
    buffer = io.StringIO()
    df.info(buf=buffer)

    return {
        "metadata": {
            **metadata,
            "ultima_actualizacion": datetime.fromtimestamp(
                os.path.getmtime(ruta_excel)
            ).isoformat()
        },
        "dataset": {
            "columnas": df.columns.tolist(),
            "primeras_filas": df.head(5).to_dict(orient="records"),
            "estadisticas": df.describe().to_dict(),
            "info": buffer.getvalue()
        }
    }

def calcular_metricas(modelo, ruta_excel: str, campos_entrada: list[str], campo_objetivo: str):
    df = pd.read_excel(ruta_excel)
    X = df[campos_entrada]
    y = df[campo_objetivo]
    y_pred = modelo.predict(X)

    ejemplos = [
        {
            "input": X.iloc[i].to_dict(),
            "real": y.iloc[i],
            "predicho": y_pred[i]
        }
        for i in range(min(10, len(X)))
    ]
    print(f"DEBUG: Tipo del modelo: {type(modelo)}")
    if isinstance(modelo, RandomForestClassifier):
        return {
            "tipo": "clasificacion",
            "accuracy": float(accuracy_score(y, y_pred)),  # por si acaso
            "reporte": convertir_a_python(classification_report(y, y_pred, output_dict=True)),
            "ejemplos": convertir_a_python(ejemplos)
        }

    elif isinstance(modelo, RegressorMixin):
        return {
            "tipo_modelo": "regresión",
            "rmse": float(np.sqrt(mean_squared_error(y, y_pred))),
            "r2_score": float(r2_score(y, y_pred)),
            "ejemplos": [
                {
                    "input": convertir_a_python(X.iloc[i].to_dict()),
                    "real": float(y.iloc[i]),
                    "predicho": float(y_pred[i])
                }
                for i in range(min(10, len(X)))
            ]
        }

    else:
        raise ValueError("Tipo de modelo no soportado. Se esperaba un modelo de clasificación o regresión.")

def convertir_a_python(obj):
    if isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: convertir_a_python(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convertir_a_python(elem) for elem in obj]
    else:
        return obj

def crear_payloads_por_modelo(payload_maestro: dict, registry: dict):
    
    resultado = {}

    for modelo, config in registry.items():
        campos_requeridos = config.get("input_fields", [])
        sub_payload = {}
        faltantes = []

        for campo in campos_requeridos:
            if campo in payload_maestro:
                sub_payload[campo] = payload_maestro[campo]
            else:
                faltantes.append(campo)

        resultado[modelo] = {
            "payload": sub_payload,
            "faltantes": faltantes
        }

    return resultado


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

def enviar_mensaje_a_gemini(system_message: str, user_message: str) -> str:
    """
    Envía un mensaje a Gemini y retorna la respuesta.
    """
    try:
        client = get_gemini_client()
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Error al comunicarse con Gemini: {str(e)}")
