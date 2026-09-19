# Telegram AI Bot Setup

## 1. Create a Telegram bot

1. Open Telegram and search for `@BotFather`.
2. Send `/newbot`.
3. Choose a bot name and username ending in `bot`.
4. Copy the token privately. Never commit it to GitHub.

## 2. Configure the environment

In Codespaces or another secure environment:

```bash
cp .env.example .env
```

Set these values in `.env`:

```env
TELEGRAM_BOT_TOKEN=your_botfather_token
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
```

## 3. Install and run

```bash
pip install -r requirements-bot.txt
python bot.py
```

Then open Telegram, find your bot, and send `/start`.

## Security

- Do not paste tokens into public issues, chats, or commits.
- Do not commit `.env`.
- Stop the bot if the token is exposed and generate a new token in BotFather.
