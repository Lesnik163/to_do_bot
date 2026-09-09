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

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id,
    "Привет! Я бот для списка дел. Напиши /help — список команд.",
    )

@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.send_message(message.chat.id,
    '\n'.join([
        "Список команд:",
        "/start — начать работу с ботом",
        "/add <задача> — добавить задачу",
        "/delete <номер> — удалить задачу",
        "/complete <номер> — отметить задачу как выполненную",
        "/list — показать список задач",
        "/help — показать список команд",
    ]),
    )

print("Бот запущен")
bot.polling(none_stop=True)