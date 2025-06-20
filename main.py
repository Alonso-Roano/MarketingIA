from fastapi import FastAPI
from app.routers import (pokemon, modelos)

app = FastAPI(
    title="API de Modelos IA",
    description="Predicciones múltiples usando FastAPI",
    version="1.0"
)

app.include_router(pokemon, prefix="/pokemon", tags=["Modelo Pokémon"])
app.include_router(modelos, prefix="/modelos", tags=["Modelos"])