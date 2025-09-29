# Analista de Opiniones con IA Generativa (RAG) en AWS

Este proyecto es un pipeline de datos 100% serverless construido en AWS que demuestra habilidades en Ingeniería de la Nube, MLOps e Inteligencia Artificial Generativa. El sistema implementa un patrón de **Retrieval-Augmented Generation (RAG)** para analizar reseñas de productos de e-commerce en tiempo real.

## Descripción General del Proyecto

El objetivo es extraer reseñas de una página de producto, utilizar un Large Language Model (LLM) para generar un análisis de sentimiento y un resumen de "pros y contras", y exponer estos insights a través de una API REST.

Este proyecto sirve como una pieza central de mi portfolio y como una herramienta de aprendizaje práctico para la certificación **AWS Certified Solutions Architect - Associate**.

## Arquitectura de la Solución

El pipeline sigue una arquitectura serverless y orientada a eventos, utilizando los siguientes servicios de AWS:

![Diagrama de Arquitectura (Placeholder)](./images/architecture_diagram.png)
*Un diagrama de la arquitectura se añadirá aquí una vez que los componentes estén definidos.*

1.  **Disparador (Trigger):** Un scheduler de **Amazon EventBridge** invoca el pipeline una vez al día.
2.  **Extracción (Retrieve):** Una función **AWS Lambda** (Python) se activa, realiza web scraping sobre una URL de producto para extraer las reseñas y las almacena temporalmente en un bucket de **Amazon S3**.
3.  **Aumento y Generación (Augment & Generate):** La misma función Lambda formatea las reseñas extraídas para crear un prompt enriquecido. Este prompt se envía a **Amazon Bedrock** (utilizando el modelo Claude 3 Sonnet) para realizar:
    *   Análisis de sentimiento general.
    *   Generación de un resumen de puntos positivos (Pros).
    *   Generación de un resumen de puntos negativos (Contras).
4.  **Persistencia (Storage):** Los insights generados por el LLM se almacenan en una tabla de **Amazon DynamoDB** para un acceso rápido y estructurado.
5.  **Exposición (Exposure):** Una segunda función **AWS Lambda**, actuando como un microservicio, se expone a través de **Amazon API Gateway**. Esto crea un endpoint RESTful (`GET /reviews/{product_id}`) que permite a aplicaciones cliente consultar los análisis almacenados en DynamoDB.

## Stack Tecnológico

*   **Proveedor de Nube:** Amazon Web Services (AWS)
*   **Lenguaje de Programación:** Python
*   **Patrón de IA:** RAG (Retrieval-Augmented Generation)
*   **Servicios Clave de AWS:**
    *   **Computación:** AWS Lambda
    *   **IA Generativa:** Amazon Bedrock (Claude 3 Sonnet)
    *   **Almacenamiento:** Amazon S3, Amazon DynamoDB
    *   **Orquestación:** Amazon EventBridge
    *   **Redes y Exposición:** Amazon API Gateway
*   **Infraestructura como Código (IaC):** Terraform (objetivo final)
*   **Control de Versiones:** Git / GitHub

## Próximos Pasos y Fases del Proyecto

El proyecto se está desarrollando en las siguientes fases:
- [X] **Fase 0: Configuración y Seguridad**
- [ ] **Fase 1: El Scraper (Retrieval)**
- [ ] **Fase 2: La Inteligencia (Augment & Generate)**
- [ ] **Fase 3: La Persistencia (Storage)**
- [ ] **Fase 4: La Exposición (API)**
- [ ] **Fase 5: La Automatización (Orquestación)**
- [ ] **Fase 6: Infraestructura como Código (IaC)**
