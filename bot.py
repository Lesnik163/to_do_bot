import os

import telebot
from dotenv import load_dotenv

from models.task import Task
from services.tasks import find_task, find_task_by_name, parsed_task_id, tasks

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
        "/add — добавить задачу",
        "/delete  — удалить задачу",
        "/complete  — отметить задачу как выполненную",
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

    if find_task_by_name(task_name):
        bot.send_message(message.chat.id, "Такая задача уже есть")
        return

    task = Task(task_name)
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

@bot.message_handler(commands=['delete'])
def handle_delete(message):
    task_id = parsed_task_id(message.text)
    if task_id is None:
        bot.send_message(message.chat.id,
        "Неверный формат команды. Используйте: /delete номер задачи")
        return
    task = find_task(task_id)
    if task is None:
        bot.send_message(message.chat.id,
        "Такой задачи не существует")
        return
    tasks.remove(task)
    bot.send_message(message.chat.id,
    f'Удалено: \n{task}')

@bot.message_handler(commands=['complete'])
def handle_complete(message):
    task_id = parsed_task_id(message.text)
    if task_id is None:
        bot.send_message(message.chat.id,
        "Неверный формат команды. Используйте: /complete номер задачи")
        return
    task = find_task(task_id)
    if task is None:
        bot.send_message(message.chat.id,
        "Такой задачи не существует")
        return
    task.complete()
    bot.send_message(message.chat.id,
    f'Задача выполнена: \n{task}')

@bot.message_handler(func=lambda message: True)
def handle_unknown(message):
    bot.send_message(message.chat.id,
    "Я не понимаю эту команду. Используйте /help для получения списка команд.")

print("Бот запущен")
bot.polling(none_stop=True)