import requests
from loguru import logger
from telebot.types import CallbackQuery

from keyboards.Inline import inline_buttons
from loader import bot
from site_API.site_core import params, url, headers
from site_API.site_handlers import site_api_handlers
from utils.trivia_functions import send_n_save_query, end_trivia


@bot.callback_query_handler(func=lambda call: call.data.startswith('cb'))
def callback_query_yes_no(call: CallbackQuery) -> None:
    """
    Обрабатывает нажатие пользователем кнопки Да или Нет

    :param call: cb_yes, cb_no
    :return: None
    """

    if call.data == 'cb_yes':
        logger.info(f'Пользователь {call.from_user.id} нажал кнопку "Да" ')
        logger.info(f'Вывод пользователю {call.from_user.id} кнопок с предложением'
                    f' поиска другого числа в левую сторону или в правую')

        message = call.message
        chat_id = message.chat.id
        message_id = message.message_id
        bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                              text='В какую сторону иcкать интересное число?', reply_markup=inline_buttons.left_right())

    elif call.data == 'cb_no':
        with bot.retrieve_data(call.from_user.id) as data:
            user_answer = data['user_answer']

        if not user_answer:
            logger.info(f'Что-то пошло не так user_answer: {user_answer} ')
        send_n_save_query(data['user_id'], user_answer)

        # Сделано для корректного закрытия сообщения
        bot.answer_callback_query(call.id)
        bot.delete_message(call.message.chat.id, call.message.id, timeout=1)


@bot.callback_query_handler(func=lambda call: call.data.endswith('cb'))
def callback_query_left_right(call: CallbackQuery) -> None:
    """
    Обрабатывает нажатие пользователем кнопки В большую или В меньшую

    :param call: right_cb, left_cb
    :return: None
    """

    with bot.retrieve_data(call.from_user.id) as data:
        number = data['user_number']

    if call.data == 'right_cb':
        logger.info(f'Пользователь {call.from_user.id} выбрал округлять '
                    f'в большую сторону ')

        logger.info(f'Создан измененный запрос на поиск числа пользователем {call.from_user.id}')
        # изменение параметров
        local_params = {"notfound": "ceil"}
        local_params.update(params)

        response = site_api_handlers.get_trivia_fact('GET', url=url, headers=headers, params=local_params,
                                                     number=number, timeout=5)
        if response.status_code == requests.codes.ok:
            logger.info(f'Запрос обработан {response.status_code}')
            answer = response.json()

            send_n_save_query(data['user_id'], answer)

            # Сделано для корректного закрытия сообщения
            bot.answer_callback_query(call.id)
            bot.delete_message(call.message.chat.id, call.message.id, timeout=1)

        else:
            logger.info(f'Код ошибки {response.status_code}')
            bot.send_message(call.from_user.id, 'Что-то пошло не так')
            # Сделано для корректного закрытия сообщения
            bot.answer_callback_query(call.id)
            bot.delete_message(call.message.chat.id, call.message.id, timeout=1)

    elif call.data == 'left_cb':
        logger.info(f'Пользователь {call.from_user.id} выбрал округлять '
                    f'в меньшую сторону ')

        # Сделано для корректного закрытия сообщения
        bot.answer_callback_query(call.id)
        bot.delete_message(call.message.chat.id, call.message.id, timeout=1)

        logger.info(f'Создан измененный запрос на поиск числа пользователем {call.from_user.id}')
        # изменение параметров
        local_params = {"notfound": "floor"}
        local_params.update(params)

        response = site_api_handlers.get_trivia_fact('GET', url=url, headers=headers, params=local_params,
                                                     number=number, timeout=5)
        if response.status_code == requests.codes.ok:
            logger.info(f'Запрос обработан {response.status_code}')
            answer = response.json()

            send_n_save_query(data['user_id'], answer)

        else:
            logger.info(f'Код ошибки {response.status_code}')
            bot.send_message(call.from_user.id, 'Что-то пошло не так')
            # Вызов функции завершения
            end_trivia(data['user_id'])

    else:
        # Вызов функции завершения
        end_trivia(data['user_id'])
