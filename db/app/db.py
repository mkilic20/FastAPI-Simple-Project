import json
from typing import List

from fastapi import FastAPI, Depends
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from pydantic import BaseModel

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    release_year = Column(Integer)


class MovieIn(BaseModel):
    id: int
    name: str
    release_year: int


class MovieOut(BaseModel):
    id: int
    name: str
    release_year: int

    class Config:
        orm_mode = True


app = FastAPI()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup_event():
    # read json data and insert into table at startup
    db = SessionLocal()
    with open('movies.json', 'r') as f:
        data = json.load(f)
    for item in data:
        if db.query(Movie).filter(Movie.id == item["id"]).first() is None:
            movie = Movie(**item)
            db.add(movie)
            db.commit()


@app.get("/")
async def welcome():
    return {"message": "Hello DB"}


@app.get("/movies/", response_model=List[MovieOut])
def read_movies(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    movies = db.query(Movie).offset(skip).limit(limit).all()
    return movies


@app.post("/movies/")
def create_movie(movie: MovieIn, db: Session = Depends(get_db)):
    db_movie = Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie
