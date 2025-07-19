import time
from contextlib import contextmanager
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.services.language_service import lanzar_carga_en_background
from contextlib import asynccontextmanager
from app.services.language_service import lanzar_carga_en_background
import threading
from app.services.registry_model import cargar_modelos

load_dotenv()

@contextmanager
def profile_block(label):
    start = time.time()
    yield
    duration = time.time() - start
    print(f"[PROFILE] {label} tomó {duration:.3f}s")

global_start = time.time()
print("[PROFILE] Iniciando aplicación...")

app = FastAPI(
    title="API de modelos de Marketig",
    description="Predicciones de múltiples datos de marketing usando FastAPI",
    version="1.0"
)

@app.on_event("startup")
async def startup_event():
    with profile_block("Cargando modelos de lenguaje"):
        lanzar_carga_en_background()

    with profile_block("Cargando modelos de ia"):
        cargar_modelos()

with profile_block("Importar dataset_router"):
    from app.routers import dataset_router
    app.include_router(dataset_router.router, tags=["Datasets"])

with profile_block("Importar laguage_router"):
    from app.routers import laguage_router
    app.include_router(laguage_router.router, tags=["Language"], include_in_schema=False)

with profile_block("Importar ai21_router"):
    from app.routers import ai21_router
    app.include_router(ai21_router.router, tags=["AI21"], include_in_schema=False)

with profile_block("Importar minios_router"):
    from app.routers import minios_router
    app.include_router(minios_router.router, tags=["Minios"])

with profile_block("Importar gemini_router"):
    from app.routers import gemini_router
    app.include_router(gemini_router.router, tags=["Gemini"])

with profile_block("Importar model_router"):
    from app.routers import model_router
    app.include_router(model_router.router, tags=["Peticion a modelos"], include_in_schema=False)

with profile_block("Importar omni_router"):
    from app.routers import omni_router
    app.include_router(omni_router.router, tags=["Peticion unitaria"])

# === OpenAPI personalizado ===
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    with profile_block("Generar esquema OpenAPI"):
        openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        openapi_schema["components"]["securitySchemes"] = {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }

        for path in openapi_schema["paths"].values():
            for method in path.values():
                if "parameters" not in method:
                    method["parameters"] = []
                method["parameters"].append({
                    "name": "refresh-token",
                    "in": "header",
                    "required": True,
                    "schema": {
                        "type": "string"
                    },
                    "description": "El token de refresco (refresh token) del usuario"
                })
                method["security"] = [{"BearerAuth": []}]

        app.openapi_schema = openapi_schema
        return app.openapi_schema

app.openapi = custom_openapi

# === Middleware CORS ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(f"[PROFILE] Aplicación lista en {time.time() - global_start:.2f}s")