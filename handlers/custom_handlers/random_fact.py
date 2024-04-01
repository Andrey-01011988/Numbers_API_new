import requests

from keyboards.reply import continue_menu_buttons
from loader import bot

from telebot.types import Message

from database.common.db_models import db, QueryResult
from database.core import crud
from states.get_facts import NumbersFacts
from site_API.site_core import url, headers, params
from site_API.site_handlers import site_api_handlers
from utils.check_user import check_user
from handlers.default_handlers.help import bot_help

from datetime import datetime

from loguru import logger

db_write = crud.create()


@bot.message_handler(commands=['random'])
def get_min(message: Message) -> None:
    """
    Обрабатывает сообщение пользователя, команду /random
    :param message: сообщение пользователя

    :param message: сообщение пользователя
    :return: None
    """
    if check_user(message):

        bot.set_state(message.from_user.id, NumbersFacts.random_fact_min, message.chat.id)
        bot.send_message(message.from_user.id, f'{message.from_user.first_name}, '
                                               f'введите нижнюю границу диапазона целым числом от 0 и более')
    else:
        bot.reply_to(message, "Вы не зарегистрированы. Напишите /start")


@bot.message_handler(func=lambda message: message.text == 'Продолжить (random)')
def get_min(message: Message) -> None:
    """
    Обрабатывает сообщение пользователя, команду /random
    :param message: сообщение пользователя

    :param message: сообщение пользователя
    :return: None
    """
    if check_user(message):

        bot.set_state(message.from_user.id, NumbersFacts.random_fact_min, message.chat.id)
        bot.send_message(message.from_user.id, f'{message.from_user.first_name}, '
                                               f'введите нижнюю границу диапазона целым числом от 0 и более',
                         reply_markup=continue_menu_buttons.remove_buttons())
    else:
        bot.reply_to(message, "Вы не зарегистрированы. Напишите /start")


@bot.message_handler(state=NumbersFacts.random_fact_min)
def get_max(message: Message) -> None:
    """
    Проверяет правильность ввода и сохраняет введенное пользователем число,
     запрашивает верхнюю границу

    :param message: сообщение пользователя
    :return: None
    """
    if message.text.isdigit():
        bot.set_state(message.from_user.id, NumbersFacts.random_fact_max, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['min'] = message.text
        bot.send_message(message.from_user.id, 'Спасибо, записал, теперь введите верхнюю границу')

    elif message.text == '/help':
        bot.delete_state(message.from_user.id)
        # Регистрация функции для вызова после указанного сообщения
        bot.register_next_step_handler(message, bot_help)

    else:
        bot.send_message(message.from_user.id, 'Нужно ввести целое число от 0 и более')


@bot.message_handler(state=NumbersFacts.random_fact_max)
def get_random_fact(message: Message) -> None:
    """
    Проверяет и сохраняет введенное пользователем число и по
    заданным параметрам выводит результат запроса от сервера

    local_params:

    :param message: сообщение пользователя
    :return: None
    """
    if message.text.isdigit():
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:

            if int(data['min']) < int(message.text):
                data['max'] = message.text
                bot.send_message(message.from_user.id, 'Спасибо, записал. Ищу факт')

            else:
                bot.send_message(message.from_user.id, 'Верхняя граница должна быть больше нижней')
                return

            local_params = {}
            local_params.update(data)
            local_params.update(params)
            logger.info(f'Создан запрос пользователем о случайном числе {message.from_user.id}')
            response = site_api_handlers.get_random_fact('GET', url=url, headers=headers,
                                                         params=local_params, timeout=5)

            if response.status_code == requests.codes.ok:
                ans = response.json()
                req_info = [{'user_id': message.from_user.id, 'query_date': datetime.now().replace(microsecond=0),
                             'result_text': f'{ans["number"]} - {ans["text"]}'}]
                db_write(db, QueryResult, req_info)
                bot.send_message(message.from_user.id, f'{ans["number"]} - {ans["text"]}')
                logger.info('Запрос успешно обработан')

            else:
                logger.info(f'Код ошибки {response.status_code}')
                bot.send_message(message.from_user.id, 'Что-то пошло не так')

    elif message.text == '/help':
        bot.delete_state(message.from_user.id)

    else:
        bot.send_message(message.from_user.id, 'Нужно ввести целое число от 0 и более')

    logger.info(f'Пользователь {message.from_user.id} завершил цикл')

    bot.clear_step_handler_by_chat_id(message.chat.id)

    bot.send_message(message.from_user.id,
                     'Можете продолжить нажав, "Продолжить", или нажмите "В меню"для выбора других опций',
                     reply_markup=continue_menu_buttons.add_buttons_random())
