"""
Tests unitarios — Servicios de data_engine y prediction.
Usa datos mockeados para no depender de archivos Parquet.
"""

import pytest
import pandas as pd
import numpy as np

from backend.services.data_engine import (
    build_simple_features,
    build_shock_features,
    calculate_risk_level,
)


@pytest.fixture
def mock_df_hist():
    """DataFrame histórico mockeado con 12 meses de datos simulados."""
    dates = pd.date_range("2025-01-01", periods=12, freq="MS")
    np.random.seed(42)
    return pd.DataFrame(
        {
            "nro_denuncias": np.random.randint(55000, 75000, size=12),
            "indice_precios": np.linspace(112.0, 116.5, 12),
            "tasa_desempleo": np.linspace(6.5, 7.2, 12),
            "es_covid": [0] * 12,
        },
        index=dates,
    )


# ═══════════════════════════════════════════════
#  build_simple_features
# ═══════════════════════════════════════════════

class TestBuildSimpleFeatures:
    """Tests para la preparación de features en modo simple."""

    def test_returns_dataframe(self, mock_df_hist):
        result = build_simple_features(mock_df_hist, 116.5, 7.2, 0)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1

    def test_has_required_columns(self, mock_df_hist):
        result = build_simple_features(mock_df_hist, 116.5, 7.2, 0)
        expected_cols = {
            "ipc_lag_1", "ipc_lag_2", "desempleo_lag_1",
            "desempleo_lag_3", "es_covid", "denuncias_media_3m",
        }
        assert set(result.columns) == expected_cols

    def test_ipc_lag_1_equals_input(self, mock_df_hist):
        result = build_simple_features(mock_df_hist, 120.0, 7.2, 0)
        assert result["ipc_lag_1"].iloc[0] == 120.0

    def test_covid_value_propagated(self, mock_df_hist):
        result = build_simple_features(mock_df_hist, 116.5, 7.2, 1)
        assert result["es_covid"].iloc[0] == 1


# ═══════════════════════════════════════════════
#  build_shock_features
# ═══════════════════════════════════════════════

class TestBuildShockFeatures:
    """Tests para la preparación de features en modo shock."""

    def test_returns_dataframe(self, mock_df_hist):
        result = build_shock_features(mock_df_hist, 130.0, 15.0, 0)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1

    def test_lags_use_user_values_for_shock(self, mock_df_hist):
        """En modo shock, ipc_lag_2 y desempleo_lag_3 usan valores del usuario."""
        result = build_shock_features(mock_df_hist, 130.0, 15.0, 0)
        assert result["ipc_lag_2"].iloc[0] == 130.0
        assert result["desempleo_lag_3"].iloc[0] == 15.0

    def test_higher_ipc_increases_media(self, mock_df_hist):
        """Un IPC más alto que el histórico debe incrementar la media simulada."""
        ipc_historico = mock_df_hist["indice_precios"].iloc[-1]
        result = build_shock_features(mock_df_hist, ipc_historico + 20, 7.2, 0)
        media_actual = mock_df_hist["nro_denuncias"].iloc[-1]
        media_simulada = result["denuncias_media_3m"].iloc[0]
        assert media_simulada > media_actual

    def test_lower_ipc_decreases_media(self, mock_df_hist):
        """Un IPC más bajo que el histórico debe disminuir la media simulada."""
        ipc_historico = mock_df_hist["indice_precios"].iloc[-1]
        result = build_shock_features(mock_df_hist, ipc_historico - 10, 7.2, 0)
        media_actual = mock_df_hist["nro_denuncias"].iloc[-1]
        media_simulada = result["denuncias_media_3m"].iloc[0]
        assert media_simulada < media_actual

    def test_media_simulada_non_negative(self, mock_df_hist):
        """La media simulada nunca debe ser negativa."""
        result = build_shock_features(mock_df_hist, 50.0, 7.2, 0)
        assert result["denuncias_media_3m"].iloc[0] >= 0


# ═══════════════════════════════════════════════
#  calculate_risk_level
# ═══════════════════════════════════════════════

class TestCalculateRiskLevel:
    """Tests para el cálculo de nivel de riesgo."""

    def test_bajo_for_very_low_value(self, mock_df_hist):
        level = calculate_risk_level(1000, mock_df_hist)
        assert level == "BAJO"

    def test_alto_for_very_high_value(self, mock_df_hist):
        level = calculate_risk_level(999_999, mock_df_hist)
        assert level == "ALTO"

    def test_returns_valid_level(self, mock_df_hist):
        level = calculate_risk_level(65000, mock_df_hist)
        assert level in ("BAJO", "MODERADO", "ALTO")
