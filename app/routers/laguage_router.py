from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.common.middleware import verificar_acceso
from app.common.settings import GEMINI_API_KEY, GEMINI_BASE_URL
import spacy
import joblib
import numpy as np
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

router = APIRouter(prefix="/language")

modelo_categoria = joblib.load("app/models/category_text/modelo_entrenado.joblib")
nlp = spacy.load("en_core_web_md")

model_st = SentenceTransformer("all-MiniLM-L6-v2")
reg = joblib.load("app/models/regressor_model/regressor_model.pkl")
keyword_embeddings = np.load("app/models/regressor_model/keyword_embeddings.npy")
all_keywords = joblib.load("app/models/regressor_model/all_keywords.pkl")

class TextoEntrada(BaseModel):
    descripcion: str

def traducir_texto(texto, destino="en"):
    """Traduce texto usando Gemini API"""
    try:
        if not GEMINI_API_KEY:
            raise HTTPException(
                status_code=500,
                detail="Gemini API key no configurada"
            )
        
        client = OpenAI(
            api_key=GEMINI_API_KEY,
            base_url=GEMINI_BASE_URL
        )
        
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
    doc = nlp(texto)
    return " ".join(
        (token.lemma_ if usar_lemma else token.text).lower()
        for token in doc
        if token.pos_ in ["NOUN", "ADJ", "PROPN"] and not token.is_stop
    )

def validar_conceptos(conceptos):
    if not conceptos.strip():
        raise HTTPException(
            status_code=400,
            detail="No se encontraron conceptos relevantes en el texto."
        )

def traducir_lista(lista_textos, destino="es"):
    return [traducir_texto(t, destino) for t in lista_textos]

@router.post("/predecir/rubro")
def predecir_categoria_api(
    entrada: TextoEntrada,
    _: None = Depends(verificar_acceso)
):
    texto_en = traducir_texto(entrada.descripcion, destino="en")

    conceptos = extraer_conceptos(texto_en, usar_lemma=False)
    validar_conceptos(conceptos)

    categoria_predicha = modelo_categoria.predict([conceptos])[0]

    categoria_predicha_es = traducir_texto(categoria_predicha, destino="es")

    return {
        "categoria_predicha_en": categoria_predicha,
        "categoria_predicha_es": categoria_predicha_es
    }

@router.post("/predecir/keywords")
def predecir_keywords_api(
    entrada: TextoEntrada,
    _: None = Depends(verificar_acceso)
):
    texto_en = traducir_texto(entrada.descripcion, destino="en")

    conceptos = extraer_conceptos(texto_en, usar_lemma=True)
    validar_conceptos(conceptos)

    x_new = model_st.encode(conceptos).reshape(1, -1)

    y_pred = reg.predict(x_new)

    sims = cosine_similarity(y_pred, keyword_embeddings).flatten()
    indices = sims.argsort()[::-1][:10]

    predicted_keywords_en = [all_keywords[i] for i in indices]
    predicted_keywords_es = traducir_lista(predicted_keywords_en, destino="es")

    return {
        "keywords_predichas_en": predicted_keywords_en,
        "keywords_predichas_es": predicted_keywords_es
    }
