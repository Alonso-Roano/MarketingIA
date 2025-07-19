from app.services.registry_model import MODEL_REGISTRY
from app.common.utils import crear_payloads_por_modelo
import json
from app.common.utils import enviar_mensaje_a_gemini
from app.services.apiRequest import api_request

def ejecutar_todo(payload_maestro: dict) -> dict:
    resultados = {}

    modelos_ordenados = ["marketing_media_cost", "marketing_impressions", "marketing_clicks"]

    for modelo in modelos_ordenados:
        config = MODEL_REGISTRY.get(modelo)
        if not config:
            resultados[modelo] = {"prediccion": f"Modelo {modelo} no encontrado en registro"}
            continue

        # Crear payload para este modelo usando el payload maestro actualizado
        payloads = crear_payloads_por_modelo(payload_maestro, registry={modelo: config})
        datos_modelo = payloads[modelo]
        faltantes = datos_modelo["faltantes"]

        if faltantes:
            resultados[modelo] = {
                "prediccion": {
                    "error": f"Faltan campos en el payload maestro para {modelo}",
                    "faltantes": faltantes
                }
            }
            # No actualizar payload maestro si faltan campos
            continue

        try:
            data = config["schema"](**datos_modelo["payload"])

            prediccion = config["service"].predecir(data.dict())
            resultados[modelo] = prediccion

            # Desempaquetar el valor antes de usarlo como entrada para otros modelos
            valor_predicho = prediccion.get("prediccion")

            if modelo == "marketing_media_cost":
                payload_maestro["media_cost_usd"] = valor_predicho
            elif modelo == "impresiones":
                payload_maestro["impresiones"] = valor_predicho
            elif modelo == "clicks":
                payload_maestro["clicks"] = valor_predicho

        except Exception as e:
            resultados[modelo] = {"prediccion": f"Error en predicción {modelo}: {e}"}

    # Ahora ejecuta el resto de modelos que no están en esa lista
    for modelo, config in MODEL_REGISTRY.items():
        if modelo in modelos_ordenados:
            continue

        payloads = crear_payloads_por_modelo(payload_maestro, registry={modelo: config})
        datos_modelo = payloads[modelo]
        faltantes = datos_modelo["faltantes"]

        if faltantes:
            resultados[modelo] = {
                "prediccion": {
                    "error": "Faltan campos en el payload maestro",
                    "faltantes": faltantes
                }
            }
            continue

        try:
            data = config["schema"](**datos_modelo["payload"])
            resultados[modelo] = config["service"].predecir(data.dict())
        except Exception as e:
            resultados[modelo] = {"prediccion": f"Error en predicción: {e}"}

    return resultados

def interpretar_predicciones_en_contexto(predicciones: dict, descripcion: str, mision_vision:str) -> dict:
    system_message = (
        "Eres un analista experto en marketing digital. "
        "Tienes un conjunto de variables predichas para una campaña, y debes generar para cada variable una interpretación"
        "basada en el contexto completo de la campaña. La interpretacion debe de ser del lado del sistema, dirigida al usuario, y debe ser dicha como una recomendacion\n\n"
        "Tu respuesta **debe ser exclusivamente un JSON válido** con esta estructura exacta:\n"
        "{\n"
        "  \"variable1\": {\n"
        "    \"prediccion\": valor_original,\n"
        "    \"interpretacion\": \"explicación breve y clara, en una sola línea\"\n"
        "  },\n"
        "  \"variable2\": {\n"
        "    \"prediccion\": valor_original,\n"
        "    \"interpretacion\": \"explicación breve y clara, en una sola línea\"\n"
        "  },\n"
        "  ...\n"
        "}\n\n"
        "No agregues texto fuera del JSON. No uses comillas triples ni markdown. No agregues explicaciones adicionales."
    )

    user_message = (
        f"Contexto de campaña:\n{descripcion}\n\n"
        f"Mision y vision para mas contexto:\n{mision_vision}\n\n"
        f"Predicciones de campaña:\n{json.dumps(predicciones, indent=2)}"
    )

    respuesta = enviar_mensaje_a_gemini(system_message, user_message)

    try:
        return json.loads(respuesta)
    except json.JSONDecodeError:
        raise ValueError(f"La respuesta de Gemini no es un JSON válido:\n{respuesta}")
    
def interpretar_fake(predicciones: dict, descripcion: str, mision_vision: str) -> dict:
    # Esto no se usa por ahora, solo lo dejamos para mantener el diseño
    system_message = (
        "Eres un analista experto en marketing digital. ..."
    )
    user_message = (
        f"Contexto de campaña:\n{descripcion}\n\n"
        f"Misión y visión:\n{mision_vision}\n\n"
        f"Predicciones:\n{json.dumps(predicciones, indent=2)}"
    )

    respuesta_fake = {
        variable: {
            "prediccion": valor,
            "interpretacion": "Interpretación simulada para pruebas"
        }
        for variable, valor in predicciones.items()
    }

    return respuesta_fake

def armar_contexto_interpretacion(
    predicciones: dict,
    keywords: dict
) -> dict:
    return {
        "keywords_predichas": keywords["keywords_predichas_es"],
        **predicciones
    }

def crear_proyecto(
    nombre: str,
    icono: str,
    primary_color: str,
    access_token: str,
    refresh_token: str
):
    body = {
        "nombre": nombre,
        "icono": icono,
        "primary_color": primary_color
    }

    result, new_token = api_request(
        key="project.crear",
        access_token=access_token,
        refresh_token=refresh_token,
        data=body
    )

    return result, new_token

def crear_project_data(
    access_token: str,
    refresh_token: str,
    body: dict
) -> dict:
    result, new_token = api_request(
        key="projectData.crear",
        access_token=access_token,
        refresh_token=refresh_token,
        data=body
    )

    return result, new_token

def crear_project_prediction(
    access_token: str,
    refresh_token: str,
    body: dict
) -> dict:
    result, new_token = api_request(
        key="projectPrediction.crear",
        access_token=access_token,
        refresh_token=refresh_token,
        data=body
    )

    return result, new_token
