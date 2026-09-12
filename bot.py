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

@bot.message_handler(commands=['add'])
def handle_add(message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip():
        bot.send_message(message.chat.id,
        'Неверный формат команды. Используйте: /add имя задачи')
        return
    task_name = parts[1].strip()
    
    task =  Task(task_name)
    tasks.append(task)
    bot.send_message(message.chat.id,
    f'Добавлено: \n{task}')

@bot.message_handler(commands=['list'])
def handle_list(message):
    if not tasks:
        bot.send_message(message.chat.id,
        "Список задач пуст")
        return
    task_list = "\n".join(str(task) for task in tasks)
    bot.send_message(message.chat.id,
    f"Список задач:\n{task_list}")



print("Бот запущен")
bot.polling(none_stop=True)