from typing import Optional, Dict, Any

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    SERVER_HOSTNAME: str
    HTTP_PATH: str
    ACCESS_TOKEN: str
    DATABRICKS_DB: str = "fastapi"
    DATABRICKS_DATABASE_URI: Optional[str] = None

    @validator("DATABRICKS_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return "databricks+connector://token:{}@{}:443/{}".format(
            values.get("ACCESS_TOKEN"),
            values.get("SERVER_HOSTNAME"),
            values.get("DATABRICKS_DB"),
        )

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
