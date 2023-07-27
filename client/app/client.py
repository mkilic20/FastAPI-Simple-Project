from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()


@app.post("/send-movie/")  # Changed from @app.get to @app.post
async def send_movie():
    movie_data = {
        "id": 15,
        "name": "New Movie",
        "release_year": 2023
    }
    try:
        response = requests.post("http://db-service:8001/add-movie/", json=movie_data)
        response.raise_for_status()  # Raise an HTTPError if one occurred
    except requests.exceptions.RequestException as err:
        raise HTTPException(status_code=500, detail=str(err))
    return response.json()
