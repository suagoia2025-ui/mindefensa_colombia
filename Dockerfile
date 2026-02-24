# API FastAPI - Análisis Seguridad Colombia
FROM python:3.12-slim

WORKDIR /app

# Dependencias del sistema (opcional, para compilación de paquetes)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/
# Datos: se montan por volumen en docker-compose; aquí creamos el directorio
RUN mkdir -p /app/data/processed

ENV PYTHONPATH=/app
EXPOSE 8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
