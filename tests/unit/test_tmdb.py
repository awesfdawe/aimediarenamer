import pytest
import httpx
import respx
from hypothesis import given, settings, strategies as st
from pydantic import ValidationError

from src.tools.tmdb import search_in_tmdb, get_details_in_tmdb

# Temporary written by ai, will rewrite it later

TMDB_BASE_URL = "https://api.themoviedb.org/3"

# --- Mock Data ---

MOCK_TV_SEARCH_RESPONSE = {
    "page": 1,
    "total_pages": 1,
    "total_results": 1,
    "results": [
        {
            "adult": False,
            "genre_ids": [18],
            "id": 123,
            "name": "Test TV Show",
            "popularity": 5.0,
            "vote_average": 8.0,
            "vote_count": 100,
        }
    ]
}

MOCK_MOVIE_SEARCH_RESPONSE = {
    "page": 1,
    "total_pages": 1,
    "total_results": 1,
    "results": [
        {
            "adult": False,
            "backdrop_path": None,
            "genre_ids": [28],
            "id": 456,
            "title": "Test Movie",
            "popularity": 6.0,
            "vote_average": 7.5,
            "vote_count": 150,
            "video": False,
        }
    ]
}

MOCK_TV_DETAILS_RESPONSE = {
    "adult": False,
    "id": 123,
    "in_production": True,
    "number_of_episodes": 20,
    "number_of_seasons": 2,
    "popularity": 5.0,
    "vote_average": 8.0,
    "vote_count": 100,
    "name": "Test TV Show Details"
}

MOCK_MOVIE_DETAILS_RESPONSE = {
    "adult": False,
    "id": 456,
    "budget": 1000000,
    "revenue": 5000000,
    "popularity": 6.0,
    "vote_average": 7.5,
    "vote_count": 150,
    "video": False,
    "title": "Test Movie Details"
}

# --- Tests for search_in_tmdb ---

@pytest.mark.asyncio
async def test_search_tv_success(async_client):
    with respx.mock(assert_all_called=False) as mock:
        route = mock.get(path="/3/search/tv").respond(200, json=MOCK_TV_SEARCH_RESPONSE)
        result = await search_in_tmdb(async_client, "Test", 2024, "tv")
        
        assert route.called
        assert result is not None
        assert result.total_results == 1
        assert result.results[0].name == "Test TV Show"

@pytest.mark.asyncio
async def test_search_movie_success(async_client):
    with respx.mock(assert_all_called=False) as mock:
        route = mock.get(path="/3/search/movie").respond(200, json=MOCK_MOVIE_SEARCH_RESPONSE)
        result = await search_in_tmdb(async_client, "Test Movie", None, "movie")
        
        assert route.called
        assert result is not None
        assert result.results[0].title == "Test Movie"

@pytest.mark.asyncio
async def test_search_http_error(async_client):
    with respx.mock(assert_all_called=False) as mock:
        mock.get(path="/3/search/tv").respond(404, text="Not Found")
        result = await search_in_tmdb(async_client, "Test", None, "tv")
        assert result is None

@pytest.mark.asyncio
async def test_search_request_error(async_client):
    with respx.mock(assert_all_called=False) as mock:
        mock.get(path="/3/search/tv").mock(side_effect=httpx.ConnectError("Network Error"))
        result = await search_in_tmdb(async_client, "Test", None, "tv")
        assert result is None

@pytest.mark.asyncio
async def test_search_response_validation_error(async_client):
    with respx.mock(assert_all_called=False) as mock:
        mock.get(path="/3/search/tv").respond(200, json={"page": 1}) 
        with pytest.raises(ValidationError):
            await search_in_tmdb(async_client, "Test", None, "tv")

# --- Tests for get_details_in_tmdb ---

@pytest.mark.asyncio
async def test_get_details_tv_success(async_client):
    with respx.mock(assert_all_called=False) as mock:
        mock.get(path="/3/tv/123").respond(200, json=MOCK_TV_DETAILS_RESPONSE)
        result = await get_details_in_tmdb(async_client, 123, "tv")
        assert result is not None
        assert result.id == 123
        assert result.number_of_episodes == 20

@pytest.mark.asyncio
async def test_get_details_movie_success(async_client):
    with respx.mock(assert_all_called=False) as mock:
        mock.get(path="/3/movie/456").respond(200, json=MOCK_MOVIE_DETAILS_RESPONSE)
        result = await get_details_in_tmdb(async_client, 456, "movie")
        assert result is not None
        assert result.id == 456
        assert result.budget == 1000000

@pytest.mark.asyncio
async def test_get_details_http_error(async_client):
    with respx.mock(assert_all_called=False) as mock:
        mock.get(path="/3/tv/999").respond(500, text="Internal Server Error")
        result = await get_details_in_tmdb(async_client, 999, "tv")
        assert result is None

# --- Edge Cases & Property-Based Testing ---

@settings(max_examples=20)
@given(
    query=st.text(min_size=0, max_size=2500), # testing edge sizes for query (valid: 1-2000)
    year=st.one_of(st.none(), st.integers(min_value=1000, max_value=3000)) # valid: 1850-2100
)
@pytest.mark.asyncio
async def test_search_input_validation_fuzz(query, year):
    """Test that pydantic catches bad input properties using hypothesis"""
    is_query_valid = 1 <= len(query) <= 2000
    is_year_valid = year is None or (1850 <= year <= 2100)
    
    async with httpx.AsyncClient() as client:
        with respx.mock(assert_all_called=False) as mock:
            mock.get(path="/3/search/tv").respond(200, json=MOCK_TV_SEARCH_RESPONSE)
        
            if not is_query_valid or not is_year_valid:
                with pytest.raises(ValidationError):
                    await search_in_tmdb(client, query, year, "tv")
            else:
                result = await search_in_tmdb(client, query, year, "tv")
                assert result is not None
