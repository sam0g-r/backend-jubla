# Configuración de Prisma con PostgreSQL

## 📋 Requisitos Previos

1. **PostgreSQL corriendo en el puerto 5556**
2. **Base de datos `jubla_db` creada**
3. **Python 3.12+ instalado**

## 🚀 Configuración Paso a Paso

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

```bash
cp env.example .env
```

Edita el archivo `.env` con tus credenciales de PostgreSQL:

```env
DATABASE_URL=postgresql://usuario:contraseña@localhost:5556/jubla_db
```

### 3. Generar el cliente de Prisma

```bash
prisma py fetch
```

```bash
prisma generate
```

### 4. Sincronizar el esquema con la base de datos

```bash
prisma db push
```

### 5. Verificar la conexión

```bash
python scripts/init_db.py
```

## 📊 Estructura de la Base de Datos

El esquema de Prisma incluye:

- **User**: Usuarios del sistema
- **Event**: Eventos de Jubla
- **Registration**: Registros de usuarios a eventos
- **PaymentStatus**: Estados de pago
- **PastoralLetterStatus**: Estados de cartas pastorales

## 🔧 Comandos Útiles

### Ver el estado de la base de datos
```bash
prisma db pull
```

### Abrir Prisma Studio (interfaz visual)
```bash
prisma studio
```

### Resetear la base de datos
```bash
prisma db push --force-reset
```

### Generar migraciones (si usas migraciones)
```bash
prisma migrate dev --name init
```

## 🐛 Solución de Problemas

### Error de conexión
- Verifica que PostgreSQL esté corriendo en el puerto 5556
- Confirma que la base de datos `jubla_db` existe
- Revisa las credenciales en `DATABASE_URL`

### Error de esquema
- Ejecuta `prisma generate` después de cambios en el esquema
- Usa `prisma db push` para sincronizar cambios

### Error de dependencias
- Asegúrate de tener `prisma==0.13.0` en requirements.txt
- Ejecuta `pip install -r requirements.txt`

## 📝 Notas Importantes

- El esquema usa UUIDs como IDs
- Las relaciones están configuradas con `onDelete: Cascade`
- Los timestamps (`created_at`, `updated_at`) se manejan automáticamente
- Los enums están definidos en el esquema de Prisma 