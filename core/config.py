import os
from pathlib import Path
from pydantic import BaseModel

class Settings(BaseModel):
    # Database and external config
    DB_HOST: str = os.environ.get("DB_HOST", "localhost")
    DB_USER: str = "root"
    DB_PASS: str = "root"
    DB_NAME: str = "postgres"
    DB_PORT: int = 5432


settings = Settings()
