# ⚙️ Configuración de Prisma con PostgreSQL

## 📋 Requisitos Previos

1. ✅ PostgreSQL corriendo en el puerto `5432` (por defecto en `docker-compose`)
2. ✅ Base de datos `jubla_db` creada
3. ✅ Python `3.12+` instalado
4. ✅ Node.js `16+` instalado (para usar el CLI de Prisma si lo necesitas)

---

## 🚀 Configuración Paso a Paso

### 1. Instalar dependencias Python

Asegúrate de tener las dependencias de Python del proyecto:

```bash
pip install -r requirements.txt
```

`requirements.txt` debe incluir (o instalarse manualmente):

```txt
prisma==0.13.0
prisma-client-py
```

> Nota: la versión exacta puede variar; usa la versión fijada en `requirements.txt` del repo.

---

### 2. Instalar Prisma CLI (opcional)

Para ejecutar comandos de Prisma localmente puedes usar `npx` (no requiere instalación global):

```bash
npx prisma --version
```

Si prefieres instalar de forma global:

```bash
npm install -g prisma
```

> También puedes ejecutar la mayoría de los comandos desde dentro de un contenedor si no tienes Node.js instalado localmente (ver sección "Usando Docker").

---

### 3. Configurar las variables de entorno

Copia el ejemplo y edita `.env` con tus credenciales reales:

```bash
cp env.example .env
```

Ejemplo relevante en `.env`:

```env
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/jubla_db
```

---

### 4. Generar el cliente de Prisma para Python

Asegúrate de que en `schema.prisma` exista el generador para Python:

```prisma
generator client {
  provider = "prisma-client-py"
}
```

Luego ejecuta (localmente):

```bash
prisma py fetch      # descarga binarios para Python
prisma generate      # genera el cliente Prisma para Python
```

Si usas `npx`:

```bash
npx prisma py fetch
npx prisma generate
```

---

### 5. Sincronizar el esquema con la base de datos

```bash
prisma db push
```

Esto aplicará el modelo definido en `schema.prisma` a tu base de datos PostgreSQL.

---

### 6. Verificar la conexión

Ejecuta el script para probar la conexión a la base de datos:

```bash
python scripts/init_db.py
```

Deberías ver un mensaje como:

```
✅ Conexión exitosa a PostgreSQL
👥 Usuarios encontrados: 0
✅ Conexión cerrada.
```

---

## 🐳 Usando Docker (opcional)

Si no quieres instalar Prisma/Node en tu máquina, puedes ejecutar los comandos dentro del contenedor `api` o usando `npx` dentro de un contenedor Node.

Ejemplo (ejecutar desde la raíz del repo):

```bash
docker compose up -d db redis
# Ejecutar prisma desde el servicio api (requiere que la imagen tenga las herramientas). Si no, usa npx en una imagen node:
docker compose run --rm node:18-alpine sh -c "npm install -g prisma && npx prisma --version"
```

Para generar el cliente usando `npx` desde un contenedor Node y apuntando a los archivos locales:

```bash
docker run --rm -v "$PWD":/work -w /work node:18-alpine sh -c "npm install -g prisma && npx prisma py fetch && npx prisma generate"
```

---

## 🧬 Estructura de la Base de Datos

El esquema de Prisma incluye los siguientes modelos:

- `User`: Usuarios del sistema
- `Event`: Eventos de Jubla
- `Registration`: Registros de usuarios a eventos
- `PaymentStatus`: Estados de pago
- `PastoralLetterStatus`: Estados de cartas pastorales

---

## 🛠️ Comandos Útiles

### Ver estado de la base de datos:

```bash
prisma db pull
```

### Abrir Prisma Studio (interfaz visual):

```bash
prisma studio
```

### Resetear la base de datos:

```bash
prisma db push --force-reset
```

### Generar migraciones (opcional):

```bash
prisma migrate dev --name init
```

---

## 🐞 Solución de Problemas

### ❌ Error de conexión

- Verifica que PostgreSQL esté corriendo en el puerto `5432`
- Asegúrate de que la base `jubla_db` exista
- Confirma que la `DATABASE_URL` esté bien escrita en `.env`

### ❌ Error al generar el cliente

- Asegúrate de tener `prisma-client-py` instalado (`pip show prisma-client-py`)
- Verifica que tu archivo `schema.prisma` tenga el bloque del generador con `provider = "prisma-client-py"`
- Ejecuta `prisma py fetch` y luego `prisma generate`

### ❌ Error de dependencias

- Revisa que tu entorno virtual esté activado
- Vuelve a instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## 📌 Notas Importantes

- Se usan **UUIDs como IDs** primarios
- Las relaciones usan `onDelete: Cascade`
- Los campos `createdAt` y `updatedAt` se actualizan automáticamente
- Los enums están definidos directamente en el esquema `.prisma`