from datetime import datetime

import requests

from keyboards.reply import continue_menu_buttons
from loader import bot

from telebot.types import Message

from loguru import logger

from database.core import crud
from database.common.db_models import db, QueryResult
from site_API.site_handlers import site_api_handlers
from site_API.site_core import url, headers, params
from states.get_facts import NumbersFacts
from utils.check_user import check_user
from handlers.default_handlers.help import bot_help


db_write = crud.create()


@bot.message_handler(commands=["number"])
def get_number(message: Message) -> None:
    """
    Запрашивает у пользователя цифру, факт о которой он хочет узнать

    :param message: команда пользователя

    :return: None
    """
    if check_user(message):
        bot.set_state(message.from_user.id, NumbersFacts.math_fact_num, message.chat.id)
        bot.send_message(message.from_user.id, f'{message.from_user.first_name}, '
                                               f'введите любое целое число от 0 и более',
                         reply_markup=continue_menu_buttons.remove_buttons())
    else:
        bot.reply_to(message, "Вы не зарегистрированы. Напишите /start")


@bot.message_handler(func=lambda message: message.text == 'Продолжить (number)')
def get_number(message: Message) -> None:
    """
    Запрашивает у пользователя цифру, факт о которой он хочет узнать

    :param message: команда пользователя

    :return: None
    """
    if check_user(message):
        bot.set_state(message.from_user.id, NumbersFacts.math_fact_num, message.chat.id)
        bot.send_message(message.from_user.id, f'{message.from_user.first_name}, '
                                               f'введите любое целое число от 0 и более',
                         reply_markup=continue_menu_buttons.remove_buttons())
    else:
        bot.reply_to(message, "Вы не зарегистрированы. Напишите /start")


@bot.message_handler(state=NumbersFacts.math_fact_num)
def get_math_fact(message: Message) -> None:
    """
    get_math_fact
    Сохраняет введенное пользователем число и выводит по нему информацию,
    записывает в б/д ответ

    :param message: Число пользователя
    :return: None
    """
    if message.text.isdigit():
        logger.info(f'Пользователь {message.from_user.id} ввел цифру {message.text}')
        logger.info(f'Создан запрос факта о цифре пользователем {message.from_user.id}')
        number = str(message.text)
        response = site_api_handlers.get_math_fact('GET', url=url, headers=headers, params=params,
                                                   number=number, timeout=5)

        if response.status_code == requests.codes.ok:
            answer = response.json()
            req_info = [{'user_id': message.from_user.id, 'query_date': datetime.now().replace(microsecond=0),
                         'result_text': f'{number} - {answer["text"]}'}]
            db_write(db, QueryResult, req_info)
            bot.send_message(message.from_user.id, f'{number} - {answer["text"]}')
            logger.info('Запрос успешно обработан')

        else:
            logger.info(f'Код ошибки {response.status_code}')
            bot.send_message(message.from_user.id, 'Что-то пошло не так')

    elif message.text == '/help':
        bot.delete_state(message.from_user.id)
        # Регистрация функции для вызова после указанного сообщения
        bot.register_next_step_handler(message, bot_help)

    else:
        bot.send_message(message.from_user.id, 'Нужно ввести целое число от 0 и более')

    logger.info(f'Пользователь {message.from_user.id} завершил цикл')
    # удаляются состояния
    bot.delete_state(message.from_user.id, message.chat.id)

    # Очищает список функций, зарегистрированных с помощью register_next_step_handler()
    bot.clear_step_handler_by_chat_id(message.chat.id)

    bot.send_message(message.from_user.id,
                     'Можете продолжить нажав, "Продолжить", или нажмите "В меню"для выбора других опций',
                     reply_markup=continue_menu_buttons.add_buttons_number())
