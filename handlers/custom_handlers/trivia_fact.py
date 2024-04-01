import requests

from loader import bot

from telebot.types import Message

from database.core import crud
from states.get_facts import NumbersFacts
from site_API.site_core import url, headers, params
from site_API.site_handlers import site_api_handlers
from utils.check_user import check_user
from utils.trivia_functions import send_n_save_query
from keyboards.Inline import inline_buttons
from keyboards.reply import continue_menu_buttons

from loguru import logger

db_write = crud.create()


# TODO сделай чтобы обработчики нажатия клавиш меняли состояния,
#  а все отправки сообщений пользователю остались здесь


def get_cipher(message: Message) -> None:
    """
    get_cipher
    Запрашивает у пользователя цифру

    :param message: команда пользователя
    :return: None
    """
    if check_user(message):
        bot.set_state(message.from_user.id, NumbersFacts.trivia_fact_num, message.chat.id)
        bot.send_message(message.from_user.id, f'{message.from_user.first_name}, '
                                               f'введите любое целое число от 0 и более',
                         reply_markup=continue_menu_buttons.remove_buttons())
    else:
        bot.reply_to(message, "Вы не зарегистрированы. Напишите /start")


@bot.message_handler(commands=['trivia'])
def start_trivia(message: Message) -> None:
    """
    start_trivia
    При вводе команды /trivia запускает функцию get_cipher

    :param message:
    :return:
    """
    get_cipher(message)


@bot.message_handler(func=lambda message: message.text == 'Продолжить (trivia)')
def continue_trivia(message: Message) -> None:
    """
    continue_trivia
    При нажатии на клавишу "Продолжить (trivia)" запускает функцию get_cipher

    :param message: команда пользователя
    :return: None
    """
    get_cipher(message)


@bot.message_handler(state=NumbersFacts.trivia_fact_num)
def get_trivia_fact(message: Message) -> None:
    """
    get_trivia_fact
    Сохраняет введенное пользователем число и выводит по нему информацию,
    записывает в б/д ответ

    :param message: Число пользователя
    :return: None
    """

    if message.text.isdigit():
        user_number = str(message.text)
        logger.info(f'Создан запрос на поиск числа по умолчанию пользователем {message.from_user.id}')

        with bot.retrieve_data(message.from_user.id) as data:
            data['user_answer'] = {}  # Словарь для хранения ответа от сервера
            data['user_id'] = message.from_user.id  # Сохраняю id текущего пользователя
            data['user_number'] = user_number  # Сохранил цифру пользователя

        local_params = {"notfound": "default"}
        local_params.update(params)
        response = site_api_handlers.get_trivia_fact('GET', url=url, headers=headers, params=local_params,
                                                     number=user_number, timeout=5)

        if response.status_code == requests.codes.ok:
            logger.info(f'Запрос обработан {response.status_code}')
            data['user_answer'] = response.json()
            if not data['user_answer']['found']:
                # Добавление кнопок и сообщения
                logger.info(f'Вывод пользователю {message.from_user.id} кнопок с предложением поиска другого числа')

                # Сообщение под которым будут размещены кнопки
                bot.send_message(message.from_user.id, 'Это число скучное, может, поискать рядом с ним поинтереснее?',
                                 reply_markup=inline_buttons.yes_no())

            # Далее вся информация будет обработана в других функциях

            else:
                send_n_save_query(data['user_id'], data['user_answer'])

        else:
            logger.info(f'Код ошибки {response.status_code}')
            bot.send_message(message.from_user.id, 'Что-то пошло не так')

    else:
        bot.send_message(message.from_user.id, 'Нужно ввести целое число от 0 и более')
