from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import main

cliente = TestClient(main.app)


# Teste UNITARIO: testa a rota GET /api/previsoes isolada, usando um banco "de mentira" (mock).
# Nao precisa do Docker nem de internet.
@patch("main.conectar")
def test_listar(conectar_falso):
    banco = MagicMock()
    banco.cursor().fetchall.return_value = [("Palmas", 25.0, 3.2)]
    conectar_falso.return_value = banco

    resposta = cliente.get("/api/previsoes")

    assert resposta.status_code == 200
    assert resposta.json() == [{"cidade": "Palmas", "temperatura": 25.0, "vento": 3.2}]
