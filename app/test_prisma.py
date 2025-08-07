# test_prisma.py
import asyncio
from prisma import Prisma

async def main():
    db = Prisma()
    print("🟡 Conectando a la base de datos...")
    await db.connect()
    print("🟢 Conexión exitosa.")

    # Puedes probar una consulta si tienes un modelo User
    try:
        users = await db.user.find_many()
        print(f"👥 Usuarios encontrados: {len(users)}")
    except Exception as e:
        print(f"⚠️ No se pudo consultar usuarios: {e}")

    await db.disconnect()
    print("🔴 Conexión cerrada.")

if __name__ == "__main__":
    asyncio.run(main())