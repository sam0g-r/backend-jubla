# ---- Builder Stage ----
# This stage installs node, npm dependencies, and generates the prisma client.
FROM node:18-slim as builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install JS dependencies (including prisma CLI)
RUN npm install

# Copy prisma schema
COPY prisma ./prisma/

# Generate the Prisma client. This is the memory-intensive step.
# The output path is now explicitly configured in schema.prisma.
RUN npx prisma generate

# ---- Final Stage ----
# This is the final, lean production image.
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
# This environment variable ensures that prisma-client-py downloads the correct
# binary for the Debian-based slim image.
ENV PRISMA_CLI_QUERY_ENGINE_BINARY_TARGETS=debian-openssl-3.0.x

WORKDIR /app

# Install runtime system dependencies.
# postgresql-client is needed for psycopg2 to connect to PostgreSQL.
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install Python dependencies from requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Copy the pre-generated Prisma client from the builder stage.
COPY --from=builder /app/app/infrastructure/database/prisma_client.py ./app/infrastructure/database/prisma_client.py

# Create a non-root user for security.
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser \
    && chown -R appuser:appuser /app

# Switch to the non-root user.
USER appuser

EXPOSE 8000

# The command to run the application.
# We first apply any pending database migrations and then start the uvicorn server.
# We use `python -m prisma` which is available from the `prisma-client-py` package.
# This avoids needing Node.js in the final image.
CMD ["sh", "-c", "python -m prisma migrate deploy && uvicorn main:app --host 0.0.0.0 --port 8000"]
