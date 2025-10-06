import json
from unittest.mock import MagicMock
from bedrock_analyzer import analyze_reviews

# Datos de entrada de prueba para nuestra función
SAMPLE_REVIEWS = [
    "¡Una obra maestra absoluta! La dirección y las actuaciones son de otro nivel.",
    "Me pareció un poco lenta y sobrevalorada. No es para todo el mundo.",
    "Visualmente impresionante, con una historia que te atrapa. La mejor película del año."
]

# Esta es la respuesta que *simularemos* que Bedrock nos devuelve.
# La estructura imita la respuesta real de la API de Bedrock para Claude 3.
MOCK_BEDROCK_RESPONSE = {
    "body": MagicMock(
        read=lambda: json.dumps({
            "content": [
                {
                    "type": "text",
                    "text": json.dumps({
                        "sentiment": "Positivo",
                        "summary": "La mayoría de las opiniones son muy positivas, elogiando la dirección y las actuaciones.",
                        "pros": ["Dirección excepcional", "Actuaciones memorables"],
                        "cons": ["Puede ser lenta para algunos espectadores"]
                    })
                }
            ]
        }).encode('utf-8')
    )
}


def test_analyze_reviews_success(mocker):
    """
    Prueba la función analyze_reviews en un escenario de éxito,
    "mockeando" (simulando) la llamada a la API de Bedrock.
    """
    # --- Preparación (Arrange) ---

    # Aquí está la magia del mocking. `mocker.patch` intercepta todas las llamadas
    # a 'bedrock_analyzer.bedrock_client.invoke_model'.
    # En lugar de hacer la llamada real, hará que devuelva nuestro objeto simulado.
    mock_invoke_model = mocker.patch(
        'bedrock_analyzer.bedrock_client.invoke_model',
        return_value=MOCK_BEDROCK_RESPONSE
    )

    # --- Acción (Act) ---

    # Llamamos a nuestra función. Internamente, cuando intente llamar a
    # bedrock_client.invoke_model, se ejecutará nuestro mock en su lugar.
    result = analyze_reviews(SAMPLE_REVIEWS)

    # --- Aserción (Assert) ---

    # 1. Verificamos que la llamada a la API se hizo una vez.
    mock_invoke_model.assert_called_once()

    # 2. Verificamos que el resultado de nuestra función es el que esperamos.
    #    Nuestra función debe haber parseado correctamente la respuesta simulada.
    assert result is not None
    assert result["sentiment"] == "Positivo"
    assert "Dirección excepcional" in result["pros"]
    assert "Puede ser lenta para algunos espectadores" in result["cons"]


def test_analyze_reviews_api_error(mocker):
    """
    Prueba cómo se comporta la función analyze_reviews si la API de Bedrock falla.
    """
    # --- Preparación (Arrange) ---

    # Esta vez, configuramos el mock para que, en lugar de devolver un valor,
    # lance una excepción, simulando un error de red o de la API.
    mocker.patch(
        'bedrock_analyzer.bedrock_client.invoke_model',
        side_effect=Exception("AWS API Error")
    )

    # --- Acción (Act) ---
    result = analyze_reviews(SAMPLE_REVIEWS)

    # --- Aserción (Assert) ---
    # Verificamos que nuestra función manejó el error correctamente y devolvió None.
    assert result is None
