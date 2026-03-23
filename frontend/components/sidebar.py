

import os
import streamlit as st



LOGO_PATH = os.path.join(os.path.dirname(__file__), "..", "assets", "logo.svg")


def render_sidebar():
    
    with st.sidebar:
        # Logo del sistema
        if os.path.exists(LOGO_PATH):
            st.image(LOGO_PATH, width=90)
        st.markdown("### ⚙️ Panel de Control")
        st.caption("Configure los parámetros del escenario económico")

        st.divider()

        # Modo de simulación
        modo = st.radio(
            "🎯 Nivel de Análisis",
            ["Simple (Próximo Mes)", "Shock (Crisis Sostenida)"],
            help="**Simple**: predice el próximo mes con cambio puntual.\n\n"
                 "**Shock**: simula que las condiciones se mantienen por un trimestre.",
        )

        st.divider()


        st.markdown("#### 📊 Parámetros Económicos")

        ipc = st.slider(
            "📈 Índice de Precios (IPC)",
            min_value=100.0,
            max_value=140.0,
            value=116.5,
            step=0.5,
            help="Simula la inflación acumulada. Valor actual ~116.",
        )

        desempleo = st.slider(
            "💼 Tasa de Desempleo (%)",
            min_value=3.0,
            max_value=20.0,
            value=7.2,
            step=0.1,
            help="Porcentaje de desempleo en Lima. Actual ~7.2%.",
        )

        covid = st.toggle(
            "🚨 Estado de Emergencia",
            value=False,
            help="Activa restricciones tipo pandemia.",
        )

        st.divider()

        # Botón de simulación
        btn_simular = st.button(
            "Ejecutar Simulación",
            width="stretch",
            type="primary",
        )


        modo_shock = "Shock" in modo
        if modo_shock:
            st.warning(
                "⚡ **Modo Shock activo**: El modelo simulará que las condiciones "
                "económicas se mantienen durante 3 meses consecutivos.",
                icon="⚡",
            )

    return ipc, desempleo, covid, modo_shock, btn_simular
