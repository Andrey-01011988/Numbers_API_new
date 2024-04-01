from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def yes_no() -> InlineKeyboardMarkup:
    """
    Создает инлайн кнопки Да/Нет (размещаются под сообщением)

    :return: InlineKeyboardMarkup
    """
    markup = InlineKeyboardMarkup()
    markup.row_width = 2  # количество кнопок под строкой
    markup.add(InlineKeyboardButton('Да', callback_data='cb_yes'),
               InlineKeyboardButton('Нет', callback_data='cb_no'))
    return markup


def left_right() -> InlineKeyboardMarkup:
    """
    Создает инлайн кнопки В меньшую/В большую (размещаются под сообщением)

    :return: None
    """
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton('В меньшую', callback_data='left_cb'),
               InlineKeyboardButton('В большую', callback_data='right_cb'))
    return markup
