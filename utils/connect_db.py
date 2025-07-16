from prisma import Prisma


async def data_base_connect():
    db = Prisma()
    await db.connect()
    return db
