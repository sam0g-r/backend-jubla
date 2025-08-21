# 🚀 Guía de Despliegue en Northflank

Esta guía te ayudará a desplegar la aplicación optimizada en Northflank, aprovechando el `Dockerfile` multi-etapa que hemos creado.

## Resumen de la Optimización

El `Dockerfile` ha sido reestructurado para usar un **build multi-etapa**. Esto resuelve el problema de alto consumo de memoria de la siguiente manera:

1.  **Etapa de `builder`**: Una imagen temporal con Node.js se encarga de la tarea pesada de generar el cliente de Prisma (`prisma generate`).
2.  **Etapa final**: La imagen final es ligera, basada en `python:3.12-slim`. No contiene Node.js ni las dependencias de desarrollo. Solo copia el cliente de Prisma ya generado desde la etapa de `builder`.

Esto resulta en una **imagen Docker más pequeña y un menor consumo de memoria** durante el despliegue y la ejecución.

---

## 📋 Pasos para Desplegar en Northflank

Aunque no puedo acceder a tu cuenta de Northflank, aquí tienes los pasos generales que deberías seguir en su plataforma.

### 1. Conectar tu Repositorio de Git

-   En tu proyecto de Northflank, ve a la sección de **"Code"** o **"Repositories"**.
-   Conecta tu cuenta de Git (GitHub, GitLab, Bitbucket, etc.) y selecciona el repositorio que contiene esta aplicación.

### 2. Configurar el Servicio de Despliegue

-   Crea un nuevo **servicio** en Northflank. Elige el tipo **"Deployment"** o **"Combined"** (si también necesitas una base de datos).
-   **Fuente del Repositorio**:
    -   **Repositorio**: Selecciona el repositorio que acabas de conectar.
    -   **Branch**: Elige la rama que quieres desplegar (ej. `main` o la rama con estos cambios).

### 3. Configurar el Build

Esta es la parte más importante.

-   En la configuración del servicio, busca la sección de **"Build Settings"** o **"Build Options"**.
-   **Tipo de Build**: Elige **`Dockerfile`**.
-   **Ruta del Dockerfile**:
    -   Asegúrate de que Northflank apunte al `Dockerfile` en la raíz del repositorio. El path debería ser `Dockerfile`. Northflank normalmente lo detecta automáticamente si está en la raíz.

### 4. Configurar Variables de Entorno

-   Ve a la sección de **"Environment Variables"** o **"Secrets"** de tu servicio.
-   Añade la variable de entorno `DATABASE_URL` con el valor correcto para tu base de datos de producción en Northflank.
    -   **Ejemplo**: `postgresql://user:password@host:port/dbname`
-   Añade cualquier otra variable de entorno que tu aplicación necesite (revisa tu archivo `.env.example`).

### 5. Configurar el Comando de Inicio (Opcional)

-   El `Dockerfile` ya incluye un `CMD` para iniciar la aplicación.
-   `CMD ["sh", "-c", "python -m prisma migrate deploy && uvicorn main:app --host 0.0.0.0 --port 8000"]`
-   Northflank debería usar este comando por defecto. Si te pide un "start command" o "runtime command", puedes dejarlo en blanco para que use el del `Dockerfile`.

### 6. Desplegar

-   Guarda la configuración del servicio.
-   Northflank debería iniciar el proceso de build y despliegue automáticamente.
-   Puedes monitorear los logs del build para asegurarte de que todo el proceso se completa sin errores. Con el `Dockerfile` optimizado, el paso de `prisma generate` no debería causar problemas de memoria.

---

## ✅ Verificación Post-Despliegue

1.  **Logs del Build**: Revisa que el build se complete exitosamente.
2.  **Logs de Runtime**: Una vez desplegado, revisa los logs de la aplicación para confirmar que se conecta a la base de datos y que el servidor `uvicorn` se inicia correctamente.
3.  **Endpoint Público**: Accede a la URL pública que Northflank te proporcione para verificar que la API responde.

Con estos pasos, tu aplicación debería desplegarse de manera eficiente y sin los errores de memoria que estabas experimentando.
