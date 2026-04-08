from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Literal
from functools import lru_cache

class Settings(BaseSettings):
    environment: Literal["dev", "prod"] = Field("prod")
    
    genai_api_key: str
    tmdb_api_key: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore") 

@lru_cache()
def get_settings() -> Settings:
    return Settings()