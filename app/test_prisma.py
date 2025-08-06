# test_prisma.py
import asyncio
from prisma import Prisma

async def main():
    db = Prisma()
    await db.connect()
    print("✅ Prisma conectado")
    await db.disconnect()
    print("✅ Prisma desconectado")

asyncio.run(main())
