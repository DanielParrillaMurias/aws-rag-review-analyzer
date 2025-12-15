import boto3
import json
import re

# Inicializamos el cliente
bedrock_client = boto3.client(
    service_name="bedrock-runtime", region_name="eu-west-1")
MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"


def clean_json_output(text):
    """
    Limpia la respuesta del LLM para extraer solo el JSON válido.
    Elimina etiquetas Markdown como ```json ... ``` y texto introductorio.
    """
    # Buscar contenido entre etiquetas de código ```json ... ``` o ``` ... ```
    pattern = r"```(?:json)?\s*(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # Si no hay etiquetas, intentamos encontrar el primer '{' y el último '}'
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1:
        return text[start:end+1]

    return text.strip()


def analyze_reviews(reviews):
    print(f"Iniciando análisis con Bedrock para {len(reviews)} reseñas.")

    reviews_text = "\n".join(
        f"<review>{review}</review>" for review in reviews)

    prompt = f"""
        Human: Eres un experto analista. Analiza las siguientes reseñas de películas dentro de <reviews>.
        Genera una respuesta EXCLUSIVAMENTE en formato JSON válido.
        No incluyas texto introductorio ni explicaciones fuera del JSON.
        
        El formato debe ser:
        {{
            "sentiment": "Positivo/Negativo/Mixto",
            "summary": "Resumen breve",
            "pros": ["pro1", "pro2"],
            "cons": ["con1", "con2"]
        }}

        <reviews>
        {reviews_text}
        </reviews>

        Assistant: {{
    """
    # Truco: Pre-llenamos el inicio del JSON "{" en el prompt para forzar a Claude a seguir el formato.

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
        response = bedrock_client.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(request_body),
        )

        response_body_raw = response["body"].read()
        response_body = json.loads(response_body_raw)

        raw_analysis_text = response_body["content"][0]["text"]

        print(f"DEBUG - Respuesta cruda de Bedrock: {raw_analysis_text}")

        full_text = raw_analysis_text.strip()
        if not full_text.startswith("{"):
            full_text = "{" + full_text

        # Limpieza básica
        cleaned_text = clean_json_output(full_text)

        # --- CORRECCIÓN ROBUSTA AQUÍ ---
        try:
            # Intentamos leerlo normal
            return json.loads(cleaned_text)
        except json.JSONDecodeError as e:
            # Si falla porque hay "Extra data" (basura al final), usamos raw_decode
            # raw_decode lee hasta donde es válido y para.
            if "Extra data" in e.msg:
                print(
                    "DEBUG - Detectado 'Extra data' (posible llave duplicada), recuperando JSON válido...")
                obj, _ = json.JSONDecoder().raw_decode(cleaned_text)
                return obj
            else:
                # Si es otro error, que falle
                raise e

    except Exception as e:
        print(f"Error CRÍTICO en analyze_reviews: {e}")
        return None
