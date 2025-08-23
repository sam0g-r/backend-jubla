# ---- Final Stage ----
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
# Asegura que prisma-client-py descargue el binario correcto en Debian slim
ENV PRISMA_CLI_QUERY_ENGINE_BINARY_TARGETS=debian-openssl-3.0.x

# Configurar el cache de Prisma en un directorio accesible
ENV PRISMA_CLIENT_ENGINE_BINARY_CACHE_DIR=/app/.cache

WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Actualizar pip
RUN python -m pip install --upgrade pip

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código de la aplicación (incluye schema.prisma)
COPY . .

# Crear directorio de cache accesible para Prisma
RUN mkdir -p /app/.cache

# Generar el cliente Prisma en Python
RUN python -m prisma generate

# Crear usuario no root por seguridad
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Comando de arranque: aplicar migraciones (si no las aplicaste en build) y levantar uvicorn
CMD ["sh", "-c", "python -m prisma migrate deploy && uvicorn main:app --host 0.0.0.0 --port 8000"]
