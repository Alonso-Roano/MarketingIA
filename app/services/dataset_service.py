import pandas as pd
import joblib
import os
import traceback
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from app.common.enums import ModeloTipo, DatasetTipo
from datetime import datetime, timedelta
import shutil

def entrenar_modelo(
    dataset: DatasetTipo,
    campos_entrada: list[str],
    campo_objetivo: str,
    tipo_modelo: ModeloTipo,
    carpeta_modelo: str
):
    # Ruta del dataset
    ruta_dataset = os.path.join("app", "common", "data", dataset)
    if not os.path.exists(ruta_dataset):
        raise FileNotFoundError(f"Dataset no encontrado: {ruta_dataset}")

    # Cargar datos
    df = pd.read_excel(ruta_dataset)

    # Validar columnas
    columnas_faltantes = [c for c in campos_entrada + [campo_objetivo] if c not in df.columns]
    if columnas_faltantes:
        raise ValueError(f"Columnas no encontradas en el dataset: {columnas_faltantes}")

    X = df[campos_entrada]
    y = df[campo_objetivo]

    # Seleccionar modelo
    if tipo_modelo == ModeloTipo.random_forest:
        modelo = RandomForestClassifier()
    elif tipo_modelo == ModeloTipo.random_forest_regressor:
        modelo = RandomForestRegressor()
    elif tipo_modelo == ModeloTipo.linear_regression:
        modelo = LinearRegression()
    else:
        raise ValueError(f"Modelo no soportado: {tipo_modelo}")
    # Entrenar
    modelo.fit(X, y)

    # Asegurar carpeta de salida
    ruta_salida = os.path.join("app", "models", carpeta_modelo)
    os.makedirs(ruta_salida, exist_ok=True)

    # Guardar modelo
    ruta_modelo = os.path.join(ruta_salida, "current_model.pkl")
    joblib.dump(modelo, ruta_modelo)

    return f"Modelo entrenado y guardado en {ruta_modelo}"

def agregar_datos_excel(ruta_excel: str, datos_nuevos: list[dict], nombre_dataset: str = "dataset"):
    if not os.path.exists(ruta_excel):
        raise FileNotFoundError(f"Archivo de datos no encontrado en: {ruta_excel}")
    
    hacer_respaldo(ruta_excel)

    try:
        df_existente = pd.read_excel(ruta_excel)
        df_nuevos = pd.DataFrame(datos_nuevos)
        df_actualizado = pd.concat([df_existente, df_nuevos], ignore_index=True)
        df_actualizado.to_excel(ruta_excel, index=False)
        return f"{len(df_nuevos)} registros agregados al {nombre_dataset}"

    except Exception as e:
        print("ERROR INTERNO:", traceback.format_exc())
        raise Exception(f"Error al agregar datos: {str(e)}")

def eliminar_fila_por_id(ruta_excel: str, id_columna: str, id_valor: int | str):
    if not os.path.exists(ruta_excel):
        raise FileNotFoundError(f"Archivo de datos no encontrado en: {ruta_excel}")
    
    hacer_respaldo(ruta_excel)

    df = pd.read_excel(ruta_excel)

    if id_columna not in df.columns:
        raise ValueError(f"La columna '{id_columna}' no existe en el dataset")

    filas_iniciales = len(df)
    df_filtrado = df[df[id_columna] != id_valor]
    filas_finales = len(df_filtrado)

    if filas_iniciales == filas_finales:
        raise ValueError(f"No se encontró ningún registro con {id_columna} = {id_valor}")

    df_filtrado.to_excel(ruta_excel, index=False)

    return f"Fila con {id_columna}={id_valor} eliminada correctamente"

def actualizar_campo_por_id(ruta_excel: str, id_columna: str, id_valor: int | str, nuevos_datos: dict):
    if not os.path.exists(ruta_excel):
        raise FileNotFoundError(f"Archivo de datos no encontrado en: {ruta_excel}")
    
    hacer_respaldo(ruta_excel)

    df = pd.read_excel(ruta_excel)

    if id_columna not in df.columns:
        raise ValueError(f"La columna '{id_columna}' no existe en el dataset")

    indice = df[df[id_columna] == id_valor].index
    if len(indice) == 0:
        raise ValueError(f"No se encontró ningún registro con {id_columna} = {id_valor}")

    idx = indice[0]

    for campo, valor in nuevos_datos.items():
        if campo not in df.columns:
            raise ValueError(f"El campo '{campo}' no existe en el dataset")
        df.at[idx, campo] = valor

    df.to_excel(ruta_excel, index=False)

    return f"Registro con {id_columna}={id_valor} actualizado correctamente"

def hacer_respaldo(ruta_excel: str):
    if not os.path.exists(ruta_excel):
        return 

    ultima_mod = datetime.fromtimestamp(os.path.getmtime(ruta_excel))
    ahora = datetime.now()

    if (ahora - ultima_mod) >= timedelta(days=1):
        nombre_archivo = os.path.basename(ruta_excel)
        nombre_base, ext = os.path.splitext(nombre_archivo)
        timestamp = ahora.strftime("%Y-%m-%d_%H-%M-%S")
        nombre_respaldo = f"{nombre_base}_BACKUP_{timestamp}{ext}"
        ruta_respaldo = os.path.join(os.path.dirname(ruta_excel), nombre_respaldo)

        shutil.copy2(ruta_excel, ruta_respaldo)
        print(f"Respaldo creado: {ruta_respaldo}")

def obtener_dataset(ruta_excel: str) -> pd.DataFrame:
    if not os.path.exists(ruta_excel):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta_excel}")

    df = pd.read_excel(ruta_excel)
    return df