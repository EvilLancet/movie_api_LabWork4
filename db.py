import os
from pymongo import MongoClient

# получить URL и имя базы данных из переменных окружения
MONGO_URL = (os.getenv("MONGO_URL", "mongodb://localhost:27017"))
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "movie_api")

client = MongoClient(MONGO_URL)
database = client[MONGO_DB_NAME]
movies = database["movies"]

# получить подключение к базе данных
def get_db():
    return database

# получить коллекцию фильмов
def get_movies_collection():
    return movies