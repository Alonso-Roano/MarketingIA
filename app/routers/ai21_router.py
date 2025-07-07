from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import List, Optional
import re
from app.common.settings import AI21_API_URL, AI21_API_TOKEN_1, AI21_API_TOKEN_2, AI21_API_TOKEN_3
import requests
import json
import random

API_KEYS = [
    AI21_API_TOKEN_1,
    AI21_API_TOKEN_2,
    AI21_API_TOKEN_3
]

API_URL = AI21_API_URL
MODEL_NAME = "jamba-mini"

router = APIRouter(prefix="/ai21")

class EmpresaRequest(BaseModel):
    descripcion: str
    rubro: Optional[str] = ""
    tamano: str
    alcance: str
    palabras_clave: Optional[List[str]] = []

class MisionVisionResponse(BaseModel):
    mision: str
    vision: str

def get_api_key():
    return random.choice(API_KEYS)

def limpiar_texto(texto):
    texto = re.sub(r"[*]+", "", texto)
    texto = texto.strip()
    return texto

def construir_prompt(descripcion, rubro, tamano, alcance, palabras_clave):
    prompt = (
        "Eres un experto en redacción corporativa. "
        "Genera la Misión y Visión para una empresa en español. "
        "IMPORTANTE:\n"
        "- Prioriza la descripción, tamaño y alcance de la empresa.\n"
        "- El rubro y las palabras clave son solo referencia secundaria.\n"
        "- Sé conciso y evita textos muy largos.\n\n"
        f"Descripción: {descripcion}\n"
        f"Tamaño: {tamano}\n"
        f"Alcance: {alcance}\n"
        f"Rubro (guía): {rubro}\n"
        f"Palabras clave (guía): {', '.join(palabras_clave)}\n\n"
        "Genera la respuesta en este formato exacto:\n"
        "Misión: <texto de la misión>\n"
        "Visión: <texto de la visión>\n"
    )
    return prompt

@router.post("/generar-mision-vision", response_model=MisionVisionResponse)
def generar_mision_vision(request: EmpresaRequest):
    prompt = construir_prompt(
        request.descripcion,
        request.rubro,
        request.tamano,
        request.alcance,
        request.palabras_clave
    )

    api_key = get_api_key()

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": MODEL_NAME,
        "max_tokens": 300,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            data = response.json()
            texto = data['choices'][0]['message']['content'].strip()

            mision = ""
            vision = ""

            if "Misión:" in texto and "Visión:" in texto:
                partes = texto.split("Visión:")
                mision = limpiar_texto(partes[0].replace("Misión:", ""))
                vision = limpiar_texto(partes[1])
            else:
                mision = texto
                vision = ""

            return MisionVisionResponse(mision=mision, vision=vision)

        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"AI21 API error: {response.text}"
            )

    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=500,
            detail=f"Request error: {e}"
        )
