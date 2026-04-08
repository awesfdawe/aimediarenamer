from pydantic import BaseModel, Field
from typing import TypeVar, Generic

TitleT = TypeVar("TitleT")


class BaseSearchParams(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)


class TvSearchParams(BaseSearchParams):
    first_air_date_year: int | None = Field(None, ge=1850, le=2100)


class MovieSearchParams(BaseSearchParams):
    primary_release_year: int | None = Field(None, ge=1850, le=2100)


class TmdbSearchAnswer(BaseModel, Generic[TitleT]):
    page: int
    total_pages: int
    total_results: int
    results: list[TitleT]


class TmdbTvSearchAnswer(BaseModel):
    adult: bool
    backdrop_path: str | None
    genre_ids: list[int]
    id: int
    origin_country: list[str] | None
    original_language: str | None
    original_name: str | None
    overview: str | None
    popularity: float
    poster_path: str | None
    first_air_date: str | None
    name: str | None
    vote_average: float
    vote_count: int


class TmdbMovieSearchAnswer(BaseModel):
    adult: bool
    backdrop_path: str | None
    genre_ids: list[int]
    id: int
    original_language: str | None
    original_title: str | None
    overview: str | None
    popularity: float
    poster_path: str | None
    release_date: str | None
    title: str | None
    video: bool
    vote_average: float
    vote_count: int
