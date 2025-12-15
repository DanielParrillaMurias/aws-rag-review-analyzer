import json
from scraper import scrape_imdb_reviews
from bedrock_analyzer import analyze_reviews


def handler(event, context):
    print("Iniciando ejecución Lambda...")

    # --- ADAPTADOR PARA API GATEWAY ---
    # Si la petición viene de API Gateway, los datos están dentro de 'body' como string
    if 'body' in event:
        try:
            # Parseamos el string JSON que viene en el body
            body_data = json.loads(event['body'])
            movie_url = body_data.get('url')
        except Exception as e:
            print(f"Error parseando el body: {e}")
            return {"statusCode": 400, "body": json.dumps({"message": "JSON inválido en el body"})}
    else:
        # Si viene de la consola de test directa
        movie_url = event.get('url')

    # --- VALIDACIÓN ---
    if not movie_url:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Falta el parámetro 'url'"})
        }

    # --- LÓGICA EXISTENTE ---
    print(f"Procesando URL: {movie_url}")

    reviews = scrape_imdb_reviews(movie_url)
    if not reviews:
        return {"statusCode": 500, "body": json.dumps({"message": "Error obteniendo reseñas"})}

    analysis = analyze_reviews(reviews)
    if not analysis:
        return {"statusCode": 500, "body": json.dumps({"message": "Error en análisis de IA"})}

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json; charset=utf-8"
        },
        "body": json.dumps({
            "message": "Éxito",
            "data": analysis
        }, ensure_ascii=False)  # Para que se vean bien las tildes y caracteres especiales
    }
