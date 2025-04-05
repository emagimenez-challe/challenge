# challenge

#### Se adjuntará una muestra de la tabla creada y cargada en GCP 

Prepara el archivo .env

Edita el archivo .env con tus valores:
# Archivo .env  ¡¡¡¡Editar antes de desplegar!!!!!!

# GCP Project ID
PROJECT_ID=tu-project-id

# Región (ejemplo: us-central1, southamerica-east1)
REGION=southamerica-east1

# Nombre del servicio en Cloud Run
SERVICE_NAME=scraper-service

# Nombre del repositorio en Artifact Registry
REPO_NAME=scraper-repo

# Nombre y etiqueta de la imagen Docker
IMAGE_NAME=scraper-bq
TAG=latest

# === Scraper / BigQuery ===
GOOGLE_APPLICATION_CREDENTIALS_JSON=  # Contenido codificado en base64
DATASET_ID=tu_dataset
TABLE_ID=tu_tabla

Para generar el contenido en base64 de tu archivo de credenciales:

base64 credenciales.json
Luego, copia y pega el resultado en la variable GOOGLE_APPLICATION_CREDENTIALS_JSON.


#### Despliegue

1. Ejecuta el script de despliegue
chmod +x deploy.sh
./deploy.sh
### Recuerde haber rellenado el archivo .env con las variables solicitadas###

Que hace este deploy?
A.  Construye la imagen Docker
B.  La sube a Artifact Registry
C.  La despliega en Cloud Run


### Docker

### Detalles del Dockerfile:
Usa Python 3.9

Instala Chrome y ChromeDriver para Selenium

Instala las dependencias desde requirements.txt

Decodifica las credenciales base64 a credenciales.json


### Requisitos:

Proyecto en Google Cloud

Artifact Registry habilitado

Cloud Run habilitado

Dataset y tabla en BigQuery

Cuenta de servicio con permisos para BigQuery y Cloud Run



### Tecnologías utilizadas:

Python 3.9

Selenium 4.30.0

Google Cloud SDK

Docker

BigQuery / pandas-gbq


