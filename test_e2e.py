from fastapi.testclient import TestClient
import main

cliente = TestClient(main.app)


# Teste E2E (ponta a ponta): testa o fluxo completo de verdade.
# IMPORTANTE: precisa do banco rodando no Docker (docker compose up -d).
# 1) Faz um POST que busca o tempo real e salva no banco.
# 2) Faz um GET e confere se a previsao salva aparece na lista.
def test_fluxo_completo():
    # Passo 1: salva uma previsao
    resposta_post = cliente.post("/api/previsao")
    assert resposta_post.status_code == 200

    previsao_salva = resposta_post.json()
    assert previsao_salva["cidade"] == "Palmas"

    # Passo 2: lista e confere que existe pelo menos uma previsao de Palmas
    resposta_get = cliente.get("/api/previsoes")
    assert resposta_get.status_code == 200

    lista = resposta_get.json()
    assert len(lista) >= 1
    assert lista[-1]["cidade"] == "Palmas"
