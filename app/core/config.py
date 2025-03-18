import os
from dotenv import load_dotenv
from functools import lru_cache
from pydantic_settings import BaseSettings  # ✅ Correct import for Pydantic v2

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default-secret-key")  # Read from .env or use default
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
