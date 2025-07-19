import joblib
import numpy as np
import spacy
from sentence_transformers import SentenceTransformer
import threading
from fastapi import HTTPException
from openai import OpenAI
from app.common.settings import GEMINI_API_KEY, GEMINI_BASE_URL
from sklearn.metrics.pairwise import cosine_similarity

modelo_categoria = None
nlp = None
model_st = None
reg = None
keyword_embeddings = None
all_keywords = None

def get_modelo_categoria():
    global modelo_categoria
    if modelo_categoria is None:
        print("[LOAD] Cargando modelo de categoría...")
        modelo_categoria = joblib.load("app/models/category_text/modelo_entrenado.joblib")
    return modelo_categoria

def get_nlp():
    global nlp
    if nlp is None:
        print("[LOAD] Cargando modelo Spacy...")
        nlp = spacy.load("en_core_web_md")
    return nlp

def get_model_st():
    global model_st
    if model_st is None:
        print("[LOAD] Cargando modelo SentenceTransformer...")
        model_st = SentenceTransformer("all-MiniLM-L6-v2")
    return model_st

def get_regressor():
    global reg
    if reg is None:
        print("[LOAD] Cargando regresor...")
        reg = joblib.load("app/models/regressor_model/regressor_model.pkl")
    return reg

def get_embeddings():
    global keyword_embeddings
    if keyword_embeddings is None:
        print("[LOAD] Cargando embeddings...")
        keyword_embeddings = np.load("app/models/regressor_model/keyword_embeddings.npy")
    return keyword_embeddings

def get_keywords():
    global all_keywords
    if all_keywords is None:
        print("[LOAD] Cargando lista de keywords...")
        all_keywords = joblib.load("app/models/regressor_model/all_keywords.pkl")
    return all_keywords

def precargar_modelos():
    print("[INIT] Precargando modelos en segundo plano...")
    try:
        get_modelo_categoria()
        get_nlp()
        get_model_st()
        get_regressor()
        get_embeddings()
        get_keywords()
        print("[INIT] Modelos cargados en background.")
    except Exception as e:
        print(f"[INIT] Error al precargar modelos: {e}")

import threading
import traceback

def lanzar_carga_en_background():
    def _wrapper():
        try:
            print("[INIT] Cargando modelos de lenguaje...")
            precargar_modelos()
            print("[INIT] Modelos de lenguaje cargados.")
        except Exception as e:
            print(f"[ERROR] en precargar_modelos: {e}")
            traceback.print_exc()

    hilo = threading.Thread(target=_wrapper, name="PrecargaModelos", daemon=True)
    hilo.start()

def traducir_texto(texto, destino="en"):
    try:
        if not GEMINI_API_KEY:
            raise HTTPException(status_code=500, detail="Gemini API key no configurada")
        
        client = OpenAI(api_key=GEMINI_API_KEY, base_url=GEMINI_BASE_URL)
        idioma_destino = "English" if destino == "en" else "Spanish"
        
        prompt = f"Translate the following text to {idioma_destino}. Only return the translation, nothing else:\n\n{texto}"
        
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": "You are a professional translator. Translate accurately and return only the translation."},
                {"role": "user", "content": prompt}
            ],
            stream=False,
            max_tokens=500
        )
        
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error en traducción: {str(e)}")
        return texto

def extraer_conceptos(texto, usar_lemma=True):
    doc = get_nlp()(texto)
    return " ".join(
        (token.lemma_ if usar_lemma else token.text).lower()
        for token in doc
        if token.pos_ in ["NOUN", "ADJ", "PROPN"] and not token.is_stop
    )

def validar_conceptos(conceptos):
    if not conceptos.strip():
        raise HTTPException(status_code=400, detail="No se encontraron conceptos relevantes en el texto.")

def traducir_lista(lista_textos, destino="es"):
    return [traducir_texto(t, destino) for t in lista_textos]

def obtener_conceptos_desde_texto(texto: str, usar_lemma: bool = False) -> list[str]:
    texto_en = traducir_texto(texto, destino="en")
    conceptos = extraer_conceptos(texto_en, usar_lemma=usar_lemma)
    validar_conceptos(conceptos)
    return conceptos

def predecir_categoria(conceptos: list[str]) -> dict:
    categoria_en = get_modelo_categoria().predict([conceptos])[0]
    categoria_es = traducir_texto(categoria_en, destino="es")
    return {
        "categoria_predicha_en": categoria_en,
        "categoria_predicha_es": categoria_es
    }

def predecir_keywords(conceptos: list[str]) -> dict:
    x_new = get_model_st().encode(conceptos).reshape(1, -1)
    y_pred = get_regressor().predict(x_new)
    sims = cosine_similarity(y_pred, get_embeddings()).flatten()
    indices = sims.argsort()[::-1][:10]
    keywords_en = [get_keywords()[i] for i in indices]
    keywords_es = traducir_lista(keywords_en, destino="es")
    return {
        "keywords_predichas_en": keywords_en,
        "keywords_predichas_es": keywords_es
    }
