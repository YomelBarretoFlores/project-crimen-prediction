
import pandas as pd

from backend.schemas.prediction import (
    EscenarioInfo,
    EscenarioRequest,
    PrediccionResponse,
)
from backend.services.data_engine import (
    build_shock_features,
    build_simple_features,
    calculate_risk_level,
)


class PredictionService:
    

    @staticmethod
    def predict(
        escenario: EscenarioRequest,
        model,
        df_hist: pd.DataFrame,
    ) -> PrediccionResponse:
       

   
        if escenario.modo_shock:
            X_input = build_shock_features(
                df_hist, escenario.ipc, escenario.desempleo, escenario.covid
            )
        else:
            X_input = build_simple_features(
                df_hist, escenario.ipc, escenario.desempleo, escenario.covid
            )


        resultado = model.predict(X_input)
        prediccion = int(resultado[0])


        nivel_riesgo = calculate_risk_level(prediccion, df_hist)

 
        return PrediccionResponse(
            escenario=EscenarioInfo(
                ipc=escenario.ipc,
                desempleo=escenario.desempleo,
                modo="shock" if escenario.modo_shock else "simple",
            ),
            denuncias_estimadas=prediccion,
            nivel_riesgo=nivel_riesgo,
            contexto=f"Datos históricos hasta {df_hist.index.max().strftime('%B %Y')}",
        )
