import os
from pymongo import MongoClient


MONGO_URL = (
    os.getenv("MONGO_URL")
    or os.getenv("MONGO_URI")
    or os.getenv("DATABASE_URL")
    or "mongodb://localhost:27017"
)
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "movie_api")

client = MongoClient(MONGO_URL)
database = client[MONGO_DB_NAME]
movies = database["movies"]


def get_db():
    return database

def get_movies_collection():
    return movies