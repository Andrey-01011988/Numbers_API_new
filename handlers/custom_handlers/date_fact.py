import requests

from keyboards.reply import continue_menu_buttons
from loader import bot

from telebot.types import Message

from database.common.db_models import db, QueryResult
from database.core import crud
from states.get_facts import NumbersFacts
from site_API.site_core import url, headers, params
from site_API.site_handlers import site_api_handlers
from utils.right_date import right_month, right_day
from utils.check_user import check_user
from handlers.default_handlers.help import bot_help

from datetime import datetime
from dateutil.parser import parse

from loguru import logger


db_write = crud.create()  # Создание и запись в таблицу данных


@bot.message_handler(commands=['date'])
def get_month(message: Message) -> None:
    """
    Обрабатывает сообщение пользователя, команду /date
    :param message: сообщение пользователя
    """
    if check_user(message):

        bot.set_state(message.from_user.id, NumbersFacts.date_fact_month, message.chat.id)
        bot.send_message(message.from_user.id, f'{message.from_user.first_name}, '
                                               f'введите месяц (числом от 1 до 12)',
                         reply_markup=continue_menu_buttons.remove_buttons())
    else:
        bot.reply_to(message, "Вы не зарегистрированы. Напишите /start")


@bot.message_handler(func=lambda message: message.text == 'Продолжить (date)')
def get_month(message: Message) -> None:
    """
    Обрабатывает сообщение пользователя, команду Продолжить

    :param message: сообщение пользователя
    """
    if check_user(message):

        bot.set_state(message.from_user.id, NumbersFacts.date_fact_month, message.chat.id)
        bot.send_message(message.from_user.id, f'{message.from_user.first_name}, '
                                               f'введите месяц (числом от 1 до 12)',
                         reply_markup=continue_menu_buttons.remove_buttons())
    else:
        bot.reply_to(message, "Вы не зарегистрированы. Напишите /start")


@bot.message_handler(state=NumbersFacts.date_fact_month)
def get_day(message: Message) -> None:
    """
    Сохраняет введенный номер месяца и запрашивает день
    """
    if message.text.isdigit() and right_month(message.text):

        logger.info(f'Пользователь {message.from_user.id} ввел месяц {message.text}')
        bot.set_state(message.from_user.id, NumbersFacts.date_fact_day, message.chat.id)
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['month'] = message.text
        bot.send_message(message.from_user.id, 'Спасибо, записал, теперь введите число месяца')

    elif message.text == '/help':
        bot.delete_state(message.from_user.id)
        # Регистрация функции для вызова после указанного сообщения
        bot.register_next_step_handler(message, bot_help)

    else:
        bot.send_message(message.from_user.id, 'Месяц нужно ввести целым числом от 1 до 12')


@bot.message_handler(state=NumbersFacts.date_fact_day)
def get_fact(message: Message) -> None:
    """
    get_fact
    Сохраняет число и выводит информацию по внесенным параметрам

    message.text.isdigit(): проверка является строка числом

    right_day(data['month'], message.text): проверка на правильный ввод дня

    response: отправка сформированного запроса на сервер

    right_date: формирование читаемой даты в ответе сервера

    req_info: формирование данных для внесения в б/д


    """
    if message.text.isdigit():
        logger.info(f'Пользователь {message.from_user.id} ввел день {message.text}')

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            if right_day(data['month'], message.text):
                data['day'] = message.text
                bot.send_message(message.from_user.id, 'Спасибо, записал. Ищу факт')
            else:
                bot.send_message(message.from_user.id, f'Такого числа в {data["month"]} месяце нет')
                return
            logger.info(f'Создан запрос поиска даты пользователем {message.from_user.id}')
            response = site_api_handlers.get_date_fact('GET', url=url, headers=headers, params=params,
                                                       date_day=data['day'], date_month=data['month'], timeout=5)

            if response.status_code == requests.codes.ok:
                # Получение ответа в формате JSON
                ans = response.json()
                # Создание записи информации в таблицу
                user_date = f'{data["day"]}.{data["month"]}.{ans["year"]}'

                right_date = parse(user_date).strftime('%d.%m.%Y')

                req_info = [{'user_id': message.from_user.id, 'query_date': datetime.now().replace(microsecond=0),
                             'result_text': f'{right_date} - {ans["text"]}'}]
                # Запись в таблицу
                db_write(db, QueryResult, req_info)

                bot.send_message(message.from_user.id, f'{right_date} - {ans["text"]}')
                logger.info('Запрос успешно обработан')

            else:
                logger.info(f'Код ошибки {response.status_code}')
                bot.send_message(message.from_user.id, 'Что-то пошло не так')

    elif message.text == '/help':
        bot.delete_state(message.from_user.id)  # функция bot_help будет вызвана автоматически

    else:
        bot.send_message(message.from_user.id, 'День нужно ввести целым числом')

    logger.info(f'Пользователь {message.from_user.id} завершил цикл')

    # Очищает список функций, зарегистрированных с помощью register_next_step_handler()
    bot.clear_step_handler_by_chat_id(message.chat.id)

    bot.send_message(message.from_user.id,
                     'Можете продолжить нажав, "Продолжить", или нажмите "В меню"для выбора других опций',
                     reply_markup=continue_menu_buttons.add_buttons_date())
