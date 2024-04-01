from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def add_buttons_number() -> ReplyKeyboardMarkup:
    """
    Добавляет кнопки под чатом

    :return:
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    continue_btn = KeyboardButton(text='Продолжить (number)')
    menu_btn = KeyboardButton(text='В меню')
    keyboard.add(continue_btn, menu_btn)

    return keyboard


def add_buttons_date() -> ReplyKeyboardMarkup:
    """
    Добавляет кнопки под чатом

    :return:
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    continue_btn = KeyboardButton(text='Продолжить (date)')
    menu_btn = KeyboardButton(text='В меню')
    keyboard.add(continue_btn, menu_btn)

    return keyboard


def add_buttons_random() -> ReplyKeyboardMarkup:
    """
    Добавляет кнопки под чатом

    :return:
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    continue_btn = KeyboardButton(text='Продолжить (random)')
    menu_btn = KeyboardButton(text='В меню')
    keyboard.add(continue_btn, menu_btn)

    return keyboard


def add_buttons_trivia() -> ReplyKeyboardMarkup:
    """
    Добавляет кнопки под чатом

    :return:
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    continue_btn = KeyboardButton(text='Продолжить (trivia)')
    menu_btn = KeyboardButton(text='В меню')
    keyboard.add(continue_btn, menu_btn)

    return keyboard


def add_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    menu_btn = KeyboardButton(text='В меню')
    keyboard.add(menu_btn)

    return keyboard


def remove_buttons() -> ReplyKeyboardRemove:
    """
    Удаляет кнопки под чатом

    :return:
    """
    keyboard = ReplyKeyboardRemove()
    return keyboard
