# Usar la imagen base oficial de AWS para Python 3.12 en arquitectura ARM64
FROM public.ecr.aws/lambda/python:3.12-arm64

# Copiar el archivo de requerimientos al directorio de trabajo de la imagen
COPY requirements.txt .

# Instalar las dependencias de Python desde el archivo de requerimientos
RUN pip install -r requirements.txt

# Copiar nuestro código fuente de la aplicación a la imagen
COPY scraper.py .
COPY lambda_handler.py .
COPY bedrock_analyzer.py .

# Definir el comando que Lambda ejecutará cuando se inicie el contenedor.
CMD [ "lambda_handler.handler" ]