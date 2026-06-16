from fastapi import FastAPI
import requests

app = FastAPI()

# Lista que guarda as previsoes na memoria
previsoes = []

# Coordenadas de Palmas - TO
LAT = -10.18
LON = -48.33


@app.get("/api/previsoes")
def listar():
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

    previsoes.append(previsao)
    return previsao