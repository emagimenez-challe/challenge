# Imagen base ligera con Python
FROM python:3.9-slim

# Instala dependencias del sistema para Chrome y Selenium
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    gnupg \
    ca-certificates \
    chromium \
    chromium-driver \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libnss3 \
    libxss1 \
    libgbm-dev \
    libxshmfence1 \
    && rm -rf /var/lib/apt/lists/*

# Variables de entorno para usar Chromium con Selenium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver
ENV PATH="${CHROME_BIN}:${PATH}"

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de la app
COPY requirements.txt . 
COPY scrap.py .
COPY .env .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando final: ejecuta directamente el script
CMD ["python", "scrap.py"]
