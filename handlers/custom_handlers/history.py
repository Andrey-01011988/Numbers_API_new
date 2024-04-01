from loader import bot

from loguru import logger

from telebot.types import Message
from database.common.db_models import User, QueryResult
from keyboards.reply import continue_menu_buttons


@logger.catch()
@bot.message_handler(commands=["history"])
def history(message: Message) -> None:
    """
    history
    Выдает пользователю ответы на последние 10 запросов

    :param message: сообщение пользователя
    :return: None
    """

    cur_user_id = message.from_user.id
    cur_user = User.get_or_none(User.user_id == cur_user_id)
    if cur_user:
        logger.info(f'Пользователь {cur_user} сделал запрос истории')

        queries = cur_user.queries.order_by(-QueryResult.query_date, -QueryResult.res_id).limit(10)
        text = [f'№{line.res_id} Создан: {line.query_date} Ответ: {line.result_text}\n' for line in queries]
        bot.send_message(message.from_user.id, '\n'.join(text))
        bot.send_message(message.from_user.id, 'Чтобы выйти в меню нажмите кнопку "В меню"',
                         reply_markup=continue_menu_buttons.add_menu())
        logger.info('Запрос выполнен')
    else:
        bot.reply_to(message, "Вы не зарегистрированы. Напишите /start")
        return
