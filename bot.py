# -*- coding: utf-8 -*-
"""
Телеграм-бот для рассылки гайда "Система периодизации".

Как это работает:
- Пользователь пишет боту /start (или любое сообщение)
- Бот отправляет приветственный текст + PDF-файл гайда

Установка (один раз):
    pip install python-telegram-bot==21.4

Запуск:
    python3 bot.py

Перед запуском:
1. Впиши свой токен от BotFather в TOKEN ниже
2. Положи PDF-файл гайда в ту же папку, что и этот скрипт,
   и укажи точное имя файла в GUIDE_PATH
"""

import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)

# ==== НАСТРОЙКИ ====
# Токен читается из переменной окружения TELEGRAM_TOKEN (безопасно для Railway).
# Для запуска на своём компьютере можно временно вписать токен прямо в кавычки ниже.
TOKEN = os.environ.get("TELEGRAM_TOKEN", "ВСТАВЬ_СЮДА_ТОКЕН_ОТ_BOTFATHER")
GUIDE_PATH = "Sistema_Periodizatsii_Guide.pdf"  # имя файла гайда, должен лежать рядом со скриптом

WELCOME_TEXT = (
    "Привет! 👋\n\n"
    "Это гайд по базовой системе периодизации — как строить прогресс в тренировках "
    "без хаоса, травм и выгорания.\n\n"
    "Забирай файл ниже 👇"
)

CAPTION_TEXT = "Базовая система периодизации — гайд"

# ==== ЛОГИКА БОТА (менять не нужно) ====

async def send_guide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_TEXT)
    with open(GUIDE_PATH, "rb") as f:
        await update.message.reply_document(document=f, caption=CAPTION_TEXT)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_guide(update, context)

async def any_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Любое текстовое сообщение тоже присылает гайд —
    # так проще: не нужно объяснять человеку, что писать
    await send_guide(update, context)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, any_message))
    print("Бот запущен. Нажми Ctrl+C чтобы остановить.")
    app.run_polling()
