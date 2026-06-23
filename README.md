# API de Previsão do Tempo em Palmas

API REST construída com **FastAPI** que busca a previsão do tempo atual de Palmas (TO) na API gratuita [Open-Meteo](https://open-meteo.com/) e salva os resultados em um banco de dados **PostgreSQL** rodando em um container **Docker**. O projeto conta com testes automatizados (unitário, end-to-end e de mutação) e uma esteira de **Integração Contínua (CI)** com GitHub Actions.

## Tecnologias

- Python 3.12
- FastAPI
- Uvicorn
- Requests
- PostgreSQL (via Docker)
- psycopg2
- pytest
- GitHub Actions (CI)

## Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET`  | `/api/previsoes` | Lista todas as previsões salvas no banco |
| `POST` | `/api/previsao`  | Busca o clima atual de Palmas e salva uma nova previsão |

## Como rodar

### 1. Suba o banco de dados (Docker)

Com o Docker Desktop aberto, suba o PostgreSQL:

```bash
docker compose up -d
```

### 2. Prepare o ambiente Python

```bash
# Crie e ative o ambiente virtual
python -m venv .venv
source .venv/Scripts/activate   # Windows (Git Bash)
# source .venv/bin/activate     # Linux/Mac

# Instale as dependências
pip install -r requirements.txt
```

### 3. Rode a aplicação

```bash
uvicorn main:app --reload
```

Acesse a documentação interativa em: **http://127.0.0.1:8000/docs**

## Como testar (Swagger)

1. Em `/docs`, clique no **POST /api/previsao** → "Try it out" → "Execute". A API busca a temperatura e o vento atuais de Palmas e salva no banco.
2. Clique no **GET /api/previsoes** → "Try it out" → "Execute" para ver todas as previsões salvas.

Como os dados ficam no PostgreSQL, eles permanecem salvos mesmo após reiniciar o servidor.

## Testes automatizados

O projeto possui três tipos de teste:

| Arquivo | Tipo | Descrição |
|---------|------|-----------|
| `test_unitario.py` | Unitário | Testa a rota GET isoladamente usando mock (sem banco/internet) |
| `test_e2e.py` | End-to-end | Testa o fluxo completo de verdade (precisa do banco ligado) |
| `test_mutacao.py` | Mutação | Testa a rota POST com mock; usado pela ferramenta mutmut |

```bash
# Instale as ferramentas de teste (já incluídas no requirements.txt)
pip install pytest httpx

# Rode todos os testes (suba o banco antes para o E2E passar)
python -m pytest -v

# Teste de mutação
pip install mutmut
mutmut run --paths-to-mutate main.py
mutmut results
```

## Integração Contínua (CI)

A cada `push` ou `pull request` na branch `main`, o **GitHub Actions** executa automaticamente todos os testes em um ambiente Linux, subindo um banco PostgreSQL temporário. A configuração está em `.github/workflows/ci.yml`. O resultado pode ser acompanhado na aba **Actions** do repositório.

## Comandos úteis do Docker

```bash
docker compose up -d     # Sobe o banco
docker compose down      # Desliga o banco
docker ps                # Lista containers rodando
```

## Estrutura do projeto

```
APIprevisaodotempo/
├── .github/workflows/ci.yml   # Esteira de CI
├── main.py                    # Código da API
├── requirements.txt           # Dependências
├── docker-compose.yml         # Configuração do banco no Docker
├── test_unitario.py           # Teste unitário
├── test_e2e.py                # Teste end-to-end
└── test_mutacao.py            # Teste de mutação
```

## Autor

**Emanuel Borges Moraes**
[github.com/EmanuelBmoraes7](https://github.com/EmanuelBmoraes7)
