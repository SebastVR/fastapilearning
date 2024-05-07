# pull official base image
# FROM python:3.12-slim
FROM python:3.11.4-slim

# Se establece el directorio de trabajo en el contenedor
WORKDIR /app

# Instalar dependencias del sistema para psycopg2
RUN apt-get update && apt-get install -y \
    poppler-utils \
    ghostscript \
    tesseract-ocr \
    tesseract-ocr-eng \
    libtesseract-dev \
    libpq-dev \
    gcc \
    libgl1-mesa-dev \ 
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Se copian el archivo de requisitos en el contenedor
COPY requirements.txt /app


RUN pip install --no-cache-dir -r requirements.txt
# Se copian los archivos restantes en el contenedor
COPY . .

# Copia y otorga permisos al script de entrypoint
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh
# Se expone el puerto en el que se ejecutará la aplicación
EXPOSE 80

# Se establece comando para ejecutar la aplicación FastAPI con Uvicorn
# ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]