

import streamlit as st


def render_metrics(prediccion: int, ultimo_real: int, nivel_riesgo: str, modo: str):
    
    m1, m2, m3 = st.columns(3)


    diff = prediccion - ultimo_real
    m1.metric(
        label="🤖 Predicción IA",
        value=f"{prediccion:,}",
        delta=f"{diff:+,} vs último real",
        delta_color="inverse", 
    )

 
    riesgo_config = {
        "BAJO": ("🟢", "El escenario presenta un riesgo controlado."),
        "MODERADO": ("🟡", "El escenario requiere monitoreo activo."),
        "ALTO": ("🔴", "⚠️ Escenario de riesgo elevado. Se requiere acción."),
    }
    emoji, descripcion = riesgo_config.get(nivel_riesgo, ("⚪", "Sin datos"))

    m2.metric(
        label="🎯 Nivel de Riesgo",
        value=f"{emoji} {nivel_riesgo}",
    )
    m2.caption(descripcion)

   
    modo_display = "⚡ SHOCK" if modo == "shock" else "📊 SIMPLE"
    m3.metric(
        label="🔧 Modo Activo",
        value=modo_display,
    )
    m3.caption(
        "Crisis sostenida (3 meses)" if modo == "shock"
        else "Cambio puntual del próximo mes"
    )
