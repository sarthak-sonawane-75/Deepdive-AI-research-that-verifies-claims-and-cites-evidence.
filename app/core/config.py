from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "DeepDive"
    mesh_api_key: str = ""
    mesh_model: str = "openai/gpt-4o"
    mesh_base_url: str = "https://api.meshapi.ai/v1"
    max_research_rounds: int = 2
    min_verified_claims: int = 3
    database_path: str = "deepdive.sqlite3"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)


@lru_cache
def get_settings() -> Settings:
    return Settings()
