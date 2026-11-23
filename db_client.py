
from pymongo import ReturnDocument


def _collections(db):
    return db["movies"], db["counters"]


def _serialize(movie):
    if movie is None:
        return None

    movie.pop("_id", None)
    return movie


# Получить все фильмы
def get_all_movies(db):
    movies, _ = _collections(db)
    return [_serialize(movie) for movie in movies.find({}).sort("id", 1)]


# Получить фильм по ID
def get_movie(movie_id: int, db):
    movies, _ = _collections(db)
    return _serialize(movies.find_one({"id": movie_id}))


# Добавить фильм
def add_movie(payload, db):
    movies, counters = _collections(db)

    counter = counters.find_one_and_update(
        {"_id": "movie_id"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )

    movie = payload.model_dump()
    movie["id"] = counter["seq"]

    movies.insert_one(movie)

    return movie


# Удалить фильм
def delete_movie(movie_id: int, db):
    movies, _ = _collections(db)

    result = movies.delete_one({"id": movie_id})

    return result.deleted_count > 0


# Обновить фильм
def update_movie(movie_id: int, payload, db):
    movies, _ = _collections(db)

    movie = movies.find_one_and_update(
        {"id": movie_id},
        {"$set": payload.model_dump()},
        return_document=ReturnDocument.AFTER
    )

    return _serialize(movie)
