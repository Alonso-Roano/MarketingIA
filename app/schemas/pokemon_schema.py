from pydantic import BaseModel

class PokemonData(BaseModel):
    species_id: int
    height: int
    weight: int
    base_experience: int
    order: int
