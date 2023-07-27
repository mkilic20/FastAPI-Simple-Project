import requests
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Movie(BaseModel):
    id: int
    name: str
    release_year: int


@app.post("/add-movie/")
async def add_movie(movie: Movie):
    existing_movies = requests.get("http://db:8000/movies/").json()
    if movie.id not in [m["id"] for m in existing_movies]:
        response = requests.post("http://db:8000/movies/", json=movie.dict())
        return response.json()
    else:
        return {"status": "Movie already exists"}
