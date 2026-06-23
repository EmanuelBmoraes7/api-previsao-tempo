from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import main

cliente = TestClient(main.app)


# Teste usado tambem pela ferramenta de mutacao.
# Testa a rota POST /api/previsao com mocks (sem banco, sem internet),
# conferindo cada valor para "pegar" possiveis mutacoes no codigo.
@patch("main.conectar")
@patch("main.requests.get")
def test_adicionar(get_falso, conectar_falso):
    # Finge a resposta da Open-Meteo
    resposta_meteo = MagicMock()
    resposta_meteo.json.return_value = {
        "current_weather": {"temperature": 30.5, "windspeed": 10.0}
    }
    get_falso.return_value = resposta_meteo

    # Finge o banco de dados
    conectar_falso.return_value = MagicMock()

    resposta = cliente.post("/api/previsao")

    assert resposta.status_code == 200
    assert resposta.json()["cidade"] == "Palmas"
    assert resposta.json()["temperatura"] == 30.5
    assert resposta.json()["vento"] == 10.0
