"""
Tests de la API — Endpoints de predicción y healthcheck.
Usa httpx TestClient para simular requests sin levantar uvicorn.
"""

import pytest
from fastapi.testclient import TestClient

from backend.main import app


@pytest.fixture
def client():
    """TestClient de FastAPI para los tests."""
    return TestClient(app)


# ═══════════════════════════════════════════════
#  GET / — Healthcheck
# ═══════════════════════════════════════════════

class TestHealthCheck:
    """Tests para el endpoint de healthcheck."""

    def test_health_returns_ok(self, client):
        res = client.get("/")
        assert res.status_code == 200
        data = res.json()
        assert data["estado"] == "OK"
        assert "version" in data
        assert data["mensaje"] == "Servidor de Inteligencia Artificial activo"


# ═══════════════════════════════════════════════
#  POST /predecir — Predicción
# ═══════════════════════════════════════════════

class TestPrediccion:
    """Tests para el endpoint de predicción."""

    def test_prediccion_simple(self, client):
        """Modo simple con valores por defecto."""
        payload = {"ipc": 116.5, "desempleo": 7.2, "covid": 0, "modo_shock": False}
        res = client.post("/predecir", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert "denuncias_estimadas" in data
        assert isinstance(data["denuncias_estimadas"], int)
        assert data["escenario"]["modo"] == "simple"
        assert data["nivel_riesgo"] in ("BAJO", "MODERADO", "ALTO")

    def test_prediccion_shock(self, client):
        """Modo shock con valores extremos."""
        payload = {"ipc": 135.0, "desempleo": 15.0, "covid": 1, "modo_shock": True}
        res = client.post("/predecir", json=payload)
        assert res.status_code == 200
        data = res.json()
        assert data["escenario"]["modo"] == "shock"
        assert isinstance(data["denuncias_estimadas"], int)

    def test_prediccion_valores_minimos(self, client):
        """Valores mínimos permitidos por los schemas."""
        payload = {"ipc": 100.0, "desempleo": 3.0, "covid": 0, "modo_shock": False}
        res = client.post("/predecir", json=payload)
        assert res.status_code == 200

    def test_prediccion_ipc_fuera_de_rango(self, client):
        """IPC fuera de rango debe retornar 422."""
        payload = {"ipc": 50.0, "desempleo": 7.0, "covid": 0, "modo_shock": False}
        res = client.post("/predecir", json=payload)
        assert res.status_code == 422

    def test_prediccion_desempleo_negativo(self, client):
        """Desempleo negativo debe retornar 422."""
        payload = {"ipc": 116.5, "desempleo": -5.0, "covid": 0, "modo_shock": False}
        res = client.post("/predecir", json=payload)
        assert res.status_code == 422

    def test_prediccion_sin_body(self, client):
        """Request sin body debe retornar 422."""
        res = client.post("/predecir")
        assert res.status_code == 422


# ═══════════════════════════════════════════════
#  GET /historico — Datos Históricos
# ═══════════════════════════════════════════════

class TestHistorico:
    """Tests para el endpoint de datos históricos."""

    def test_historico_default(self, client):
        """Obtener últimos 12 meses por defecto."""
        res = client.get("/historico")
        assert res.status_code == 200
        data = res.json()
        assert "datos" in data
        assert "total_registros" in data
        assert len(data["datos"]) <= 12

    def test_historico_custom_meses(self, client):
        """Obtener últimos 6 meses."""
        res = client.get("/historico?ultimos_meses=6")
        assert res.status_code == 200
        data = res.json()
        assert len(data["datos"]) <= 6
