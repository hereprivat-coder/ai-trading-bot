import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# Получаем токены из переменных окружения
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Проверки на наличие токенов
if not TELEGRAM_TOKEN:
    raise ValueError("❌ TELEGRAM_TOKEN не найден! Добавьте его в переменные окружения Render.")

if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY не найден! Добавьте его в переменные окружения Render.")

# Инициализация клиента OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! 🤖 AI бот подключен и готов к работе.")

# Обработка любых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    # Отправка запроса в OpenAI
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты AI-помощник трейдера. Отвечай чётко и по делу."},
                {"role": "user", "content": user_text}
            ]
        )
        answer = response.choices[0].message.content
    except Exception as e:
        answer = f"❌ Ошибка OpenAI: {e}"

    await update.message.reply_text(answer)

if __name__ == "__main__":
    print("🤖 Бот запущен!")

    # Инициализация приложения Telegram
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск Polling (без конфликтов)
    app.run_polling()
