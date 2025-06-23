from fastapi import FastAPI, APIRouter
from app.services.registry_model import MODEL_REGISTRY
from app.routers import dataset_router, model_router

app = FastAPI(
    title="API de Modelos IA",
    description="Predicciones múltiples usando FastAPI",
    version="1.0"
)

# Ruta para modificar el dataset y los modelos
app.include_router(dataset_router.router, tags=["Datasets"])

# Mapear todos los modelos de IA, actualmente esta oculta en el swagger
app.include_router(model_router.router, tags=["Peticion a modelos"], include_in_schema=False)

# Esto es solo para mostrar las rutas en el Swagger, borrar al subir a produccion
for modelo_name, entry in MODEL_REGISTRY.items():
    router = APIRouter(prefix=f"/modelo/{modelo_name}", tags=[modelo_name])
    
    schema = entry["schema"]
    service = entry["service"]

    @router.post("/predict")
    def predict(data: schema):
        return service.predecir(data.dict())

    @router.get("/info")
    def info():
        return service.obtener_info()

    @router.get("/metricas")
    def metricas():
        return service.obtener_metricas()

    app.include_router(router)