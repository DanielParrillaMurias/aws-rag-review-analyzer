import pytest
from scraper import parse_reviews_from_html  # Importamos solo la función pura


def load_test_html():
    """Función auxiliar para cargar nuestro archivo HTML de prueba."""
    with open("test_data/imdb_reviews_fixture.html", "r", encoding="utf-8") as f:
        return f.read()


def test_parse_reviews_from_html():
    """
    Prueba la lógica de parseo con datos locales.
    Esta prueba no hace ninguna llamada a internet.
    """
    # 1. Preparación (Arrange)
    html_content = load_test_html()

    # 2. Acción (Act)
    reviews = parse_reviews_from_html(html_content)

    # 3. Aserción (Assert) - Verificamos que el resultado es el esperado
    assert isinstance(reviews, list)
    assert len(reviews) == 15  # IMDb suele mostrar 15 reseñas por página

    # Verificamos que el contenido de la primera reseña es el que esperamos
    assert "It is now past 1 PM and I just finished watching Francis Ford Coppola" in reviews[0]
    # Verificamos que el contenido de la última reseña es el que esperamos
    assert "The directing by Coppola was perfect as well." in reviews[-1]
