from app.schemas.landingPage_schema import REGLAS_URLS_TEMPLATE
from app.common.utils import enviar_mensaje_a_gemini
from pydantic import BaseModel
from deepdiff import DeepDiff
import json
import re


def generar_landing_con_gemini(contexto_empresa: str, esquema: type[BaseModel], imagenes: dict[str, str]) -> dict:
    import json
    from json import loads

    imagenes_json = json.dumps(imagenes, indent=2)

    prompt = f"""
                Eres un generador de contenido para landing pages en formato JSON.

                Contexto de la empresa:
                {contexto_empresa}

                Estas son las imágenes disponibles, con claves que indican su propósito:
                {imagenes_json}

                - Usa exclusivamente estas imágenes donde correspondan.
                - No inventes URLs.
                - Si una clave es "hero_background", va en hero.backgroundImage.
                - "feature_0_icon" va en features.items[0].icon, etc.
                - Usa todas las imágenes donde corresponda.
                - Si tienes que usar iconos usa Primeicons de vue y escribelo como se inserta en html, osea como una clase de etiqueta i, pero solo la clase no la etiqueta completa.
                - si el template tiene un theme trata de adaptar los colores con la empresa, por ejemplo, las que trabajan con plantas resalta el verde y asi con las otras.

                Genera un JSON que cumpla con este esquema y no dejes ningun valor en null:
                {esquema.model_json_schema()}

                No expliques nada. Devuelve solo el JSON.
                """

    try:
        respuesta_raw = enviar_mensaje_a_gemini(
            system_message="Eres un generador de landing pages en JSON válido.",
            user_message=prompt
        )
        json_generado = extraer_json_de_gemini(respuesta_raw)
        data = json_generado
        return esquema.model_validate(data).model_dump()
    except Exception as e:
        raise RuntimeError(f"Error generando landing: {e}")


def validar_imagenes_input(template_id: str, imagenes: dict[str, str]):
    requeridas = REGLAS_URLS_TEMPLATE.get(template_id)
    if requeridas is None:
        raise ValueError(f"No hay reglas de imágenes para el template '{template_id}'")

    faltantes = [k for k in requeridas if k not in imagenes]
    if faltantes:
        raise ValueError(f"Faltan imágenes requeridas para '{template_id}': {faltantes}")

def verificar_uso_de_imagenes(json_generado: dict, imagenes: dict[str, str]) -> list[str]:
    usados = json.dumps(json_generado)
    faltantes = [k for k, url in imagenes.items() if url not in usados]
    return faltantes

from typing import Type
from pydantic import BaseModel

def validar_estructura_exacta(json_generado: dict, esquema: Type[BaseModel]):
    """
    Verifica que el json generado tenga la misma estructura de claves que el esquema.
    Lanza error si hay campos faltantes o adicionales.
    """

    def crear_objeto_simulado(cls):
        ejemplo = cls.model_construct(
            **{
                k: crear_objeto_simulado(v.annotation)
                if isinstance(v.annotation, type) and issubclass(v.annotation, BaseModel)
                else [] if v.annotation == list else ""
                for k, v in cls.model_fields.items()
            }
        )
        return ejemplo

    esperado = crear_objeto_simulado(esquema).model_dump()
    generado = json_generado

    diff = DeepDiff(esperado, generado, ignore_order=True, report_repetition=True, view='tree')

    if diff.get('dictionary_item_added') or diff.get('dictionary_item_removed'):
        raise ValueError(f"Estructura incorrecta:\n{diff.pretty()}")
    
def extraer_json_de_gemini(texto: str):
    match = re.search(r"```json\s*(\{.*?\})\s*```", texto, re.DOTALL)
    if not match:
        raise ValueError("No se encontró un bloque JSON válido en la respuesta.")
    return json.loads(match.group(1))