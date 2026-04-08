from pydantic import BaseModel, Field
from typing import TypeVar, Generic

TitleT = TypeVar("TitleT", bound=BaseModel)


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
    backdrop_path: str | None = None
    genre_ids: list[int]
    id: int
    origin_country: list[str] | None = None
    original_language: str | None = None
    original_name: str | None = None
    overview: str | None = None
    popularity: float
    poster_path: str | None = None
    first_air_date: str | None = None
    name: str
    vote_average: float
    vote_count: int


class TmdbMovieSearchAnswer(BaseModel):
    adult: bool
    backdrop_path: str | None
    genre_ids: list[int]
    id: int
    original_language: str | None = None
    original_title: str | None = None
    overview: str | None = None
    popularity: float
    poster_path: str | None = None
    release_date: str | None = None
    title: str
    video: bool
    vote_average: float
    vote_count: int


# Parts below was written by ai
class Genre(BaseModel):
    id: int
    name: str


class ProductionCompany(BaseModel):
    id: int
    logo_path: str | None = None
    name: str
    origin_country: str


class ProductionCountry(BaseModel):
    iso_3166_1: str
    name: str


class SpokenLanguage(BaseModel):
    english_name: str
    iso_639_1: str
    name: str


class Creator(BaseModel):
    id: int
    credit_id: str
    name: str
    gender: int
    profile_path: str | None = None


class Network(BaseModel):
    id: int
    logo_path: str | None = None
    name: str
    origin_country: str


class Episode(BaseModel):
    id: int
    name: str
    overview: str
    vote_average: float
    vote_count: int
    air_date: str | None = None
    episode_number: int
    production_code: str
    runtime: int | None = None
    season_number: int
    show_id: int
    still_path: str | None = None


class Season(BaseModel):
    air_date: str | None = None
    episode_count: int
    id: int
    name: str
    overview: str
    poster_path: str | None = None
    season_number: int
    vote_average: float


class BelongsToCollection(BaseModel):
    id: int
    name: str
    poster_path: str | None = None
    backdrop_path: str | None = None


class TmdbTvDetailsAnswer(BaseModel):
    adult: bool
    backdrop_path: str | None = None
    created_by: list[Creator] = Field(default_factory=list)
    episode_run_time: list[int] = Field(default_factory=list)
    first_air_date: str | None = None
    genres: list[Genre] = Field(default_factory=list)
    homepage: str | None = None
    id: int
    in_production: bool
    languages: list[str] = Field(default_factory=list)
    last_air_date: str | None = None
    last_episode_to_air: Episode | None = None
    name: str | None = None
    next_episode_to_air: Episode | None = None
    networks: list[Network] = Field(default_factory=list)
    number_of_episodes: int
    number_of_seasons: int
    origin_country: list[str] = Field(default_factory=list)
    original_language: str | None = None
    original_name: str | None = None
    overview: str | None = None
    popularity: float
    poster_path: str | None = None
    production_companies: list[ProductionCompany] = Field(default_factory=list)
    production_countries: list[ProductionCountry] = Field(default_factory=list)
    seasons: list[Season] = Field(default_factory=list)
    spoken_languages: list[SpokenLanguage] = Field(default_factory=list)
    status: str | None = None
    tagline: str | None = None
    type: str | None = None
    vote_average: float
    vote_count: int


class TmdbMovieDetailsAnswer(BaseModel):
    adult: bool
    backdrop_path: str | None = None
    belongs_to_collection: BelongsToCollection | None = None
    budget: int
    genres: list[Genre] = Field(default_factory=list)
    homepage: str | None = None
    id: int
    imdb_id: str | None = None
    origin_country: list[str] = Field(default_factory=list)
    original_language: str | None = None
    original_title: str | None = None
    overview: str | None = None
    popularity: float
    poster_path: str | None = None
    production_companies: list[ProductionCompany] = Field(default_factory=list)
    production_countries: list[ProductionCountry] = Field(default_factory=list)
    release_date: str | None = None
    revenue: int
    runtime: int | None = None
    spoken_languages: list[SpokenLanguage] = Field(default_factory=list)
    status: str | None = None
    tagline: str | None = None
    title: str | None = None
    video: bool
    vote_average: float
    vote_count: int
