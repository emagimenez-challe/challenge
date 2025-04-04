#!/bin/bash

# Cargar variables de entorno
source .env

# Validar variables obligatorias
if [[ -z "$PROJECT_ID" || -z "$REGION" || -z "$SERVICE_NAME" || -z "$REPO_NAME" || -z "$IMAGE_NAME" || -z "$GOOGLE_APPLICATION_CREDENTIALS_JSON" ]]; then
    echo "Faltan variables requeridas en el .env. Verifica PROJECT_ID, REGION, SERVICE_NAME, REPO_NAME, IMAGE_NAME, y GOOGLE_APPLICATION_CREDENTIALS_JSON"
    exit 1
fi

# Autenticarse en gcloud
gcloud config set project "$PROJECT_ID"

# Crear repositorio si no existe
gcloud artifacts repositories describe "$REPO_NAME" --location="$REGION" 2>/dev/null || \
gcloud artifacts repositories create "$REPO_NAME" \
  --repository-format=docker \
  --location="$REGION" \
  --description="Repositorio para scraper"

# Build de imagen Docker
IMAGE_URI="$REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME:$TAG"
docker build -t "$IMAGE_URI" .

# Subir imagen a Artifact Registry
docker push "$IMAGE_URI"

# Desplegar en Cloud Run
gcloud run deploy "$SERVICE_NAME" \
  --image="$IMAGE_URI" \
  --region="$REGION" \
  --platform=managed \
  --allow-unauthenticated \
  --set-env-vars=PROJECT_ID=$PROJECT_ID,DATASET_ID=$DATASET_ID,TABLE_ID=$TABLE_ID,GOOGLE_APPLICATION_CREDENTIALS_JSON=$GOOGLE_APPLICATION_CREDENTIALS_JSON

echo "Completo"
