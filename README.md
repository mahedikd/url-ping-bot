# Telegram Ping Bot

This project offers a lightweight and efficient solution for monitoring the status of your web services. It’s a minimal alternative to heavier tools like Uptime Kuma — ideal for users who want to keep services online without consuming much RAM or CPU.

## Key Features

- **Lightweight:** Uses minimal system resources.
- **Keep Services Alive:** Prevents free-tier services from sleeping due to inactivity.
- **Easy to Use:** Add, Remove, or List URLs using simple Telegram commands.
- **Telegram Notifications:** Get alerts directly in your Telegram chat when services go down.

## How It Works

The bot periodically sends HTTP requests (pings) to the URLs you specify. If a service fails to respond or returns an error, you’ll get notified via Telegram.

This is especially useful for:

- **Monitoring personal projects:** Websites, APIs, or other services.
- **Keeping free services awake:** Free platforms like Heroku, Render, etc., may sleep due to inactivity — this bot prevents that.

---

## Getting Started

To get started, you'll need your Telegram Chat ID and Bot Token.

### 1. Get Your Telegram Chat ID

Use [@userinfobot](https://t.me/userinfobot) on Telegram:

- Start a chat with the bot.
- It will reply with your user info, including your **Chat ID**.

### 2. Create a Telegram Bot

Use [@BotFather](https://t.me/botfather) to create your bot:

1. Start a chat with [@BotFather](https://t.me/botfather).
2. Send the `/newbot` command.
3. Follow instructions to set a bot name and username.
4. Copy the **bot token** it gives you.

---

## 3. Configure the Application

Create a `.env` file in project’s root with the following content:

```
BOT_TOKEN="your_telegram_bot_token"
CHAT_ID="your_telegram_chat_id"
REMOVE_INTERVAL_HOURS="hours_to_empty_the_database"
```

### Environment Variable Details

| Variable                | Description                                                                                                              |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `BOT_TOKEN`             | Your Telegram bot token from [@BotFather](https://t.me/botfather). Used to send notifications.                           |
| `CHAT_ID`               | Your Telegram Chat ID from [@userinfobot](https://t.me/userinfobot). Use `0` to allow any user to interact with the bot. |
| `REMOVE_INTERVAL_HOURS` | How often (in hours) the database should be cleared. Use `0` to disable automatic deletion.                              |

---

## Running the Bot

You can run this bot using either Docker or directly with Python.

- **Option 1: Docker**
  Make sure you have Docker and Docker Compose installed. Then run:

```
    docker compose up -d
```

This will build and start the bot in the background.

- **Option 2: Python (with uv)**

Make sure your environment is set up with dependencies (`uv sync`), then run:

```bash
    source .venv/bin/activate
    prisma db push
    uv run main.py
```

---

## Managing the Bot

You can manage monitored URLs through these Telegram commands:

### Available Commands

- `/help` — Shows all available commands and usage examples
- `/list` — Lists all currently monitored URLs
- `/add` — Adds a new URL to monitor
- `/remove` — Removes a URL from monitoring

---

## Example Usage

```
/add https://google.com 60 3
/remove https://google.com
/list
```
