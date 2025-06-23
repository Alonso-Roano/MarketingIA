from pydantic import BaseModel, model_validator
from typing import Optional
from typing import List

class PokemonData(BaseModel):
    species_id: Optional[int] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    base_experience: Optional[int] = None
    order: Optional[int] = None

    @model_validator(mode='after')
    def al_menos_uno_requerido(cls, values):
        if all(
            getattr(values, field) is None
            for field in ['species_id', 'height', 'weight', 'base_experience', 'order']
        ):
            raise ValueError("Se requiere al menos un campo con valor")
        return values

class PokemonUpdateData(BaseModel):
    id: Optional[int] = None
    identifier: Optional[str] = None
    species_id: Optional[int] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    base_experience: Optional[int] = None
    order: Optional[int] = None
    is_default: Optional[bool] = None

class PokemonDataRequest(BaseModel):
    id: int
    identifier: str
    species_id: int
    height: int
    weight: int
    base_experience: int
    order: int
    is_default: bool

class InsertarDatosPokemonRequest(BaseModel):
    datos: List[PokemonDataRequest]