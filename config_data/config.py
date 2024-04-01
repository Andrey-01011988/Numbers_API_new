import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

# путь к базе данных
DB_PATH = "database.db"

BOT_TOKEN = os.getenv("BOT_TOKEN")
RAPID_API_KEY = os.getenv("SITE_API")
HOST_API = os.getenv("HOST_API")
DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
    ("date", "Узнайте интересный факт о дате"),
    ("number", "Узнайте факт о положительном целом числе, если оно действительно интересное"),
    ("random", "Узнайте интересный факт о числе в заданном диапазоне"),
    ("trivia", "Узнайте интересный факт связанный с числом"),
    ("history", "Краткая история ответов (последние 10)"),
)

# формат назначенной даты у задачи
DATE_FORMAT = "%d.%m.%Y"
