
from fastapi import FastAPI, HTTPException, Depends, Response
from pymongo.database import Database

from db import get_db
from schemas import MovieResponse, MovieDB
from db_client import (
    get_all_movies,
    get_movie,
    add_movie,
    delete_movie,
    update_movie
)

app = FastAPI()


# Получить все фильмы
@app.get("/", response_model=list[MovieDB])
def get_all_movies_endpoint(db: Database = Depends(get_db)):
    return get_all_movies(db)


# Получить фильм по ID
@app.get("/{movie_id}", response_model=MovieDB)
def get_movie_endpoint(movie_id: int, db: Database = Depends(get_db)):
    movie = get_movie(movie_id, db)

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    return movie


# Добавить фильм
@app.post("/", status_code=201, response_model=MovieDB)
def add_movie_endpoint(
    payload: MovieResponse,
    db: Database = Depends(get_db)
):
    return add_movie(payload, db)


# Удалить фильм
@app.delete("/{movie_id}", status_code=204)
def delete_movie_endpoint(movie_id: int, db: Database = Depends(get_db)):
    if not delete_movie(movie_id, db):
        raise HTTPException(status_code=404, detail="Movie not found")

    return Response(status_code=204)


# Обновить фильм
@app.put("/{movie_id}", response_model=MovieDB)
def update_movie_endpoint(
    movie_id: int,
    payload: MovieResponse,
    db: Database = Depends(get_db)
):
    movie = update_movie(movie_id, payload, db)

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")

    return movie
