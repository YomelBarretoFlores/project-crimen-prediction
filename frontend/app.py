
import os
import streamlit as st
import requests
import pandas as pd


from components.sidebar import render_sidebar
from components.metrics import render_metrics
from components.charts import render_timeline_chart, render_context_table


st.set_page_config(
    page_title="IA Criminalidad Perú — UNASAM",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown("""
    <style>
    .stButton > button[kind="primary"] {
        background-color: #2563EB;
        border-color: #2563EB;
    }
    .stButton > button[kind="primary"]:hover {
        background-color: #1D4ED8;
        border-color: #1D4ED8;
    }
    </style>
""", unsafe_allow_html=True)


API_URL = os.getenv("API_URL", "http://127.0.0.1:8000").rstrip("/")



@st.cache_data(ttl=300)
def load_historical_data():
    
    try:
        res = requests.get(f"{API_URL}/historico?ultimos_meses=12", timeout=120)
        res.raise_for_status()
        data = res.json()["datos"]
        df = pd.DataFrame(data)
        df["fecha"] = pd.to_datetime(df["fecha"])
        df = df.set_index("fecha").sort_index()
        
        df = df.rename(columns={
            "nro_denuncias": "nro_denuncias",
            "indice_precios": "indice_precios",
            "tasa_desempleo": "tasa_desempleo",
        })
      
        if "es_covid" not in df.columns:
            df["es_covid"] = 0
        return df
    except Exception:
        
        fallback_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "gold_nacional_96m.parquet"
        )
        if os.path.exists(fallback_path):
            df = pd.read_parquet(fallback_path)
            df["fecha"] = pd.to_datetime(df["fecha"])
            df = df.set_index("fecha").sort_index()
            return df.tail(12)
        return None





ipc, desempleo, covid, modo_shock, btn_simular = render_sidebar()


st.title("🛡️ Sistema Inteligente de Seguridad Ciudadana")
st.caption(
    "Predictor de Criminalidad basado en Inteligencia Artificial y Variables "
    "Macroeconómicas · Proyecto UNASAM"
)


df_hist = load_historical_data()

if df_hist is None:
    st.error(
        "⚠️ No se pudieron cargar los datos históricos. "
        "Asegúrese de que la API esté activa o que el archivo Parquet exista."
    )
    st.stop()

ultimo_valor_real = int(df_hist["nro_denuncias"].iloc[-1])


if btn_simular:
    payload = {
        "ipc": ipc,
        "desempleo": desempleo,
        "covid": 1 if covid else 0,
        "modo_shock": modo_shock,
    }

    try:
        with st.spinner("🧠 Procesando escenario con el modelo de IA..."):
            res = requests.post(f"{API_URL}/predecir", json=payload, timeout=120)
            res.raise_for_status()
            data = res.json()

        prediccion = data["denuncias_estimadas"]
        nivel_riesgo = data["nivel_riesgo"]
        modo = data["escenario"]["modo"]


        render_metrics(prediccion, ultimo_valor_real, nivel_riesgo, modo)

        st.markdown("")  


        render_timeline_chart(df_hist, prediccion, ultimo_valor_real)

    
        render_context_table(df_hist)


        with st.expander("📝 Detalles de la Simulación", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Parámetros de Entrada**")
                st.json({
                    "IPC": ipc,
                    "Desempleo (%)": desempleo,
                    "Estado de Emergencia": "Sí" if covid else "No",
                    "Modo": "Shock (Crisis Sostenida)" if modo_shock else "Simple (Próximo Mes)",
                })
            with col2:
                st.markdown("**Resultado del Modelo**")
                st.json({
                    "Denuncias Estimadas": f"{prediccion:,}",
                    "Nivel de Riesgo": nivel_riesgo,
                    "Diferencia vs Real": f"{prediccion - ultimo_valor_real:+,}",
                    "Contexto": data["contexto"],
                })

    except requests.ConnectionError:
        st.error(
            "🔌 **Error de conexión**: No se pudo contactar al servidor de IA.\n\n"
            f"Verifique que la API esté corriendo en `{API_URL}`\n\n"
            "```bash\nuvicorn backend.main:app --reload\n```"
        )
    except requests.HTTPError as e:
        st.error(f"⚠️ **Error HTTP** {e.response.status_code}: {e.response.text}")
    except Exception as e:
        st.error(f"❌ **Error inesperado**: {e}")

else:
 
    st.info(
        "👈 **Configure los parámetros** en el panel lateral y presione "
        "**'Ejecutar Simulación'** para generar la predicción.",
        icon="ℹ️",
    )


    render_context_table(df_hist)




st.divider()
st.caption(
    "**UNASAM** · Facultad de Ciencias · Estadística e Informática  \n"
    "Sistema Inteligente de Seguridad Ciudadana · Modelo Random Forest (2018–2025)  \n"
    "Datos: INEI & PNP & BCRP (2018–2025) · Proyecto de Ciencia de Datos"
)