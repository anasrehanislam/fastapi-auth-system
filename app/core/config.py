# app/core/config.py

from pydantic_settings import BaseSettings  # Correct import

class Settings(BaseSettings):
    SECRET_KEY: str
    API_KEY: str
    DATABASE_URL: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # OAuth configurations
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str

    class Config:
        env_file = ".env"
        #extra = "allow"  # Allow extra fields in environment file
settings = Settings()
