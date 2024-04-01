from telebot.types import Message

from loader import bot

from utils.check_user import check_user
from database.common.db_models import User, db
from database.core import crud

db_write = crud.create()


@bot.message_handler(commands=["start"])
def bot_start(message: Message) -> None:
    """
    Стартовое сообщение, записывает пользователя в б/д если он впервые зашел

    :param message: сообщение пользователя
    :return: None
    """
    if check_user(message):
        bot.reply_to(message, f"Здравствуйте, {message.from_user.full_name}, чтобы узнать все мои функции введите /help")
    else:
        user_info = [
            {
                'user_id': message.from_user.id,
                'username': message.from_user.username,
                'first_name': message.from_user.first_name,
                'last_name': message.from_user.last_name,
            }
        ]
        db_write(db, User, user_info)
        bot.reply_to(message, "Добро пожаловать, давайте найдем что-нибудь интересное!")
