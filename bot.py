import logging
import os

from openai import AsyncOpenAI
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

logging.basicConfig(level=logging.INFO)

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)
SYSTEM_PROMPT = (
    "You are Danny AI Assistant, a helpful and safe personal assistant. "
    "Reply in the same language as the user. Be concise and practical. "
    "Never claim to have completed an external action unless it was actually completed."
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "नमस्ते! मैं Danny AI Assistant हूँ 🤖\n\n"
        "आप मुझसे सवाल पूछ सकते हैं, ideas ले सकते हैं और अपने काम की planning कर सकते हैं।"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "/start - Assistant शुरू करें\n"
        "/help - मदद देखें\n\n"
        "कोई भी message भेजकर सवाल पूछें।"
    )


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    try:
        response = await client.responses.create(
            model=MODEL,
            instructions=SYSTEM_PROMPT,
            input=update.message.text,
        )
        await update.message.reply_text(response.output_text)
    except Exception:
        logging.exception("AI request failed")
        await update.message.reply_text(
            "अभी थोड़ी तकनीकी समस्या है। कृपया कुछ देर बाद फिर कोशिश करें।"
        )


def main() -> None:
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))
    application.run_polling()


if __name__ == "__main__":
    main()
