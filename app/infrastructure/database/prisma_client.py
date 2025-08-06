from prisma import Prisma
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import asyncio
from functools import wraps

class PrismaClient:
    def __init__(self):
        self._client = Prisma()
        self._is_connected = False

    async def connect(self):
        """Conectar a la base de datos"""
        if not self._is_connected:
            await self._client.connect()
            self._is_connected = True

    async def disconnect(self):
        """Desconectar de la base de datos"""
        if self._is_connected:
            await self._client.disconnect()
            self._is_connected = False

    @property
    def client(self):
        """Obtener el cliente de Prisma"""
        return self._client

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()

# Instancia global del cliente
prisma_client = Prisma()

def with_prisma(func):
    """Decorador para manejar la conexión de Prisma automáticamente"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with prisma_client as client:
            return await func(*args, **kwargs)
    return wrapper

async def get_prisma_client() -> PrismaClient:
    """Obtener la instancia del cliente de Prisma"""
    return prisma_client 