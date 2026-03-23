
from fastapi import APIRouter, Depends

from backend.core.dependencies import get_historical_data, get_model
from backend.schemas.prediction import EscenarioRequest, PrediccionResponse
from backend.services.prediction_service import PredictionService

router = APIRouter()


@router.post(
    "/predecir",
    response_model=PrediccionResponse,
    tags=["Predicción"],
    summary="Simular escenario económico",
    description="Recibe parámetros macroeconómicos y predice el volumen de denuncias mensuales.",
)
def predecir(
    escenario: EscenarioRequest,
    model=Depends(get_model),
    df_hist=Depends(get_historical_data),
):

    return PredictionService.predict(escenario, model, df_hist)
