import os
from pydantic import AnyHttpUrl, field_validator
from typing import List, Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API settings
    API_V1_STR: str = "/api/v1"
    
    # CORS settings - parse from comma-separated string in .env
    ALLOWED_ORIGINS_STR: str = ""
    ALLOWED_ORIGINS: List[str] = ["http://localhost", "http://localhost:3000", "http://localhost:8001"]

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v, info):
        if isinstance(v, str) and not v.startswith("["):
            return [origin.strip() for origin in v.split(",")]
        return v

    # Tesseract OCR path - adjust for your environment
    TESSERACT_CMD: str = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    
    # Temporary file settings
    TEMP_DIR: Optional[str] = None  # None means use system default temp directory
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()