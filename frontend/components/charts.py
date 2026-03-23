

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def render_timeline_chart(
    df_hist: pd.DataFrame,
    prediccion: int,
    ultimo_real: int,
):
    
    fig = go.Figure()

    
    sigma = df_hist["nro_denuncias"].std()
    upper = df_hist["nro_denuncias"] + sigma
    lower = df_hist["nro_denuncias"] - sigma

    fig.add_trace(go.Scatter(
        x=pd.concat([df_hist.index.to_series(), df_hist.index.to_series()[::-1]]),
        y=pd.concat([upper, lower[::-1]]),
        fill="toself",
        fillcolor="rgba(31, 119, 180, 0.1)",
        line=dict(color="rgba(0,0,0,0)"),
        showlegend=True,
        name="Banda ±1σ",
        hoverinfo="skip",
    ))

    
    fig.add_trace(go.Scatter(
        x=df_hist.index,
        y=df_hist["nro_denuncias"],
        mode="lines+markers",
        name="Datos Reales",
        line=dict(color="#1f77b4", width=3),
        marker=dict(size=6, color="#1f77b4"),
        hovertemplate="<b>%{x|%b %Y}</b><br>Denuncias: %{y:,.0f}<extra></extra>",
    ))

    
    fecha_pred = df_hist.index[-1] + pd.DateOffset(months=1)
    
    # ── Línea punteada de Proyección ──
    fig.add_trace(go.Scatter(
        x=[df_hist.index[-1], fecha_pred],
        y=[ultimo_real, prediccion],
        mode="lines",
        line=dict(color="#ff4b4b", width=4, dash="dash"),
        showlegend=False,
        hoverinfo="skip",
    ))

    # ── Punto Estrella de Predicción ──
    fig.add_trace(go.Scatter(
        x=[fecha_pred],
        y=[prediccion],
        mode="markers",
        name="Proyección IA",
        marker=dict(size=14, symbol="star", color="#ff4b4b"),
        hovertemplate="<b>%{x|%b %Y}</b><br>Predicción: %{y:,.0f}<extra></extra>",
    ))


    fig.add_annotation(
        x=fecha_pred,
        y=prediccion,
        text=f"<b>{prediccion:,}</b>",
        showarrow=True,
        arrowhead=2,
        arrowcolor="#ff4b4b",
        font=dict(size=14, color="#ff4b4b"),
        bgcolor="white",
        bordercolor="#ff4b4b",
        borderpad=6,
        borderwidth=1,
    )


    fig.update_layout(
        title="Tendencia de Criminalidad — Histórico vs Proyección IA",
        xaxis_title="Periodo",
        yaxis_title="Nro de Denuncias",
        yaxis_tickformat=",",
        template="plotly_white",
        height=420,
        margin=dict(l=60, r=30, t=60, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        hovermode="x unified",
    )

    st.plotly_chart(fig, width="stretch")


def render_context_table(df_hist: pd.DataFrame):

    df_display = df_hist.tail(6).copy()
    df_display = df_display.reset_index()
    df_display.columns = ["Fecha", "Denuncias", "IPC", "Desempleo (%)", "COVID"]


    df_display["Fecha"] = df_display["Fecha"].dt.strftime("%b %Y")
    df_display["Denuncias"] = df_display["Denuncias"].apply(lambda x: f"{int(x):,}")
    df_display["IPC"] = df_display["IPC"].round(2)
    df_display["Desempleo (%)"] = df_display["Desempleo (%)"].round(1)
    df_display["COVID"] = df_display["COVID"].map({0: "No", 1: "Sí"})

    st.markdown("#### 📋 Contexto Histórico (Últimos 6 meses)")
    st.dataframe(
        df_display,
        width="stretch",
        hide_index=True,
    )