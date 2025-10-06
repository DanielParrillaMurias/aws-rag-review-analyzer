import json
from scraper import scrape_imdb_reviews
from bedrock_analyzer import analyze_reviews


def handler(event, context):
    """
    Orquesta el proceso: Scrape -> Analyze -> Respond.
    """
    print("Iniciando la ejecución de la función Lambda.")

    movie_url = event.get('url')
    if not movie_url:
        print("Error: No se proporcionó ninguna 'url' en el evento de entrada.")
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "El parámetro 'url' es requerido."})
        }

    # --- PASO 1: RETRIEVE (Recuperar) ---
    print(f"Scrapeando la URL: {movie_url}")
    reviews = scrape_imdb_reviews(movie_url)

    if reviews is None or not reviews:
        print("El scraping falló o no se encontraron reseñas.")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "No se pudieron obtener las reseñas."})
        }

    print(f"Scraping exitoso. Se encontraron {len(reviews)} reseñas.")

    # --- PASO 2: AUGMENT & GENERATE (Aumentar y Generar) ---
    analysis_result = analyze_reviews(reviews)

    if analysis_result is None:
        print("El análisis con Bedrock falló.")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Ocurrió un error durante el análisis de IA."})
        }

    # --- PASO 3: RESPONDER ---
    print("Proceso completado con éxito.")
    response = {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Análisis completado con éxito",
            "source_url": movie_url,
            "analysis": analysis_result  # <-- DEVOLVEMOS EL ANÁLISIS DE BEDROCK
        })
    }

    return response
