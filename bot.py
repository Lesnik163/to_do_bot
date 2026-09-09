import os

import telebot
from dotenv import load_dotenv

from models.task import Task

tasks = []
load_dotenv()

token = os.getenv("BOT_TOKEN")
if not token:
    raise ValueError("BOT_TOKEN не найден. Проверьте файл .env")

bot = telebot.TeleBot(token)
print("Бот запущен")
bot.polling(none_stop=True)