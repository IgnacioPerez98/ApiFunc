import logging
import os
import requests
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Procesando solicitud de noticias...")

    # API Key desde Application Settings
    api_key = os.environ.get("NEWS_API_KEY")
    if not api_key:
        return func.HttpResponse("Falta NEWS_API_KEY", status_code=500)

    # Construir URL de NewsAPI
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)

    if response.status_code != 200:
        return func.HttpResponse(
            f"Error al obtener noticias: {response.text}", 
            status_code=response.status_code
        )

    data = response.json()
    # Devolver solo títulos
    headlines = [article["title"] for article in data.get("articles", [])]

    return func.HttpResponse(
        body=str({"headlines": headlines}),
        status_code=200,
        mimetype="application/json"
    )
