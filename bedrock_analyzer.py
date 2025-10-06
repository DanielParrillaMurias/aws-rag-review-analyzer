import boto3
import json

# Inicializamos el cliente de Bedrock fuera del handler para reutilizar la conexión
# Es una mejor práctica para el rendimiento en Lambda
bedrock_client = boto3.client(
    service_name="bedrock-runtime", region_name="eu-west-1")

MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"


def analyze_reviews(reviews):
    """
    Analiza una lista de reseñas usando Amazon Bedrock con Claude 3 Sonnet.
    """
    print(f"Iniciando análisis con Bedrock para {len(reviews)} reseñas.")

    # Unimos las reseñas en un solo bloque de texto para el prompt
    reviews_text = "\n".join(
        f"<review>{review}</review>" for review in reviews)

    # --- Prompt Engineering ---
    # Este es el prompt que le daremos al modelo.
    # Usamos etiquetas XML para delimitar claramente las secciones.
    # Le pedimos explícitamente una salida en formato JSON.
    prompt = f"""
        Human: Eres un experto analista de opiniones de clientes. Te he proporcionado una serie de reseñas de una película entre etiquetas <reviews>.
        Tu tarea es realizar un análisis de sentimiento y resumir los puntos clave.
        Por favor, analiza todas las reseñas en conjunto y proporciona una respuesta en formato JSON con las siguientes claves:
        - "sentiment": Un valor que puede ser "Positivo", "Negativo" o "Mixto".
        - "summary": Un resumen conciso de 2-3 frases sobre la opinión general de la película.
        - "pros": Una lista de 3 a 5 puntos positivos clave mencionados en las reseñas.
        - "cons": Una lista de 3 a 5 puntos negativos clave mencionados en las reseñas.

        <reviews>
        {reviews_text}
        </reviews>

        Assistant:
    """

    # --- Construcción del Payload para Bedrock (específico de Claude 3) ---
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2048,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}],
            }
        ],
    }

    try:
        # --- Invocación del Modelo ---
        response = bedrock_client.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(request_body),
        )

        # --- Procesamiento de la Respuesta ---
        response_body_raw = response["body"].read()
        response_body = json.loads(response_body_raw)

        # La respuesta de Claude 3 está dentro de una estructura anidada
        analysis_text = response_body["content"][0]["text"]

        print("Análisis de Bedrock recibido con éxito.")
        # Convertimos el texto de la respuesta (que debería ser un JSON) en un diccionario de Python
        return json.loads(analysis_text)

    except Exception as e:
        print(f"Error al invocar el modelo de Bedrock: {e}")
        return None
