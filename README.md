# Proyecto: API y Lambda para Procesamiento de Datos de Cine

Este proyecto implementa una infraestructura basada en Lambda y FastAPI para el procesamiento y análisis de datos de cine extraídos desde archivos JSON almacenados en Amazon S3. La solución permite limpiar, transformar y consultar datos procesados en diferentes formatos (JSON y CSV).

## Tecnologías utilizadas

- **AWS Lambda**: Función para la limpieza y transformación de datos.
- **Amazon S3**: Almacenamiento de archivos JSON y CSV.
- **FastAPI**: API para la consulta de datos procesados.
- **Pandas**: Manipulación y procesamiento de datos.
- **Boto3**: Interacción con AWS S3.

## Estructura del proyecto

```
APILambdas/
│── app/
│   ├── main.py  # Definición de la API con FastAPI
│   ├── utils.py  # Funciones auxiliares
│   ├── module_data/
│   │   ├── data.py  # Funciones para obtener datos de S3
│── lambda_movies_data_clean.py  # Script Lambda para limpieza y transformación
│── README.md  # Documentación del proyecto
```

## Descripción de los archivos principales

### 1. Lambda: `lambda_movies_data_clean.py`

Esta función se activa cuando un archivo JSON es subido a un bucket de S3. Su objetivo es:

- Extraer datos del JSON.
- Normalizar los datos y rellenar valores nulos.
- Extraer información de fecha y hora.
- Guardar los datos procesados en otro bucket en formato CSV.

### 2. API: `main.py`

Expone diferentes endpoints para consultar los datos procesados:

- `/` → Prueba de conexión.
- `/data` → Devuelve los datos originales.
- `/data/resume` → Devuelve los datos procesados en formato JSON.
- `/data/processed/{year}/{month}/{day}` → Devuelve los datos de un día específico en formato JSON.

### 3. Módulo de datos: `data.py`

Define funciones auxiliares para interactuar con los archivos en S3, permitiendo obtener datos tanto en formato JSON como CSV.

### 4. Utilidades: `utils.py`

Contiene funciones auxiliares, como `generate_file_path()`, que genera rutas dinámicas para los archivos procesados en S3.



Este proyecto facilita el procesamiento automatizado de datos de cine en AWS, permitiendo una rápida consulta y análisis de información mediante una API.

