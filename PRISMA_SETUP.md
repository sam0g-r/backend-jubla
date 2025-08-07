# ⚙️ Configuración de Prisma con PostgreSQL

## 📋 Requisitos Previos

1. ✅ PostgreSQL corriendo en el puerto `5556`
2. ✅ Base de datos `jubla_db` creada
3. ✅ Python `3.12+` instalado
4. ✅ Node.js `16+` instalado (para usar el CLI de Prisma)

---

## 🚀 Configuración Paso a Paso

### 1. Instalar dependencias Python

Asegúrate de tener el cliente de Prisma para Python:

```bash
pip install -r requirements.txt
```

`requirements.txt` debe incluir:

```txt
prisma==0.13.0
```

---

### 2. Instalar Prisma CLI (Node.js)

Puedes elegir una de las siguientes opciones:

- **Recomendado** (sin instalación global):

```bash
npx prisma --version
```

- **Alternativa global**:

```bash
npm install -g prisma
```

> ⚠️ Asegúrate de que `prisma` esté disponible después de instalarlo.

-- **y el client**:
```bash
npm install @prisma/client
```

---

### 3. Configurar las variables de entorno

```bash
cp env.example .env
```

Edita el archivo `.env` con tus credenciales reales:

```env
DATABASE_URL=postgresql://usuario:contraseña@localhost:5556/jubla_db
```

---

### 4. Generar el cliente de Prisma

Antes de ejecutar, asegúrate de que tu archivo `schema.prisma` tenga este bloque:

```prisma
generator client {
  provider = "prisma-client-py"
}
```

Luego corre:

```bash
prisma py fetch      # Descarga binarios para Python
prisma generate      # Genera el cliente Prisma para Python
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

- Verifica que PostgreSQL esté corriendo en el puerto `5556`
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
- Los campos `created_at` y `updated_at` se actualizan automáticamente
- Los enums están definidos directamente en el esquema `.prisma`