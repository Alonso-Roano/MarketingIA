from app.schemas.pokemon_schema import PokemonData
from app.common.utils import cargar_modelo
from sklearn.metrics import accuracy_score, classification_report
import io
import os
import pandas as pd
from datetime import datetime
import shap
import joblib

modelo = cargar_modelo("app/models/model_pokemon/current_model.pkl")

def predecir_pokemon(data: PokemonData):
    entrada = [[
        data.species_id,
        data.height,
        data.weight,
        data.base_experience,
        data.order
    ]]
    pred = modelo.predict(entrada)
    return {"is_default": bool(pred[0])}

def get_model_info():
    metadata = {
        "nombre": "Clasificador de pokémon",
        "descripcion": "Clasifica el tipo de pokémon según sus estadísticas base",
        "campos_esperados": ["height", "weight", "base_experience"],
        "tipo_modelo": "Regresión logística",
    }

    if not metadata:
        raise ValueError("Modelo no registrado.")

    path = f"app/models/model_pokemon/current_model.pkl"
    if not os.path.exists(path):
        raise ValueError("Modelo no entrenado aún.")

    last_updated = datetime.fromtimestamp(os.path.getmtime(path)).isoformat()

    # Leemos el dataset base (cambiar según el modelo)
    df = pd.read_excel("app/common/data/pokemons.xlsx")

    # .info() no se puede convertir directamente en string → capturamos la salida
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()

    return {
        "metadata": {
            **metadata,
            "ultima_actualizacion": last_updated
        },
        "dataset": {
            "columnas": df.columns.tolist(),
            "primeras_filas": df.head(5).to_dict(orient="records"),
            "estadisticas": df.describe().to_dict(),
            "info": info_str
        }
    }

def get_model_metrics():
    df = pd.read_excel("app/common/data/pokemons.xlsx")
    
    X = df[["species_id", "height", "weight", "base_experience", "order"]]
    y = df["species_id"]

    y_pred = modelo.predict(X)

    acc = accuracy_score(y, y_pred)
    report = classification_report(y, y_pred, output_dict=True)

    return {
        "accuracy": acc,
        "reporte": report
    }

def explicar_prediccion(datos: dict):
    df = pd.DataFrame([datos])

    explainer = shap.Explainer(modelo.predict, df)
    shap_values = explainer(df)

    explicacion = {
        "prediccion": int(modelo.predict(df)[0]),
        "shap_values": shap_values.values[0].tolist(),
        "atribuciones": {
            feature: round(value, 4)
            for feature, value in zip(df.columns, shap_values.values[0])
        }
    }
    return explicacion