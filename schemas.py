from pydantic import BaseModel, Field


# Схема входящих данных
class MovieResponse(BaseModel):
    name: str = Field(..., min_length=1, description="Название фильма")
    plot: str = Field(..., min_length=1, description="Сюжет")
    genres: list[str] = Field(..., min_length=1, description="Жанры фильма")
    casts: list[str] = Field(..., min_length=1, description="Актерский состав")


# Схема данных фильма из базы данных
class MovieDB(MovieResponse):
    id: int
