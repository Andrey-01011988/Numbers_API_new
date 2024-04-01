from datetime import datetime
from typing import Dict

from loguru import logger

from database.common.db_models import QueryResult, db
from database.core import crud
from keyboards.reply import continue_menu_buttons
from loader import bot

db_write = crud.create()


def end_trivia(user_id: int) -> None:
    """
    Выполняет повторяющиеся операции при завершении обработчиков

    :param user_id:
    :return:
    """
    logger.info(f'Пользователь {user_id} завершил цикл')

    bot.send_message(user_id,
                     'Можете продолжить нажав, "Продолжить", или нажмите "В меню"для выбора других опций',
                     reply_markup=continue_menu_buttons.add_buttons_trivia())


def send_n_save_query(user_id: int, some_dict: Dict) -> None:
    """
    Выполняет повторяющуюся операцию отправки пользователю и сохранение результатов запроса

    :param user_id:
    :param some_dict:
    :return:
    """

    req_info = [{'user_id': user_id, 'query_date': datetime.now().replace(microsecond=0),
                 'result_text': f'{some_dict["number"]} - {some_dict["text"]}'}]
    db_write(db, QueryResult, req_info)
    bot.send_message(user_id, f'{some_dict["number"]} - {some_dict["text"]}')
    logger.info('Запрос успешно обработан')
    # Вызов функции завершения
    end_trivia(user_id)
