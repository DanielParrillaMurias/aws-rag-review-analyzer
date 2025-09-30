import json
from scraper import scrape_imdb_reviews  # Importamos nuestra función probada


def handler(event, context):
    """
    Punto de entrada para la ejecución de AWS Lambda.
    """
    print("Iniciando la ejecución de la función Lambda.")

    # En una aplicación real, esta URL podría venir del objeto 'event'
    movie_url = "https://www.imdb.com/title/tt0068646/reviews"

    print(f"Scrapeando la URL: {movie_url}")
    reviews = scrape_imdb_reviews(movie_url)

    if reviews is not None:
        print(f"Scraping exitoso. Se encontraron {len(reviews)} reseñas.")
        # La respuesta de una Lambda que se integra con API Gateway
        # debe tener este formato. Es una buena práctica adoptarlo siempre.
        response = {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Reseñas extraídas con éxito",
                "review_count": len(reviews),
                "reviews": reviews
            })
        }
    else:
        print("El scraping falló.")
        response = {
            "statusCode": 500,
            "body": json.dumps({
                "message": "Ocurrió un error durante el scraping."
            })
        }

    print("Finalizando la ejecución de la función Lambda.")
    return response
