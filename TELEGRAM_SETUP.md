# Telegram AI Bot Setup

## 1. Create a Telegram bot

1. Open Telegram and search for `@BotFather`.
2. Send `/newbot`.
3. Choose a bot name and username ending in `bot`.
4. Copy the token privately. Never commit it to GitHub.

## 2. Configure the environment

In the environment where you will run the bot, create a local `.env` file:

```bash
cp .env.example .env
```

Set these values in `.env`:

```env
TELEGRAM_BOT_TOKEN=your_botfather_token
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini
```

To opt into an OpenAI-compatible proxy such as [FreeLLMAPI](https://github.com/tashfeenahmed/freellmapi),
set `OPENAI_BASE_URL=http://localhost:3001/v1` and put FreeLLMAPI's unified key in
`OPENAI_API_KEY` in this local `.env`. Also set `OPENAI_MODEL=auto` or a model ID listed by the
proxy at `http://localhost:3001/v1/models`; this bot's default `gpt-4o-mini` may not be available
there. FreeLLMAPI's dashboard is at `http://localhost:5173`; configure any upstream provider keys
there and copy the unified key for the bot. Do not commit `.env` or put either kind of key in this
repository. Leave `OPENAI_BASE_URL` unset to keep the existing OpenAI endpoint and default behavior.

FreeLLMAPI describes itself as intended for personal experimentation and learning, not production
use. It documents an OpenAI Responses API surface for text requests, which matches this bot's
text-only call; its guide says image input through `/v1/responses` is not supported.

For Android, FreeLLMAPI's [Termux guide](https://github.com/tashfeenahmed/freellmapi/blob/main/docs/en/install/02-android-termux.md)
is experimental and community-supported. It documents Android 7+, about 1 GB of free storage,
Termux from F-Droid, and Node.js 22.13+ (Node 24 LTS recommended). Android may suspend Termux, so
keeping the proxy running can require a wake lock and battery-optimization changes. For a phone-only
setup, the bot must also run on the same phone for `localhost` to reach the local proxy; this
repository has not tested its bot under Termux, so running both together on a phone is unverified.
`localhost` always refers to the device running the bot. If the bot and proxy run on different
devices, use a trusted LAN or private VPN (for example, Tailscale); do not port-forward development
servers to the public internet. The bot's default OpenAI endpoint does not require a phone-hosted proxy.

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
