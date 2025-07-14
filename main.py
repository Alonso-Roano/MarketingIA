from fastapi import FastAPI, APIRouter, Depends
from fastapi.openapi.utils import get_openapi
from app.services.registry_model import MODEL_REGISTRY
from app.routers import dataset_router, model_router, laguage_router, ai21_router, minios_router, gemini_router
from app.common.middleware import verificar_acceso
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="API de modelos de Marketig",
    description="Predicciones de múltiples datos de marketing usando FastAPI",
    version="1.0"
)

# Ruta para modificar el dataset y los modelos
app.include_router(dataset_router.router, tags=["Datasets"])

app.include_router(laguage_router.router, tags=["Language"])

app.include_router(ai21_router.router, tags=["AI21"])

app.include_router(minios_router.router, tags=["Minios"])

app.include_router(gemini_router.router, tags=["Gemini"])

# Mapear todos los modelos de IA, actualmente esta oculta en el swagger
app.include_router(model_router.router, tags=["Peticion a modelos"], include_in_schema=False)

# Esto es solo para mostrar las rutas en el Swagger, borrar al subir a produccion
for modelo_name, entry in MODEL_REGISTRY.items():
    router = APIRouter(prefix=f"/modelo/{modelo_name}", tags=[modelo_name])
    
    schema = entry["schema"]
    service = entry["service"]

    @router.post("/predict")
    def predict(data: schema, _: None = Depends(verificar_acceso)):
        return service.predecir(data.dict())

    @router.get("/info")
    def info(_: None = Depends(verificar_acceso)):
        return service.obtener_info()

    @router.get("/metricas")
    def metricas(_: None = Depends(verificar_acceso)):
        return service.obtener_metricas()

    app.include_router(router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
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
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)