from fastapi.testclient import TestClient
import main

cliente = TestClient(main.app)


# Teste E2E (ponta a ponta): testa o fluxo completo de verdade.
# IMPORTANTE: precisa do banco rodando (Docker localmente, ou o Postgres do CI).
# Antes de tudo, garante que a tabela existe chamando criar_tabela().
def test_fluxo_completo():
    # Garante que a tabela "previsoes" existe no banco
    main.criar_tabela()

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
