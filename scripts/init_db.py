#!/usr/bin/env python3
"""
Script para inicializar la base de datos con Prisma
"""

import asyncio
import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.append(str(Path(__file__).parent.parent))

from app.infrastructure.database.prisma_client import prisma_client

async def init_database():
    try:
        print("🔌 Conectando a la base de datos...")
        await prisma_client.connect()
        print("✅ Conexión exitosa a PostgreSQL")

    except Exception as e:
        print(f"❌ Error conectando a la base de datos: {e}")

    finally:
        print("🔌 Cerrando conexión...")
        await prisma_client.disconnect()
        print("✅ Conexión cerrada.")


if __name__ == "__main__":
    asyncio.run(init_database()) 