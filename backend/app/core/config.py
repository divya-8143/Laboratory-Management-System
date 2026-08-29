import os
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Enterprise Laboratory Information System (LIS)"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    SECRET_KEY: str = os.getenv("SECRET_KEY", "clinical_laboratory_super_secure_jwt_secret_key_2026_x89f_enterprise")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite+aiosqlite:///./laboratory.db"
    )
    SYNC_DATABASE_URL: str = os.getenv(
        "SYNC_DATABASE_URL",
        "sqlite:///./laboratory.db"
    )

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "*"
    ]

    # File Storage & PDF Reports
    REPORT_STORAGE_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "reports")
    STATIC_DIR: str = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "static")
    LAB_NAME: str = "AcuPath Advanced Diagnostics & Reference Laboratories"
    LAB_ADDRESS: str = "742 Medical Center Blvd, Suite 400, Metro Health District"
    LAB_PHONE: str = "+1 (800) 555-LABS"
    LAB_EMAIL: str = "reports@acupathdiagnostics.com"
    LAB_ACCREDITATION: str = "ISO 15189:2022 & CLIA Certified Reference Laboratory"

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env", extra="ignore")


settings = Settings()
os.makedirs(settings.REPORT_STORAGE_DIR, exist_ok=True)
