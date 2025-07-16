import asyncio
from telegram import BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler

from utils.connect_db import data_base_connect
from utils.commands import start, help, add, list_urls, remove
from utils.bg_task import ping_loop
from utils.remove_old_entry import remove_old_entry
from utils.config import BOT_TOKEN, REMOVE_INTERVAL_HOURS


async def on_startup(application):
    await application.bot.set_my_commands(
        [
            BotCommand("start", "Starts the bot"),
            BotCommand("help", "Shows help message"),
            BotCommand("list", "Lists all URLs in the ping list"),
            BotCommand("add", "Adds a URL to the ping list"),
            BotCommand("remove", "Removes a URL from the ping list"),
        ]
    )
    db = await data_base_connect()
    application.bot_data["db"] = db
    application.ping_task = asyncio.create_task(ping_loop(db=db, bot=application.bot))
    application.remove_task = asyncio.create_task(
        remove_old_entry(db=db, remove_interval_hours=REMOVE_INTERVAL_HOURS)
    )
    print("✅ DB connected")


async def on_shutdown(application):
    application.ping_task.cancel()
    application.remove_task.cancel()
    try:
        await application.ping_task
        await application.remove_task
    except asyncio.CancelledError:
        print("🛑 ping_task cancelled")
        print("🛑 remove_task cancelled")

    await application.bot_data["db"].disconnect()
    print("🔌 DB disconnected")


def main():
    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .post_init(on_startup)
        .post_shutdown(on_shutdown)
        .build()
    )
    start_handler = CommandHandler("start", start)
    help_handler = CommandHandler("help", help)
    add_handler = CommandHandler("add", add)
    list_handler = CommandHandler("list", list_urls)
    remove_handler = CommandHandler("remove", remove)

    application.add_handler(start_handler)
    application.add_handler(help_handler)
    application.add_handler(add_handler)
    application.add_handler(list_handler)
    application.add_handler(remove_handler)

    application.run_polling()


if __name__ == "__main__":
    main()

