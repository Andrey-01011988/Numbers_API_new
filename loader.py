# Подгружаются нужные переменные для импорта
from telebot import TeleBot
from telebot.storage import StateMemoryStorage
from config_data import config


# установка настроек хранилища состояний на время сессии
storage = StateMemoryStorage()
# Установка настроек бота (токен и хранилище состояний
bot = TeleBot(token=config.BOT_TOKEN, state_storage=storage)
