
from pathlib import Path
from functools import lru_cache

from pydantic_settings import BaseSettings



PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    APP_TITLE: str = "API de Predicción de Criminalidad - UNASAM"
    APP_DESCRIPTION: str = (
        "Servicio de simulación de denuncias basado en escenarios económicos. "
        "Proyecto de Seguridad Ciudadana con ML (Random Forest)."
    )
    APP_VERSION: str = "2.0.0"


    MODEL_PATH: Path = PROJECT_ROOT / "models" / "modelo_prediccion_crimen_2026.joblib"
    DATA_PATH: Path = PROJECT_ROOT / "data" / "gold_nacional_96m.parquet"


    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    CORS_ORIGINS: list[str] = ["*"]

    model_config = {
        "env_file": str(PROJECT_ROOT / ".env"),
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


@lru_cache
def get_settings() -> Settings:
    return Settings()
