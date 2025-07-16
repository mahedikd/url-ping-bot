import asyncio
import httpx
from prisma import Prisma
from datetime import datetime, timedelta, timezone


async def ping_url(entry, db, client: httpx.AsyncClient, bot=None, chat_id=None):
    is_up = False

    previous_status = entry.status

    for _ in range(entry.retry):
        try:
            response = await client.get(entry.url, timeout=10)
            if response.status_code < 400:
                print(f"✅ {entry.url} is UP")
                is_up = True
                break
        except Exception as e:
            print(f"❌ Error pinging {entry.url}: {e}")
        await asyncio.sleep(1)

    new_status = "UP" if is_up else "DOWN"

    # Update DB
    await db.pingurl.update(
        where={"id": entry.id},
        data={
            "last_checked": datetime.now(timezone.utc),
            "status": new_status,
        },
    )

    # Notify status changes only
    if bot and chat_id:
        try:
            if previous_status == "DOWN" and new_status == "UP":
                await bot.send_message(
                    chat_id=chat_id,
                    text=f"✅ <b>{entry.url}</b> is <b>BACK UP</b>!",
                    parse_mode="HTML",
                )
            elif previous_status != "DOWN" and new_status == "DOWN":
                await bot.send_message(
                    chat_id=chat_id,
                    text=f"⚠️ <b>{entry.url}</b> is <b>DOWN</b> after {entry.retry} attempts.",
                    parse_mode="HTML",
                )
        except Exception as e:
            print(f"❌ Failed to notify Telegram: {e}")

    return


def should_ping(entry):
    next_check = entry.last_checked + timedelta(seconds=entry.interval)
    return datetime.now(timezone.utc) >= next_check


async def ping_loop(db: Prisma, interval_seconds=15, bot=None):
    print("🚀 Starting ping_loop...")
    try:
        async with httpx.AsyncClient() as client:
            while True:
                try:
                    count = await db.pingurl.count()
                    if count > 0:
                        entries = await db.pingurl.find_many()
                        tasks = [
                            ping_url(
                                entry=entry,
                                db=db,
                                client=client,
                                bot=bot,
                                chat_id=entry.chat_id,
                            )
                            for entry in entries
                            if should_ping(entry)
                        ]
                        if tasks:
                            await asyncio.gather(*tasks)
                except Exception as e:
                    print(f"❌ Error in ping_loop: {e}")
                await asyncio.sleep(interval_seconds)
    except asyncio.CancelledError:
        print("🛑 ping_loop cancelled — shutting down cleanly.")
        raise
