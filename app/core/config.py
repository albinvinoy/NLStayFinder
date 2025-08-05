import os
from typing import List, Union, Dict, Any
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator

class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "NLStayFinder"
    API_PREFIX: str = "/api"
    
    # CORS settings
    CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Database settings - SQLite for development
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./nlstayfinder.db")
    SQLALCHEMY_DATABASE_URI: str = DATABASE_URL
    
    # PostgreSQL settings (for future production deployment)
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "nlstayfinder")
    
    @property
    def is_sqlite(self) -> bool:
        """Check if using SQLite database"""
        return self.SQLALCHEMY_DATABASE_URI.startswith("sqlite")
    
    # Scraper settings
    SCRAPER_INTERVAL_HOURS: int = int(os.getenv("SCRAPER_INTERVAL_HOURS", "24"))
    SCRAPER_URLS: List[str] = [
        "https://www.zillow.com/homes/for_rent/"
    ]
    
    # Zillow robots.txt rules to follow
    ZILLOW_ROBOTS_RULES: Dict[str, Any] = {
        "allowed_paths": [
            "/homes/for_rent/",
            "/homes/for_sale/",
            "/apartments/"
        ],
        "disallowed_paths": [
            "/homedetails/",
            "/myzillow/",
            "/profile/",
            "/reviews/",
            "/user/",
            "/forum/"
        ],
        "crawl_delay": 5  # seconds between requests
    }
    
    # AWS settings
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    AWS_REGION: str = os.getenv("AWS_REGION", "us-west-2")
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 