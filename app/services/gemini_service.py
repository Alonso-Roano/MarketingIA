# app/services/gemini_service.py

from app.services.extract_service import extract_text_from_pdf
from app.common.utils import enviar_mensaje_a_gemini
import json
import re

VALID_SIZES = ["Muy pequeña", "Pequeña", "Mediana", "Grande", "Muy grande", "Nivel Empresarial"]
VALID_SCOPES = ["Local", "Regional", "Nacional", "Global"]
VALID_INDUSTRIES = ["Retail", "Tecnología", "Salud", "Educación", "Finanzas", "Turismo"]
VALID_ICONS = [
    "pi pi-chart-line", "pi pi-users", "pi pi-bolt", "pi pi-globe", "pi pi-dollar", "pi pi-calendar",
    "pi pi-envelope", "pi pi-video", "pi pi-chart-bar", "pi pi-tags", "pi pi-bell", "pi pi-shopping-cart",
    "pi pi-share-alt", "pi pi-thumbs-up", "pi pi-star", "pi pi-mobile", "pi pi-desktop", "pi pi-clock",
    "pi pi-search", "pi pi-cog", "pi pi-eye", "pi pi-heart", "pi pi-camera", "pi pi-upload", "pi pi-download",
    "pi pi-lock", "pi pi-unlock", "pi pi-map-marker", "pi pi-check", "pi pi-times", "pi pi-cloud",
    "pi pi-sitemap", "pi pi-comments", "pi pi-briefcase", "pi pi-credit-card", "pi pi-wifi", "pi pi-moon",
    "pi pi-sun", "pi pi-database", "pi pi-question-circle", "pi pi-info-circle", "pi pi-exclamation-triangle",
    "pi pi-power-off", "pi pi-replay", "pi pi-angle-double-right", "pi pi-angle-double-left", "pi pi-book",
    "pi pi-pencil", "pi pi-trash", "pi pi-file", "pi pi-image", "pi pi-volume-up", "pi pi-microphone"
]

VALID_COLORS = [
    "#00BFFF", "#00CED1", "#00FA9A", "#00FF00", "#00FFFF", "#20B2AA", "#39FF14", "#40E0D0", "#7CFC00", "#7DF9FF",
    "#8A2BE2", "#98FB98", "#ADFF2F", "#B0FC38", "#BA55D3", "#DFFF00", "#DA70D6", "#DC143C", "#E0FFFF", "#EE82EE",
    "#FF00FF", "#FF1493", "#FF3131", "#FF4500", "#FF6347", "#FF69B4", "#FF6EC7", "#FF8C00", "#FFB6C1", "#FFD700",
    "#FFE135", "#FFFF00"
]

def validate_or_null(value: str, valid_list: list[str]) -> str | None:
    return value if value in valid_list else None

def extract_hex_color(text: str) -> str | None:
    match = re.search(r"#([A-Fa-f0-9]{6})", text)
    if match:
        hex_code = f"#{match.group(1).upper()}"
        return hex_code if hex_code in VALID_COLORS else None
    return None

def generate_campaign_from_pdf(upload_file) -> dict:
    try:
        upload_file.file.seek(0)
        texto = extract_text_from_pdf(upload_file)

        prompt = f"""
Eres un experto en branding y marketing. A partir del siguiente texto de una empresa, genera un JSON con esta estructura para autocompletar un formulario:

{{
  "nombre": "Nombre corto de la campaña de Marketing de la empresa o marca",
  "icono": "Elige uno de estos valores exactos: {', '.join(VALID_ICONS)}",
  "primary_color": "color en formato #HEX, elige uno de: {', '.join(VALID_COLORS)}",
  "description": "Breve descripción de la campaña de marketing del negocio, productos o servicios",
  "size": "elige uno de: {', '.join(VALID_SIZES)}",
  "scope": "elige uno de: {', '.join(VALID_SCOPES)}",
  "industry": "elige uno de: {', '.join(VALID_INDUSTRIES)}"
}}

Texto del documento:
\"\"\"
{texto[:3000]}
\"\"\"
"""

        respuesta = enviar_mensaje_a_gemini(
            system_message="Eres un experto en marketing y análisis de empresas.",
            user_message=prompt
        )

        # Extraer JSON desde markdown si viene como ```json ... ```
        json_text = respuesta.strip()
        if "```json" in json_text:
            json_text = json_text.split("```json")[1].split("```")[0].strip()

        data = json.loads(json_text)

        return {
            "nombre": data.get("nombre", "").strip(),
            "icono": validate_or_null(data.get("icono", "").strip(), VALID_ICONS),
            "primary_color": extract_hex_color(data.get("primary_color", "")),
            "description": data.get("description", "").strip(),
            "size": validate_or_null(data.get("size", ""), VALID_SIZES),
            "scope": validate_or_null(data.get("scope", ""), VALID_SCOPES),
            "industry": validate_or_null(data.get("industry", ""), VALID_INDUSTRIES),
        }

    except Exception as e:
        raise RuntimeError(f"Error procesando PDF: {str(e)}")
