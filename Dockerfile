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

# Instala el CLI de Prisma globalmente (opcional, pero útil)
RUN npm install -g prisma

# Copiar código de la aplicación
COPY . .

# Crear usuario no-root y ajustar permisos
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]