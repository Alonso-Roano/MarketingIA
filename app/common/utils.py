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

def cargar_modelo(ruta: str):
    return joblib.load(ruta)

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
