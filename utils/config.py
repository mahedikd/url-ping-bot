import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = str(os.getenv("BOT_TOKEN"))
REMOVE_INTERVAL_HOURS = int(os.getenv("REMOVE_INTERVAL_HOURS") or 0)
CHAT_ID = int(os.getenv("CHAT_ID") or 0)
