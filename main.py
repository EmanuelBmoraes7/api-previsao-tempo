from fastapi import FastAPI
import requests
import psycopg2

app = FastAPI()

# Coordenadas de Palmas - TO
LAT = -10.18
LON = -48.33


# Funcao que conecta no banco de dados Postgres (rodando no Docker)
def conectar():
    return psycopg2.connect(
        host="localhost",
        dbname="previsoes_db",
        user="admin",
        password="admin123"
    )


# Cria a tabela quando a API inicia (se ainda nao existir)
@app.on_event("startup")
def criar_tabela():
    banco = conectar()
    banco.cursor().execute(
        "CREATE TABLE IF NOT EXISTS previsoes (cidade TEXT, temperatura REAL, vento REAL)"
    )
    banco.commit()
    banco.close()


@app.get("/api/previsoes")
def listar():
    banco = conectar()
    cursor = banco.cursor()
    cursor.execute("SELECT cidade, temperatura, vento FROM previsoes")
    linhas = cursor.fetchall()
    banco.close()

    previsoes = []
    for linha in linhas:
        previsoes.append({
            "cidade": linha[0],
            "temperatura": linha[1],
            "vento": linha[2]
        })
    return previsoes


@app.post("/api/previsao")
def adicionar():
    # Busca o tempo atual de Palmas na API gratuita Open-Meteo
    url = "https://api.open-meteo.com/v1/forecast"
    parametros = {
        "latitude": LAT,
        "longitude": LON,
        "current_weather": True
    }
    resposta = requests.get(url, params=parametros)
    dados = resposta.json()

    previsao = {
        "cidade": "Palmas",
        "temperatura": dados["current_weather"]["temperature"],
        "vento": dados["current_weather"]["windspeed"]
    }

    # Salva a previsao no banco de dados
    banco = conectar()
    banco.cursor().execute(
        "INSERT INTO previsoes (cidade, temperatura, vento) VALUES (%s, %s, %s)",
        (previsao["cidade"], previsao["temperatura"], previsao["vento"])
    )
    banco.commit()
    banco.close()

    return previsao