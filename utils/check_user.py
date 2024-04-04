from telebot.types import Message

from database.common.db_models import User, db
from database.core import crud

from loguru import logger

from utils.remove_queries import del_queries

logger.add("out.log", backtrace=True, diagnose=True)
update_nfo = crud.update()


@logger.catch()
def check_user(message: Message) -> bool:
    """
    Проверяет есть ли пользователь в базе данных и изменяет
    информацию о пользователе если он её поменял.
    Удаляет не отображаемые данные из таблицы результатов (оставляет последние 10)

    :param message: сообщение пользователя
    :return:
    """
    user_id = message.from_user.id
    data = {}

    del_queries(user_id)  # Удаление лишних записей из таблицы QueryResult

    if User.get_or_none(User.user_id == user_id):
        user_info = User.get(User.user_id == user_id)

        if str(user_info.username) != str(message.from_user.username) \
                or user_info.username != message.from_user.username:
            data.update({'username': message.from_user.username})

        if str(user_info.first_name) != str(message.from_user.first_name) \
                or user_info.first_name != message.from_user.first_name:
            data.update({'first_name': message.from_user.first_name})

        if str(user_info.last_name) != str(message.from_user.last_name) \
                or user_info.last_name != message.from_user.last_name:
            data.update({'last_name': message.from_user.last_name})
        if len(data) > 0:
            update_nfo(db, User, data)
            logger.info(f'Данные пользователя изменились {data.items()}')

        return True
    else:
        return False
