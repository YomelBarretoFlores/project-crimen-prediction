
from fastapi import APIRouter, Depends, Query

from backend.core.dependencies import get_historical_data

router = APIRouter()


@router.get("/historico", tags=["Datos"])
def obtener_historico(
    ultimos_meses: int = Query(default=12, ge=1, le=96, description="Meses a consultar"),
    df_hist=Depends(get_historical_data),
):
    df_slice = df_hist.tail(ultimos_meses)

    registros = []
    for fecha, row in df_slice.iterrows():
        registros.append({
            "fecha": fecha.isoformat(),
            "nro_denuncias": int(row["nro_denuncias"]),
            "indice_precios": round(float(row["indice_precios"]), 2),
            "tasa_desempleo": round(float(row["tasa_desempleo"]), 2),
        })

    return {
        "total_registros": len(registros),
        "datos": registros,
    }
