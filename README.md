# Jubla Backend API

Backend API para la gestión de eventos Jubla construido con FastAPI y arquitectura hexagonal.

## 🏗️ Arquitectura

Este proyecto sigue la **arquitectura hexagonal** (también conocida como arquitectura de puertos y adaptadores):

```
app/
├── domain/           # Capa de dominio (reglas de negocio)
├── application/      # Capa de aplicación (casos de uso)
├── infrastructure/   # Capa de infraestructura (BD, APIs externas)
├── presentation/     # Capa de presentación (API REST)
└── shared/          # Código compartido
```

## 🚀 Tecnologías

- **Python 3.12**
- **FastAPI** - Framework web
- **Prisma (client para Python)** - ORM/cliente para PostgreSQL
- **PostgreSQL** - Base de datos
- **Redis** - Cache y sesiones
- **Docker** - Containerización

## 📋 Requisitos

- Python 3.12+
- Docker y Docker Compose (para correr el sistema completo)

## 🛠️ Quick start (Docker)

1. Copia y edita el `.env` con credenciales reales:

    ```bash
    cp env.example .env
    # Editar .env y colocar DATABASE_URL, SECRET_KEY, etc.
    ```

2. Construir y levantar todos los servicios:

    ```bash
    docker compose up --build
    ```

3. Accede a la API en http://localhost:8000

Para levantar solo la base de datos y redis (útil en desarrollo local):

```bash
docker compose up db redis -d
```

Y luego ejecutar la app localmente (hot reload):

```bash
uvicorn main:app --reload
```

## 🧭 Prisma (generar cliente para Python)

Este repositorio usa Prisma para definir el esquema y generar un cliente de Python.

Pasos rápidos (desde la raíz del repositorio):

```bash
# Asegúrate de tener DATABASE_URL en .env apuntando a la BD correcta
pip install -r requirements.txt
npx prisma py fetch
npx prisma generate
```

Si necesitas más detalles sobre Prisma (puedes usar Docker si no tienes Node instalado), revisa `PRISMA_SETUP.md`.

## 📚 API Documentation

Una vez ejecutada la aplicación, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔧 Desarrollo

### Formateo de código
```bash
black app/
isort app/
```

### Linting
```bash
flake8 app/
```

### Migraciones de base de datos
```bash
# Crear migración
alembic revision --autogenerate -m "description"

# Aplicar migraciones
alembic upgrade head
```

## 🧪 Testing

```bash
# Ejecutar tests
pytest

# Con coverage
pytest --cov=app
```

## 🚀 Despliegue

### Producción (mínimo)

```bash
# Construir imagen
docker build -t jubla-backend .

# Ejecutar
docker run -p 8000:8000 --env-file .env jubla-backend
```

### Variables de entorno de producción
- `ENVIRONMENT=production`
- `DEBUG=false`
- `SECRET_KEY=<strong-secret-key>`
- `DATABASE_URL=<production-db-url>`

## 📝 Licencia

Este proyecto está bajo la licencia MIT.

## 📧 Envío de correos con Resend

Este proyecto incluye una integración mínima con Resend (https://resend.com) para enviar correos transaccionales.

- Añade tu API key a `.env` (puedes copiar `env.example`):

```bash
RESEND_API_KEY=re_XXXXXXXXXXXX
RESEND_FROM_EMAIL=notifications@yourdomain.com
```

- El servicio está en `app.infrastructure.email.resend_service.ResendService` y se usa de forma "best-effort" al crear reservas.

Notas:
- La librería `httpx` ya figura en `requirements.txt`. Instala dependencias con `pip install -r requirements.txt`.
- Si quieres enviar correos de manera fiable en producción, considera encolar el envío (Celery / BackgroundTasks) y agregar métricas/logs.