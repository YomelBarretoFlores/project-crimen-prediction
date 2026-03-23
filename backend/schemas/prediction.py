

from datetime import datetime
from pydantic import BaseModel, Field




class EscenarioRequest(BaseModel):
    ipc: float = Field(
        ...,
        ge=80.0,
        le=200.0,
        description="Índice de Precios al Consumidor (IPC). Rango razonable: 100-140.",
        examples=[116.5],
    )
    desempleo: float = Field(
        ...,
        ge=0.0,
        le=50.0,
        description="Tasa de desempleo en porcentaje. Rango razonable: 3-20%.",
        examples=[7.2],
    )
    covid: int = Field(
        default=0,
        ge=0,
        le=1,
        description="Estado de emergencia / restricciones. 0 = No, 1 = Sí.",
    )
    modo_shock: bool = Field(
        default=False,
        description="Si es True, simula un impacto económico sostenido (shock de 3 meses).",
    )




class EscenarioInfo(BaseModel):
    ipc: float
    desempleo: float
    modo: str 


class PrediccionResponse(BaseModel):
    escenario: EscenarioInfo
    denuncias_estimadas: int
    unidad: str = "denuncias mensuales"
    nivel_riesgo: str  
    contexto: str
    timestamp: datetime = Field(default_factory=datetime.now)


class HealthResponse(BaseModel):
    mensaje: str
    estado: str
    version: str


class ErrorResponse(BaseModel):
    detail: str
    status_code: int
