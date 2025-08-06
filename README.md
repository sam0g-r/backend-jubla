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
- **SQLAlchemy** - ORM
- **PostgreSQL** - Base de datos
- **Redis** - Cache y sesiones
- **JWT** - Autenticación
- **Docker** - Containerización

## 📋 Requisitos

- Python 3.12+
- Docker y Docker Compose
- PostgreSQL
- Redis

## 🛠️ Instalación

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd backend-jubla
```

### 2. Configurar variables de entorno
```bash
cp env.example .env
# Editar .env con tus configuraciones
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar con Docker (recomendado)
```bash
docker-compose up --build
```

### 5. Ejecutar localmente
```bash
# Iniciar PostgreSQL y Redis
docker-compose up db redis -d

# Ejecutar la aplicación
uvicorn main:app --reload
```

## 📚 API Documentation

Una vez ejecutada la aplicación, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 🔐 Autenticación

La API usa JWT para autenticación. Los endpoints protegidos requieren el header:

```
Authorization: Bearer <token>
```

## 🌐 Endpoints Principales

### Usuarios
- `POST /api/v1/users/` - Crear usuario
- `GET /api/v1/users/{user_id}` - Obtener usuario
- `PUT /api/v1/users/{user_id}` - Actualizar usuario
- `DELETE /api/v1/users/{user_id}` - Eliminar usuario
- `GET /api/v1/users/` - Listar usuarios

### Eventos
- `GET /api/v1/events/` - Listar eventos activos
- `GET /api/v1/events/{slug}` - Obtener evento por slug
- `POST /api/v1/events/` - Crear evento
- `PUT /api/v1/events/{event_id}` - Actualizar evento
- `DELETE /api/v1/events/{event_id}` - Eliminar evento

## 🧪 Testing

```bash
# Ejecutar tests
pytest

# Con coverage
pytest --cov=app

# Tests específicos
pytest tests/test_users.py
```

## 📦 Estructura del Proyecto

```
backend-jubla/
├── app/
│   ├── domain/              # Entidades y reglas de negocio
│   ├── application/         # Casos de uso
│   ├── infrastructure/      # Implementaciones de repositorios
│   ├── presentation/        # API REST
│   └── shared/             # Configuración y utilidades
├── tests/                  # Tests unitarios e integración
├── alembic/               # Migraciones de BD
├── requirements.txt        # Dependencias Python
├── Dockerfile             # Configuración Docker
├── docker-compose.yml     # Orquestación de servicios
└── main.py               # Punto de entrada
```

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

## 🚀 Despliegue

### Producción
```bash
# Construir imagen
docker build -t jubla-backend .

# Ejecutar
docker run -p 8000:8000 jubla-backend
```

### Variables de entorno de producción
- `ENVIRONMENT=production`
- `DEBUG=false`
- `SECRET_KEY=<strong-secret-key>`
- `DATABASE_URL=<production-db-url>`

## 📝 Licencia

Este proyecto está bajo la licencia MIT. 