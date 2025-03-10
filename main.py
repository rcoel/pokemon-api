import pandas as pd
import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Pokemon(BaseModel):
    Name: str
    class Config:
        extra = "allow"

pokemons = []
df = pd.read_csv("data/Pokemon.csv")
pokemons_data = df.to_dict(orient="records")
pokemons = [Pokemon(**data) for data in pokemons_data]

@app.get("/")
async def root():
    return {"message": "Pokémon API. Visit /docs for endpoints."}

@app.get("/pokemon", response_model=Pokemon)
def get_random_pokemon():
    """Return a random Pokemon from the dataset."""
    if not pokemons:
        raise HTTPException(status_code=404, detail="No Pokemon available")
    random_pokemon = random.choice(pokemons)
    return random_pokemon

@app.get("/pokemon/{name}", response_model=Pokemon)
def get_pokemon_by_name(name: str):
    """Return a Pokemon matching the provided name (case-insensitive)."""
    for pokemon in pokemons:
        if pokemon.Name.lower() == name.lower():
            return pokemon
    raise HTTPException(status_code=404, detail="Pokemon not found")

