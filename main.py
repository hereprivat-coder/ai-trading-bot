from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
import os

TELEGRAM_TOKEN = os.getenv("8285751565:AAFLHNnE2g5z6MHsrJK1aYspiNlLN91iBm4")
OPENAI_API_KEY = os.getenv("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")

client = OpenAI(api_key=OPENAI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! 🤖 Я AI-помощник для трейдинга.\nЗадай вопрос — и я помогу!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Ты AI трейдер, объясняй чётко и по делу."},
            {"role": "user", "content": user_text}
        ]
    )
    await update.message.reply_text(response.choices[0].message.content)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
