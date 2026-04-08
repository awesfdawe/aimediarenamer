import httpx
from typing import Literal
from loguru import logger
from pydantic import ValidationError

from src.config import get_settings
from src.tools.tmdb.models import (
    TvSearchParams,
    MovieSearchParams,
    TmdbSearchAnswer,
    TmdbTvSearchAnswer,
    TmdbMovieSearchAnswer,
    TmdbTvDetailsAnswer,
    TmdbMovieDetailsAnswer,
)

settings = get_settings()

tmdb_base_url = "https://api.themoviedb.org/3"

logger = logger.bind(module=__name__)


async def search_in_tmdb(
    client: httpx.AsyncClient,
    search_request: str,
    air_year: int | None,
    title_type: Literal["tv", "movie"],
) -> TmdbSearchAnswer[TmdbTvSearchAnswer] | TmdbSearchAnswer[TmdbMovieSearchAnswer] | None:
    try:
        if title_type == "tv":
            search_params = TvSearchParams(query=search_request, first_air_date_year=air_year)
            ResponseModel = TmdbSearchAnswer[TmdbTvSearchAnswer]
        else:
            search_params = MovieSearchParams(query=search_request, primary_release_year=air_year)
            ResponseModel = TmdbSearchAnswer[TmdbMovieSearchAnswer]

        request_params = search_params.model_dump(exclude_none=True)
        response = await client.get(
            f"{tmdb_base_url}/search/{title_type}",
            params=request_params,
            headers={
                "Authorization": f"Bearer {settings.tmdb_api_key}",
                "accept": "application/json",
            },
            timeout=5.0,
        )
        response.raise_for_status()
        data = ResponseModel.model_validate(response.json())
        logger.debug(f"Sucessful request with total results: {data.total_results}")
        return data
    except ValidationError as exception:
        logger.error(f"Response data validation error. Details: {exception.errors()}")
        raise
    except httpx.HTTPStatusError as exception:
        status = exception.response.status_code
        request_url = exception.request.url
        response_body = exception.response.text.strip()[:300] or "No Content"
        logger.error(f"Response error: {status} at request: {request_url} with response body: {response_body}")
        return None
    except httpx.RequestError as exception:
        request_url = exception.request.url
        logger.error(f"Request error: {exception} at request: {request_url}")
        return None
    except Exception as exception:
        logger.exception(f"Unexpected error: {exception}")
        raise


async def get_details_in_tmdb(
    client: httpx.AsyncClient,
    title_tmdb_id: int,
    title_type: Literal["tv", "movie"],
) -> TmdbTvDetailsAnswer | TmdbMovieDetailsAnswer | None:
    try:
        if title_type == "tv":
            ResponseModel = TmdbTvDetailsAnswer
        else:
            ResponseModel = TmdbMovieDetailsAnswer

        response = await client.get(
            f"{tmdb_base_url}/{title_type}/{title_tmdb_id}",
            headers={
                "Authorization": f"Bearer {settings.tmdb_api_key}",
                "accept": "application/json",
            },
            timeout=5.0,
        )
        response.raise_for_status()
        data = ResponseModel.model_validate(response.json())
        logger.debug(f"Sucessful request with title id: {data.id}")
        return data
    except ValidationError as exception:
        logger.error(f"Response data validation error. Details: {exception.errors()}")
        raise
    except httpx.HTTPStatusError as exception:
        status = exception.response.status_code
        request_url = exception.request.url
        response_body = exception.response.text.strip()[:300] or "No Content"
        logger.error(f"Response error: {status} at request: {request_url} with response body: {response_body}")
        return None
    except httpx.RequestError as exception:
        request_url = exception.request.url
        logger.error(f"Request error: {exception} at request: {request_url}")
        return None
    except Exception as exception:
        logger.exception(f"Unexpected error: {exception}")
        raise