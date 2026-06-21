from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import main

cliente = TestClient(main.app)


# Testa o GET /api/previsoes usando um banco "de mentira" (mock)
@patch("main.conectar")
def test_listar(conectar_falso):
    # Faz o banco falso devolver uma previsao pronta
    banco = MagicMock()
    banco.cursor().fetchall.return_value = [("Palmas", 25.0, 3.2)]
    conectar_falso.return_value = banco

    # Chama a rota
    resposta = cliente.get("/api/previsoes")

    # Confere se deu certo (status 200) e se devolveu a previsao
    assert resposta.status_code == 200
    assert resposta.json() == [{"cidade": "Palmas", "temperatura": 25.0, "vento": 3.2}]