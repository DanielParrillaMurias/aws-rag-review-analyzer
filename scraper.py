import requests
from bs4 import BeautifulSoup


def parse_reviews_from_html(html_content):
    """
    Analiza el contenido HTML y extrae las reseñas.
    Esta es la función "pura" que probaremos.
    """
    soup = BeautifulSoup(html_content, 'lxml')

    review_containers = soup.find_all('article', class_='user-review-item')
    if not review_containers:
        return []

    reviews = []
    for container in review_containers:
        review_div = container.find('div', class_='ipc-html-content-inner-div')
        if review_div:
            review_text = review_div.text
            reviews.append(review_text.strip())

    return reviews


def scrape_imdb_reviews(url):
    """
    Obtiene el HTML de la URL de IMDb y usa la función de parseo para extraer las reseñas.
    Esta función se encarga de la parte "impura" (la llamada de red).
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Llama a nuestra función pura y testeable
        return parse_reviews_from_html(response.text)

    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la petición HTTP: {e}")
        return None
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        return None


# El bloque principal ahora usa la función de alto nivel
if __name__ == "__main__":
    movie_url = "https://www.imdb.com/title/tt0068646/reviews"
    extracted_reviews = scrape_imdb_reviews(movie_url)

    if extracted_reviews:
        print(f"\n--- {len(extracted_reviews)} Reseñas Extraídas de IMDb ---")
        # ... (el resto del código de impresión es el mismo)
