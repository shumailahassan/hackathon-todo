from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://username:password@localhost:5432/auth_db"

    # JWT
    JWT_SECRET_KEY: str = "your-super-secret-jwt-key-here-make-it-long-and-random"
    JWT_REFRESH_SECRET_KEY: str = "your-super-secret-refresh-key-here-make-it-long-and-random"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Password requirements
    MIN_PASSWORD_LENGTH: int = 8
    REQUIRE_UPPERCASE: bool = True
    REQUIRE_LOWERCASE: bool = True
    REQUIRE_NUMBERS: bool = True
    REQUIRE_SPECIAL_CHARS: bool = True

    # Rate limiting
    LOGIN_ATTEMPTS_LIMIT: int = 5
    LOGIN_ATTEMPTS_WINDOW: int = 900  # 15 minutes in seconds

    # Email configuration
    EMAIL_HOST: Optional[str] = None
    EMAIL_PORT: Optional[int] = 587
    EMAIL_USER: Optional[str] = None
    EMAIL_PASSWORD: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()