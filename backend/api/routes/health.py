

from fastapi import APIRouter

from backend.core.config import get_settings
from backend.schemas.prediction import HealthResponse

router = APIRouter()


@router.get("/", response_model=HealthResponse, tags=["Sistema"])
def health_check():
    settings = get_settings()
    return HealthResponse(
        mensaje="Servidor de Inteligencia Artificial activo",
        estado="OK",
        version=settings.APP_VERSION,
    )
