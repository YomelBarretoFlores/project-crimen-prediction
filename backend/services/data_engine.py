

import pandas as pd


def build_simple_features(
    df_hist: pd.DataFrame,
    ipc: float,
    desempleo: float,
    covid: int,
) -> pd.DataFrame:
   
    fila = {
        "ipc_lag_1": ipc,
        "ipc_lag_2": df_hist["indice_precios"].iloc[-1],
        "desempleo_lag_1": desempleo,
        "desempleo_lag_3": df_hist["tasa_desempleo"].iloc[-2],
        "es_covid": covid,
        "denuncias_media_3m": df_hist["nro_denuncias"].tail(3).mean(),
    }
    return pd.DataFrame([fila])


def build_shock_features(
    df_hist: pd.DataFrame,
    ipc: float,
    desempleo: float,
    covid: int,
) -> pd.DataFrame:
    
    media_actual = df_hist["nro_denuncias"].iloc[-1]
    ipc_historico = df_hist["indice_precios"].iloc[-1]
    sigma = df_hist["nro_denuncias"].std()

  
    delta_ipc = (ipc - ipc_historico) / ipc_historico if ipc_historico != 0 else 0

 
    media_simulada = media_actual + (delta_ipc * sigma * 1.5)

  
    media_simulada = max(media_simulada, 0)

    fila = {
        "ipc_lag_1": ipc,
        "ipc_lag_2": ipc,                    
        "desempleo_lag_1": desempleo,
        "desempleo_lag_3": desempleo,        
        "es_covid": covid,
        "denuncias_media_3m": media_simulada,
    }
    return pd.DataFrame([fila])


def calculate_risk_level(prediccion: int, df_hist: pd.DataFrame) -> str:
   
    denuncias = df_hist["nro_denuncias"]
    p25 = denuncias.quantile(0.25)
    p75 = denuncias.quantile(0.75)

    if prediccion <= p25:
        return "BAJO"
    elif prediccion <= p75:
        return "MODERADO"
    else:
        return "ALTO"
