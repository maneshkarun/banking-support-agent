"""Application configuration."""

from functools import lru_cache

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load .env into os.environ so third-party SDKs (e.g. LangSmith) can read
# their env vars. pydantic-settings only uses .env for its own fields.
load_dotenv()


class Settings(BaseSettings):
    """Environment-backed application settings."""

    app_name: str = "Simple Banking API"
    database_url: str = "sqlite:///./banking.db"
    debug: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings."""

    return Settings()