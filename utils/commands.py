from telegram import Update
from telegram.ext import ContextTypes
from .config import CHAT_ID

# Telegram command handlers
# All supported commands are /start, /help, /list, /add, /remove


def check_chat_id(chat_id, chat_id_tele):
    if chat_id and chat_id != chat_id_tele:
        return False
    return True


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat:
        if not check_chat_id(CHAT_ID, update.effective_chat.id):
            return

        await context.bot.send_message(
            chat_id=CHAT_ID or update.effective_chat.id,
            text=(
                "📡 <b>Ping your URLs</b> to keep free servers alive!\n"
                "ℹ️ Use <code>/help</code> for usage instructions."
            ),
            parse_mode="HTML",
        )

    return


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat:
        if not check_chat_id(CHAT_ID, update.effective_chat.id):
            return
        await context.bot.send_message(
            chat_id=CHAT_ID or update.effective_chat.id,
            text=(
                "<b>Use</b> <code>/add &lt;url&gt; &lt;interval&gt; &lt;retry&gt;</code> to add a URL to the ping list.\n"
                "<b>Use</b> <code>/remove &lt;url&gt;</code> to remove a URL from the ping list.\n"
                "<b>Use</b> <code>/list</code> to see all URLs in the ping list.\n\n"
                "<b>Example:</b>\n"
                "<code>/add https://google.com 60 3</code>\n"
                "<code>/remove https://google.com</code>\n"
                "<code>/list</code>"
            ),
            parse_mode="HTML",
        )

    return


async def list_urls(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat is None:
        return

    if not check_chat_id(CHAT_ID, update.effective_chat.id):
        return

    db = context.application.bot_data["db"]
    entries = await db.pingurl.find_many(
        where={"chat_id": str(update.effective_chat.id)}
    )

    if len(entries) == 0:
        await context.bot.send_message(
            chat_id=CHAT_ID or update.effective_chat.id,
            text="No URLs found in the ping list",
        )
        return

    await context.bot.send_message(
        chat_id=CHAT_ID or update.effective_chat.id,
        text=(
            "<b>Current PingUrl Entries:</b>\n"
            + "<code>Index | URL | Interval | Retries | Status</code>\n"
            + "\n".join(
                [
                    f"{index + 1}.<code> {entry.url} | {entry.interval} | {entry.retry} | {entry.status}</code>"
                    for index, entry in enumerate(entries)
                ]
            )
        ),
        parse_mode="HTML",
    )

    return


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat is None:
        return

    if not check_chat_id(CHAT_ID, update.effective_chat.id):
        return

    args: list[str] = context.args or []

    if len(args) != 3:
        await context.bot.send_message(
            chat_id=CHAT_ID or update.effective_chat.id,
            text="<b>Usage:</b> /add &lt;url&gt; &lt;interval&gt; &lt;retry&gt;",
            parse_mode="HTML",
        )
        return

    if not args[1].isnumeric() or not args[2].isnumeric():
        await context.bot.send_message(
            chat_id=CHAT_ID or update.effective_chat.id,
            text="<b>Usage:</b> /add &lt;url&gt; &lt;interval&gt; &lt;retry&gt;",
            parse_mode="HTML",
        )
        return

    if not args[0].startswith("http://") and not args[0].startswith("https://"):
        await context.bot.send_message(
            chat_id=CHAT_ID or update.effective_chat.id,
            text="<b>Usage:</b> /add &lt;url&gt; &lt;interval&gt; &lt;retry&gt;",
            parse_mode="HTML",
        )
        return

    db = context.application.bot_data["db"]
    await db.pingurl.create(
        data={
            "url": args[0],
            "interval": int(args[1]),
            "retry": int(args[2]),
            "chat_id": str(update.effective_chat.id),
        }
    )

    await context.bot.send_message(
        chat_id=CHAT_ID or update.effective_chat.id,
        text=(
            f"Added <b>{args[0]}</b> every <b>{args[1]}</b> seconds with <b>{args[2]}</b> retries to the ping list"
        ),
        parse_mode="HTML",
    )

    return


async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat is None:
        return

    if not check_chat_id(CHAT_ID, update.effective_chat.id):
        return

    args: list[str] = context.args or []

    if len(args) != 1:
        try:
            await context.bot.send_message(
                chat_id=CHAT_ID or update.effective_chat.id,
                text="<b>Usage:</b> /remove &lt;url&gt;",
                parse_mode="HTML",
            )
        except Exception as e:
            print("❌ send_message failed with:", repr(e))

        return

    db = context.application.bot_data["db"]
    await db.pingurl.delete_many(
        where={"url": args[0], "chat_id": str(update.effective_chat.id)}
    )
    await context.bot.send_message(
        chat_id=CHAT_ID or update.effective_chat.id,
        text=f"Removed <b>{args[0]}</b> from the ping list",
        parse_mode="HTML",
    )

    return
