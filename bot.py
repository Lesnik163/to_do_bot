import os

import telebot
from dotenv import load_dotenv

from services.tasks import (
    add_task,
    complete_task,
    delete_task,
    find_task_by_name,
    get_tasks,
    parsed_task_id,
)

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
        "/add купить хлеб — добавить задачу",
        "/delete 1 — удалить задачу",
        "/complete 1 — отметить задачу как выполненную",
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
    user_id = message.from_user.id

    if find_task_by_name(task_name, user_id):
        bot.send_message(message.chat.id, "Такая задача уже есть")
        return

    task = add_task(task_name, user_id)
    bot.send_message(message.chat.id,
    f'Добавлено: \n{task}')

@bot.message_handler(commands=['list'])
def handle_list(message):
    user_tasks = get_tasks(message.from_user.id)
    if not user_tasks:
        bot.send_message(message.chat.id,
        "Список задач пуст")
        return
    task_list = "\n".join(str(task) for task in user_tasks)
    bot.send_message(message.chat.id,
    f"Список задач:\n{task_list}")

@bot.message_handler(commands=['delete'])
def handle_delete(message):
    task_id = parsed_task_id(message.text)
    if task_id is None:
        bot.send_message(message.chat.id,
        "Неверный формат команды. Используйте: /delete номер задачи")
        return
    task = delete_task(task_id, message.from_user.id)
    if task is None:
        bot.send_message(message.chat.id,
        "Такой задачи не существует")
        return
    bot.send_message(message.chat.id,
    f'Удалено: \n{task}')

@bot.message_handler(commands=['complete'])
def handle_complete(message):
    task_id = parsed_task_id(message.text)
    if task_id is None:
        bot.send_message(message.chat.id,
        "Неверный формат команды. Используйте: /complete номер задачи")
        return
    task = complete_task(task_id, message.from_user.id)
    if task is None:
        bot.send_message(message.chat.id,
        "Такой задачи не существует")
        return
    bot.send_message(message.chat.id,
    f'Задача выполнена: \n{task}')

@bot.message_handler(func=lambda message: True)
def handle_unknown(message):
    bot.send_message(message.chat.id,
    "Я не понимаю эту команду. Используйте /help для получения списка команд.")

print("Бот запущен")
bot.polling(none_stop=True)