import json
from scraper import scrape_imdb_reviews


def handler(event, context):
    """
    Punto de entrada para la ejecución de AWS Lambda.
    Extrae una URL del evento de entrada, la scrapea y devuelve las reseñas.
    """
    print("Iniciando la ejecución de la función Lambda.")

    # --- CAMBIO CLAVE: Obtener la URL del evento de entrada ---
    # Usamos event.get('url') para evitar un error si la clave 'url' no existe.
    movie_url = event.get('url')

    # --- NUEVO: Añadir validación de la entrada ---
    if not movie_url:
        print("Error: No se proporcionó ninguna 'url' en el evento de entrada.")
        return {
            "statusCode": 400,  # 400 Bad Request es el código correcto para un error del cliente
            "body": json.dumps({
                "message": "El parámetro 'url' es requerido en el evento de entrada."
            })
        }

    print(f"Scrapeando la URL: {movie_url}")
    reviews = scrape_imdb_reviews(movie_url)

    if reviews is not None:
        print(f"Scraping exitoso. Se encontraron {len(reviews)} reseñas.")
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Reseñas extraídas con éxito",
                "source_url": movie_url,  # Buena práctica: devolver la fuente que se procesó
                "review_count": len(reviews),
                # Devolvemos solo las 5 primeras para no hacer la respuesta demasiado grande
                "reviews": reviews[:5]
            })
        }
    else:
        print("El scraping falló.")
        response = {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Ocurrió un error durante el scraping.",
                "source_url": movie_url
            })
        }

    print("Finalizando la ejecución de la función Lambda.")
    return response
