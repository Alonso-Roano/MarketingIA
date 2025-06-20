import joblib

def cargar_modelo(ruta: str):
    return joblib.load(ruta)
