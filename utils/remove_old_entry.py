import asyncio
from prisma import Prisma
from datetime import datetime, timedelta, timezone


async def remove_old_entry(db: Prisma, remove_interval_hours=1):
    if remove_interval_hours == 0:
        return

    print("🚀 Starting remove_old_entry...")
    try:
        while True:
            try:
                count = await db.pingurl.count()
                if count > 0:
                    entries = await db.pingurl.find_many()
                    for entry in entries:
                        delete_time = entry.created_at + timedelta(
                            hours=remove_interval_hours
                        )
                        if datetime.now(timezone.utc) >= delete_time:
                            await db.pingurl.delete(where={"id": entry.id})
            except Exception as e:
                print(f"❌ Error in remove_old_entry: {e}")
            await asyncio.sleep(1800)
    except asyncio.CancelledError:
        print("🛑 remove_old_entry cancelled — shutting down cleanly.")
        raise
