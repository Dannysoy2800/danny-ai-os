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

To use an OpenAI-compatible proxy such as [FreeLLMAPI](https://github.com/tashfeenahmed/freellmapi),
set `OPENAI_BASE_URL=http://localhost:3001/v1` and put the proxy's unified key in
`OPENAI_API_KEY` in your local `.env`. Leave `OPENAI_BASE_URL` unset to keep using OpenAI's
default endpoint. Do not commit `.env` or share the key. FreeLLMAPI describes itself as intended
for personal experimentation and learning, not production use.

On Android, FreeLLMAPI's [Termux guide](https://github.com/tashfeenahmed/freellmapi/blob/main/docs/en/install/02-android-termux.md)
is experimental and community-supported; this project has not tested it. Its documented setup
requires Android 7+, about 1 GB of free storage, Termux from F-Droid, and Node.js 22.13+ or Node 24
LTS. Android may suspend Termux, so sustained local hosting can require a wake lock and battery
optimization changes. No phone setup is required for the bot's default OpenAI endpoint.

`localhost` must refer to the machine running the bot and proxy. If they run on different devices,
use a trusted LAN or private VPN (for example, Tailscale); do not expose development servers by
port-forwarding them to the public internet.

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
