FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema necesarias para compilar paquetes nativos
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    postgresql-client

# Actualizar pip
RUN python -m pip install --upgrade pip

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && apt-get purge -y --auto-remove build-essential gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala Node.js y npm (necesario para Prisma)
RUN apt-get update && apt-get install -y npm && rm -rf /var/lib/apt/lists/*

#Copia los package
COPY package*.json ./

# Instala el CLI
RUN npm install

# Copiar código de la aplicación
COPY . .

# Limitar paralelismo
ENV PRISMA_CLI_QUERY_ENGINE_BINARY_TARGETS=debian-openssl-3.0.x
ENV PRISMA_CLI_ENGINE_TYPE=binary

# Generate models
RUN npx prisma generate --no-engine

# Crear usuario no-root y ajustar permisos
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["sh", "-c", "npx prisma generate && npx prisma migrate deploy && uvicorn main:app --host 0.0.0.0 --port 8000"]
