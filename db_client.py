
from pymongo import ReturnDocument

# получить коллекции фильмов и счетчиков
def collections(db):
    return db["movies"], db["counters"]

# преобразовать документ фильма в словарь без поля "_id"
def serialize(movie):
    if movie is None:
        return None

    movie.pop("_id", None)
    return movie

# Получить все фильмы
def get_all_movies(db):
    movies, _ = collections(db)
    return [serialize(movie) for movie in movies.find({}).sort("id", 1)]

# Получить фильм по ID
def get_movie(movie_id: int, db):
    movies, _ = collections(db)
    return serialize(movies.find_one({"id": movie_id}))

# Добавить фильм
def add_movie(payload, db):
    movies, counters = collections(db)

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
    movies, _ = collections(db)

    result = movies.delete_one({"id": movie_id})

    return result.deleted_count > 0

# Обновить фильм
def update_movie(movie_id: int, payload, db):
    movies, _ = collections(db)

    movie = movies.find_one_and_update(
        {"id": movie_id},
        {"$set": payload.model_dump()},
        return_document=ReturnDocument.AFTER
    )

    return serialize(movie)
