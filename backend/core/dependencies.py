

import logging
from functools import lru_cache

import joblib
import pandas as pd

from backend.core.config import get_settings

logger = logging.getLogger(__name__)


@lru_cache
def get_model():
    settings = get_settings()
    path = settings.MODEL_PATH

    if not path.exists():
        raise FileNotFoundError(f"Modelo no encontrado en: {path}")

    logger.info("🧠 Cargando modelo ML desde %s", path)
    model = joblib.load(path)
    logger.info("✅ Modelo cargado exitosamente.")
    return model


@lru_cache
def get_historical_data() -> pd.DataFrame:
    settings = get_settings()
    path = settings.DATA_PATH

    if not path.exists():
        raise FileNotFoundError(f"Datos históricos no encontrados en: {path}")

    logger.info("📊 Cargando datos históricos desde %s", path)
    df = pd.read_parquet(path)

    if "fecha" in df.columns:
        df["fecha"] = pd.to_datetime(df["fecha"])
        df = df.set_index("fecha").sort_index()

    logger.info("✅ Datos cargados: %d filas, rango %s → %s",
                len(df), df.index.min().date(), df.index.max().date())
    return df
