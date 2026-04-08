import pytest
import pytest_asyncio
import httpx
from src.config import get_settings

@pytest.fixture(autouse=True)
def test_environment(monkeypatch):
    get_settings.cache_clear()
    monkeypatch.setenv("GENAI_API_KEY", "genai_fake_api_key_123")
    monkeypatch.setenv("TMDB_API_KEY", "tmdb_fake_api_key_123")

    yield

    get_settings.cache_clear()

@pytest_asyncio.fixture
async def async_client():
    async with httpx.AsyncClient() as client:
        yield client